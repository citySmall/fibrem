#!/usr/bin/env python3
import pdb
import os
import skimage
import tkinter as tk
import numpy as np
from skimage.filters import gaussian
from tkinter import filedialog
from skimage import io
from tkinter import messagebox
from natsort import natsorted
from tkinter import ttk

LARGE_FONT= ("Verdana", 12) 

class FibRem(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Fib Rem: Sleeping aid for FIBSEMers")
        
        # init main window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
    
        # Init dict of frames
        self.frames = {}

        # the start page
        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, framekey):

        frame = self.frames[framekey]
        frame.tkraise()

        
        
class StartPage(tk.Frame):

    def __init__(self, parent, framekey):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text= "Go to page 1",
                            command=lambda: framekey.show_frame(PageOne))
        button1.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, framekey):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 1", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text= "Go Start Page",
                            command=lambda: framekey.show_frame(StartPage))
        button1.pack()


        
app = FibRem()
app.mainloop()
        








class WatchImgFolder:
    
    def __init__(self, *args, **kargs):
        pass
    pass

# def new_dialog():
    
#     # Create an empty dialog object
#     parent = tkinter.Tk() # Create the object
#     parent.overrideredirect(1) # Avoid it appearing and then disappearing quickly
#     #parent.iconbitmap("PythonIcon.ico") # Set an icon (this is optional - must be in a .ico format)
#     parent.withdraw() # Hide the window as we do not want to see this one

#     return parent

# def images_directory():
    
#     # Ask the user for the folder where images are being stored
#     parent = new_dialog()
#     directory = filedialog.askdirectory(title='Select images folder', parent=parent)
    
#     return directory


# def detect_new_image(imgdir):
    
#     images_on_init = [fname for fname in os.listdir(imgdir) if fname.endswith('tiff')]
    
#     if images_on_init == []:
#         parent = new_dialog()
#         error = messagebox.showerror('Error images directory',
#                                      '''The directory chosen doesnt contain any tiff image.\
#                                         Wrong directory chosen or SEM adquisition not started.''',
#                                       parent=parent)
        
          
#     # Sort the images
#     images_on_init = natsorted(images_on_init)
    
#     # Calculate the focus index for each init image
#     for imgfname in images_on_init:
#         calculate_focus(os.path.join(imgdir, imgfname))
   
#    # watch for new images appearing and calculate the FI 

#     return images_on_init


# def calculate_focus(imgpath):
#     new_image = io.imread(imgpath)
#     smooth_short = gaussian(new_image, sigma=2)
#     smooth_long  = gaussian(new_image, sigma=4)
#     pixwise_dif = smooth_short - smooth_long
#     focus_index = np.sum(np.sqrt(np.square(pixwise_dif))) / new_image.size
#     print(imgpath + ": " + str(focus_index))

    
    





    
# if __name__=='__main__':    
#     dir_to_watch = images_directory()
#     detect_new_image(dir_to_watch)
