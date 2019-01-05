from PIL import ImageGrab
import StringIO
import struct
import utilities as Utilities

class ScreenShot:
    def __init__(self):
        pass

    def ScreenShots(self):
        img = ImageGrab.grab()          # Capture screen shot
        output = StringIO.StringIO()    # Create string object
        img.save(output, 'JPEG')        # Write image to stringIO as JPEG
        return self.packFile(output.getvalue())    # Send image as string format

    def packFile(self, data):
        # Prefix each message with a 4-byte length (network byte order)
        data = struct.pack('>I', len(data)) + data
        return Utilities.getResponseObject(True, data)
