from tkinter import Label, Tk
from PIL import Image, ImageTk
# import tkFileDialog
from tkinter.filedialog import askopenfile
root = Tk()

path = askopenfile(filetypes=[("Image File", '.jpg')])
im = Image.open(path)
tkimage = ImageTk.PhotoImage(im)
myvar = Label(root, image=tkimage)
myvar.image = tkimage
myvar.pack()

root.mainloop()
