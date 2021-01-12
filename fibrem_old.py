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
import numpy as np
from skimage.filters import gaussian
from skimage import io
from natsort import natsorted
from tkinter import *
from tkinter.ttk import *


# Main frame of the app
root = Tk()
root.title("Fib Rem: Sleeping aid for EM microscopists")
root.geometry("600x400")

## Frame to select people on duty so they can be called
dutyframe = Frame(root, padding=5, borderwidth=1, relief="solid")
dutyframe.grid(row=0, column=0)

# Init Off-duty 
ana_duty = IntVar(0)
eliz_duty = IntVar(0)
marc_duty = IntVar(0)

# Generate checkbuttons
label = Label(dutyframe, text='Select people to notify: ').pack()
check_ana = Checkbutton(dutyframe, text='Ana', variable=ana_duty).pack()
check_eliz = Checkbutton(dutyframe, text='Elisabeth', variable=eliz_duty).pack()
check_marc = Checkbutton(dutyframe, text='Marc', variable=marc_duty).pack()

# Call person on duty if problem detected
def call_on_problem():
    pass


## Left array of buttons
leftframe = Frame(root, padding=5, borderwidth=1, relief="solid")
leftframe.grid(row=1, column=0)

folder_to_watch = ""

def start_monitoring():
    folder_to_watch = filedialog.askdirectory(title="Select the images folder", mustexist= True)    

# Create buttons
startbutton = Button(leftframe, text='Start', command=start_monitoring).pack()
quitbutton = Button(leftframe, text='Exit', command=root.destroy).pack()

if not folder == "":
    images_on_init = [fname for fname in os.listdir(imgdir) if fname.endswith('tiff')]




root.mainloop()











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
