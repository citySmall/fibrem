#!/usr/bin/env python3
import matplotlib
#import matplotlib.animation as animation
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib import style
style.use('ggplot')
import numpy as np
import os
import pandas as pd
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
    def __init__(self, path='.', patterns="*" ,logfunc=print ,*args, **kwargs):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)
        self.log = logfunc

    def on_created(self, event):
        # This function is called when a file is created
        # We sleep to allow time for the file to be created
        if event.src_path.split(".")[-1] == "tiff":
            time.sleep(5)
            ImgProcessor(event.src_path).get_focus_index()
        
    def on_deleted(self, event):
        # This function is called when a file is deleted
        self.log(f"Someone deleted {event.src_path}!")

    def on_moved(self, event):
        # This function is called when a file is moved    
        self.log(f"Someone moved {event.src_path} to {event.dest_path}")

        
class LeftFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Watchdog status
        self.watchdog = None
        self.watch_path = None
    
        # People init Off-duty 
        self.ana_duty = tk.IntVar(0)
        self.eliz_duty = tk.IntVar(0)
        self.marc_duty = tk.IntVar(0)

        # Generate checkbuttons
        self.lbl1 = tk.Label(self, text='Select people to notify: ').pack(padx=5, pady=5,  anchor=tk.W)
        self.cbtn1 = tk.Checkbutton(self, text='Ana', variable=self.ana_duty).pack(pady=5, anchor=tk.W)
        self.cbtn2 = tk.Checkbutton(self, text='Elizabeth', variable=self.eliz_duty).pack(pady=5, anchor=tk.W)
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

    def log(self, message):
        showinfo(root, message=f'{message}\n')
        
class ImgProcessor:
    focus_idxs = []        
    def __init__(self, path, *args, **kargs):
        self.imgpath = path
        
    def get_focus_index(self):
        
        print("Reading: " + self.imgpath)
        self.items = self.imgpath.split("/")
        self.imgname = self.items[-1]
        self.basepath = "/".join(self.items[:-1]) + "/"

        # Calculate focus index as in Xu et al. 2017
        self.img = io.imread(self.imgpath)
        self.smooth_short = gaussian(self.img, sigma=2)
        self.smooth_long  = gaussian(self.img, sigma=4)
        self.pixwise_dif = self.smooth_short - self.smooth_long
        self.focus_index = np.sum(np.sqrt(np.square(self.pixwise_dif))) / self.img.size
        ImgProcessor.update_idxs_list(self.imgname, self.focus_index)
        
        # Backup to a file a update the plot
        f = open(self.basepath + "focus_idxs.csv", "a+")
        f.write(self.imgname + "," + str(self.focus_index) + "\n")
        f.flush()
        f.seek(0)

        # Read contents to update the plot
        PlotsFrame.create_plot(f)
        f.close()
    
    @staticmethod    
    def update_idxs_list(img, idx):    
        # Keep in memory for detection 
        if len(ImgProcessor.focus_idxs) < 100:
            ImgProcessor.focus_idxs.append((img, idx))
        else: 
            ImgProcessor.focus_idxs.clear()
            ImgProcessor.focus_idxs.append((img, idx))
            
        print(ImgProcessor.focus_idxs[-5:])    
        
        
class PlotsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.lbl1 = tk.Label(self, text='Vital constants plots').pack(pady=5)
        self.widget = None
        self.toolbar = None
        

    def create_plot(self, fhandle):

        # remove old widgets
        if self.widget:
            self.widget.destroy()

        if self.toolbar:
            self.toolbar.destroy()

        # Prepare the plot
        plt = Figure(figsize=(4, 4), dpi=100)
        a = plt.add_subplot(211)
        a.set_ylabel("Focus Index (a.u.)")
        a.set_title("Focus index evolution")

        # Parse data
        data = fhandle.read().split('\n')
        xar=[]
        yar=[]
        
        for line in data:
            if len(line)>1:
                x,y = line.split(',')
                xar.append(str(x))
                yar.append(int(y))
                
        a.plot(xar,yar)        
        
        canvas = FigureCanvasTkAgg(plt, self)

        self.toolbar = NavigationToolbar2Tk(canvas, self)
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)


        

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.left_frame = LeftFrame(self)
        self.plots_frame = PlotsFrame(self)
        
        self.left_frame.pack(side="left", fill="y")
        self.plots_frame.pack(side="right", fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.title('FibRem: Sleeping aid for EM microscopists')
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
