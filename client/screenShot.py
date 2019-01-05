from PIL import Image
from PIL import ImageTk
from StringIO import StringIO

# Read and  open screen shot
class ScreenShot:
    def __init__(self):
        pass

    def showImage(self, data):
        img = Image.open(StringIO(data))
        img.save("img.jpeg","JPEG")

        # photo = ImageTk.PhotoImage(img)
