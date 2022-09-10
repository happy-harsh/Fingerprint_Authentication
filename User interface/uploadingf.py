# # Import the required Libraries
# from PIL import ImageTk
# import PIL.Image
# from tkinter import *
# from tkinter import ttk, filedialog
# from tkinter.filedialog import askopenfile

# # Create an instance of tkinter frame
# win = Tk()

# # Set the geometry of tkinter frame
# win.geometry("700x350")


# def open_file():
#     canvas = Canvas(win, width=600, height=400)
#     canvas.pack()
#     file = filedialog.askopenfilename()
#     if file:

#         # Load an image in the script
#         img = ImageTk.PhotoImage(PIL.Image.open(file))
#         # Add image to the Canvas Items
#         canvas.create_image(10, 10, anchor=NW, image=img)
#         # content = file.read()
#         # file.close()
#         # print("%d characters in this file" % len(content))


# # Add a Label widget
# label = Label(win, text="Click the Button to browse the Files",
#               font=('Georgia 13'))
# label.pack(pady=10)

# # Create a Button
# ttk.Button(win, text="Browse", command=open_file).pack(pady=20)

# win.mainloop()

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk

my_w = tk.Tk()
my_w.geometry("410x300")  # Size of the window
my_w.title('www.plus2net.com')
my_font1 = ('times', 18, 'bold')
l1 = tk.Label(my_w, text='Upload Files & display', width=30, font=my_font1)
l1.grid(row=1, column=1, columnspan=4)
b1 = tk.Button(my_w, text='Upload Files',
               width=20, command=lambda: upload_file())
b1.grid(row=2, column=1, columnspan=4)


def upload_file():
    f_types = [('Jpg Files', '*.jpg'),
               ('PNG Files', '*.png')]   # type of files to select
    filename = tk.filedialog.askopenfilename(filetypes=f_types)
    col = 1  # start from column 1
    row = 3  # start from row 3
    for f in filename:
        img = Image.open(f)  # read the image file
        img = img.resize((100, 100))  # new width & height
        img = ImageTk.PhotoImage(img)
        e1 = tk.Label(my_w)
        e1.grid(row=row, column=col)
        e1.image = img
        e1['image'] = img  # garbage collection
        if(col == 3):  # start new line after third column
            row = row+1  # start wtih next row
            col = 1    # start with first column
        else:       # within the same row
            col = col+1  # increase to next column


my_w.mainloop()  # Keep the window open
