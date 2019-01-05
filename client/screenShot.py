
from StringIO import StringIO
from Tkinter import *
from PIL import Image
from PIL import ImageTk
# Read and  open screen shot
class ScreenShot:
    def __init__(self):
        pass

    def showImage(self, data):
        # Convert data to image
        img = Image.open(StringIO(data))
        # img.save("img.jpeg","JPEG") # Save image to file

        # Open image in Tkinter
        root = Tk()
        imgTk = ImageTk.PhotoImage(img)
        panel = Label(root, image=imgTk)
        panel.pack(side="bottom", fill="both", expand="yes")
        root.mainloop()
