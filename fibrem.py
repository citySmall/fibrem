#!/usr/bin/env python3
import matplotlib
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
import os
import pdb
import time
from skimage.filters import gaussian
from skimage import io
import tkinter as tk 
from tkinter import filedialog
from tkinter.messagebox import showinfo
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

        
class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path='.', patterns="*" ,*args, **kwargs):
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

        
class LeftFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg="red" ,*args, **kwargs)
        self.parent = parent

        # Watchdog status
        self.watchdog = None
        self.watch_path = None
    
        # People init Off-duty 
        self.ana_duty = tk.IntVar(0)
        self.eliz_duty = tk.IntVar(0)
        self.marc_duty = tk.IntVar(0)

        # Generate checkbuttons
        self.lbl1 = tk.Label(self, text='Select people to notify: ').pack(pady=5,  anchor=tk.W)
        self.cbtn1 = tk.Checkbutton(self, text='Ana', variable=self.ana_duty).pack(pady=5, anchor=tk.W)
        self.cbtn2 = tk.Checkbutton(self, text='Elisabeth', variable=self.eliz_duty).pack(pady=5, anchor=tk.W)
        self.cbtn3 = tk.Checkbutton(self, text='Marc', variable=self.marc_duty).pack(pady=5, anchor=tk.W)

        # Generate monitoring buttons
        self.lbl2 = tk.Label(self, text=' ').pack(pady=5)
        self.btn4 = tk.Button(self, text='Select Folder', command=self.select_path).pack(anchor=tk.S+tk.W)
        self.btn5 = tk.Button(self, text='Start Monitoring', command=self.start_watchdog).pack(anchor=tk.S+tk.W)
        self.btn6 = tk.Button(self, text='Stop Monitoring', command=self.stop_watchdog).pack(anchor=tk.S+tk.W)
        self.btn7 = tk.Button(self, text='Exit', command=root.destroy).pack(anchor=tk.S+tk.W)
    
        
    def start_watchdog(self):
        if not self.watch_path:
            self.select_path()
            
        if self.watchdog is None:
            self.watchdog = Watchdog(path=self.watch_path, patterns="*.tiff")
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
    
        
class PlotsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.lbl1 = tk.Label(self, text='Vital constants plots').pack(pady=5)

        fig = Figure(figsize=(10, 8), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack()

        
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.left_frame = LeftFrame(self)
        self.plots_frame = PlotsFrame(self)
        
        self.left_frame.pack(side="left", fill="y")
        self.plots_frame.pack(side="right", fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.title('FibRem: Seeping aid for EM microscopists')
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
