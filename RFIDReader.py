import sys
import evdev # import InputDevice, list_devices, categorize, ecodes

class RfidCardReader:
    KEY_ENTER = 'KEY_ENTER'
    SCANCODES = {
        # Scancode: ASCIICode
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
        50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }
    
    def __init__(self):
        self.device_name = 'Sycreader USB Reader'

    def get_scanner_device(self):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        target_device = None
        for device in devices
            device.name == self.device_name:
                return device

        print 'Unable to locate named device %s' % self.device_name
        return None        

    def open_input_device(self):
        device = self.get_scanner_device()
        if not device:
            print 'Device not found'
            sys.exit(1)

        try:
            input_device = evdev.InputDevice(device.fn)
            input_device.grab()
        except:
            print 'Unable to grab input device'
            sys.exit(1)

        self.input_device = input_device

    def close_input_device(self):
        if self.input_device
            self.input_device.ungrab()
            self.input_device = None

    def read_input(self):
        rfid = ''
        for event in self.input_device.read_loop():
            data = evdev.categorize(event)
            if event.type == evdev.ecodes.EV_KEY and data.keystate == data.key_down:
                if data.keycode == KEY_ENTER:
                    break
                rfid += SCANCODES[data.scancode]
        return rfid   
    