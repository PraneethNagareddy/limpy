import sys
from core.spider import Spider
from kinematics.gait.gait import WalkingGait
from kinematics.gait.tripod_gait import TripodGait
import logging
import threading
import time

class KeyboardController:
    def __init__(self, gait: WalkingGait = TripodGait()):
        self.spider = Spider.get()
        self.gait = gait
        self.running = False
        self.keys_pressed = set()
        
    def _read_keys(self):
        """Reads keypresses in a separate thread"""
        import termios
        import tty
        import select
        import os
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(sys.stdin.fileno())
            while self.running:
                # Wait for input with timeout
                if select.select([sys.stdin], [], [], 0.05)[0]:
                    # Read available bytes (up to 32)
                    data = os.read(fd, 32).decode('utf-8', 'ignore')
                    
                    self.keys_pressed.clear()
                    i = 0
                    while i < len(data):
                        if data[i] == '\x1b':
                            if i + 2 < len(data) and data[i+1] in ['[', 'O']:
                                ch3 = data[i+2]
                                if ch3 in ['A', 'B', 'C', 'D']:
                                    self.keys_pressed.add('\x1b[' + ch3) # Normalize to standard bracket
                                    i += 3
                                    continue
                                elif ch3 == '1' and i + 5 < len(data) and data[i+3:i+5] == ';5':
                                    self.keys_pressed.add('ctrl+' + data[i+5])
                                    i += 6
                                    continue
                        
                        ch = data[i].lower()
                        if ch in ['q', 'a', 'd', 'z', 'c', '\x03']:
                            self.keys_pressed.add(ch)
                        i += 1
                else:
                    self.keys_pressed.clear()
                    
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def start(self):
        self.running = True
        logging.info("Keyboard controller started. Use arrow keys to move. (Press 'q' or 'esc' to stop)")
        
        self.reader_thread = threading.Thread(target=self._read_keys)
        self.reader_thread.start()
        
        while self.running:
            try:
                # Handle Exit
                if 'q' in self.keys_pressed or '\x03' in self.keys_pressed:
                    logging.info("Exit key pressed.")
                    self.stop()
                    break

                # Handle discrete turns (mapped to 'a' and 'd')
                if 'a' in self.keys_pressed:
                    logging.info("\\r'a' Pressed (Turn Left)")
                    self.gait.turn_left()
                    continue
                if 'd' in self.keys_pressed:
                    logging.info("\\r'd' Pressed (Turn Right)")
                    self.gait.turn_right()
                    continue

                # Handle step left and step right (mapped to 'z' and 'c')
                if 'z' in self.keys_pressed:
                    logging.info("\\r'z' Pressed (Step Left)")
                    self.gait.step_left()
                    continue
                if 'c' in self.keys_pressed:
                    logging.info("\\r'c' Pressed (Step Right)")
                    self.gait.step_right()
                    continue

                # Handle continuous omni directional walking
                x = 0.0
                y = 0.0
                
                # Up / Down
                if '\x1b[A' in self.keys_pressed:
                    x += 1.0
                if '\x1b[B' in self.keys_pressed:
                    x -= 1.0
                    
                # Left / Right (Arrow keys)
                if '\x1b[D' in self.keys_pressed:
                    y -= 1.0
                if '\x1b[C' in self.keys_pressed:
                    y += 1.0

                if x != 0.0 or y != 0.0:
                    logging.info("\\rArrows pressed X:%f, Y:%f", x, y)
                    self.gait.walk_omni(x, y, stride_factor=1)
                else:
                    time.sleep(0.01)
                    
            except Exception as e:
                logging.error(f"Error in keyboard controller: {e}")
                self.running = False

        self.reader_thread.join()

    def stop(self):
        self.running = False
