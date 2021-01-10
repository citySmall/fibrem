#!/usr/bin/env python3
import pdb
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import os
import skimage
import tkinter as tk
import numpy as np
from skimage.filters import gaussian
from tkinter import *
from skimage import io
from natsort import natsorted



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
