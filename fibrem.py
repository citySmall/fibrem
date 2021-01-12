#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import os
import pdb
import time
from skimage.filters import gaussian
from skimage import io
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


root = Tk()
root.title('FibRem: Seeping aid for EM microscopists')


class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path, patterns, logfunc):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)
        self.log = logfunc

    def on_created(self, event):
        # This function is called when a file is created
        # We sleep to allow time for the file to be created
        if event.src_path.split(".")[-1] == "tiff":
            time.sleep(5)
            get_focus_index(event.src_path)
        
    def on_deleted(self, event):
        # This function is called when a file is deleted
        self.log(f"Someone deleted {event.src_path}!")

    def on_moved(self, event):
        # This function is called when a file is moved    
        self.log(f"Someone moved {event.src_path} to {event.dest_path}")

class LeftFrame:
    def __init__(self, master):
        frm = Frame(master)
        
        # Watchdog init
        self.watchdog = None
        self.watch_path = None
    
        # People init Off-duty 
        self.ana_duty = IntVar(0)
        self.eliz_duty = IntVar(0)
        self.marc_duty = IntVar(0)

        # Generate checkbuttons
        Label(master, text='Select people to notify: ').pack(pady=5,  anchor=W)
        Checkbutton(master, text='Ana', variable=self.ana_duty).pack(pady=5, anchor=W)
        Checkbutton(master, text='Elisabeth', variable=self.eliz_duty).pack(pady=5, anchor=W)
        Checkbutton(master, text='Marc', variable=self.marc_duty).pack(pady=5, anchor=W)

        # Generate monitoring buttons
        Label(master, text=' ').pack(pady=5)
        Button(master, text='Select Folder', command=self.select_path).pack(anchor=S+W)
        Button(master, text='Start Monitoring', command=self.start_watchdog).pack(anchor=S+W)
        Button(master, text='Stop Monitoring', command=self.stop_watchdog).pack(anchor=S+W)
        Button(master, text='Exit', command=root.destroy).pack(anchor=S+W)
        frm.pack(fill=Y, expand=1)
        
    def start_watchdog(self):
        if not self.watch_path:
            self.select_path()
            
        if self.watchdog is None:
            self.watchdog = Watchdog(path=self.watch_path, patterns="*.tiff", logfunc=self.log)
            self.watchdog.start()
            self.log('Watchdog started')
        else:
            self.log('Watchdog already started')


    def stop_watchdog(self):
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log('Watchdog stopped')
        else:
            self.log('Watchdog is not running')

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.watch_path = path
            self.log(f'Selected path: {path}')
        
    def log(self, message):
        showinfo(root, message=f'{message}\n')
                 
        
def get_focus_index(imgpath):
    print("Reading: " + imgpath)
    items = imgpath.split("/")
    imgname = items[-1]
    basepath = "/".join(items[:-1]) + "/"

    # Calculate focus index as in Xu et al. 2017
    img = io.imread(imgpath)
    smooth_short = gaussian(img, sigma=2)
    smooth_long  = gaussian(img, sigma=4)
    pixwise_dif = smooth_short - smooth_long
    focus_index = np.sum(np.sqrt(np.square(pixwise_dif))) / img.size

    # Write it to a file
    f = open(basepath + "focus_idxs.csv", "a+")
    f.write(imgname + "\t" + str(focus_index) + "\n")
    f.close()
    
    

    
class PlotsFrame:
    def __init__(self, master):
        frm = Frame(master)
        frm.pack()
        self.focus_index = np.random.normal(0.34, 0.1, 3000)
        plt.hist(focus_index)
        plt.show()
    

lf = LeftFrame(root)
root.mainloop()
