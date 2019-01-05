from PIL import ImageGrab
import StringIO
import struct
import utilities as Utilities

class ScreenShot:
    def __init__(self):
        pass

    def CaptureScreenShot(self):
        img = ImageGrab.grab()          # Capture screen shot
        output = StringIO.StringIO()    # Create string object
        img.save(output, 'JPEG')        # Write image to stringIO as JPEG
        return output.getvalue()        # Send image as string format
