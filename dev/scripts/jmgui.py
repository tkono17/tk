#!/usr/bin/env python

from Tkinter import *

class JobSummaryPanel:
    def __init__(self, parent):
        self.panel = Frame(parent)
        self.panel.pack()
        title = Label(self.panel, text='Job list')
        title.pack()
        update_button = Button(self.panel, text='Update')
        update_button.pack()
    def frame(self):
        return self.panel
        
class JobTrackingPanel:
    def __init__(self, parent):
        self.panel = Frame(parent)
        self.panel.pack()
        title = Label(self.panel, text='Job list')
        title.pack()
    def frame(self):
        return self.panel

class JMApp:
    def __init__(self, parent):
        panel = JobSummaryPanel(parent)
        panel.frame().pack(side=LEFT)
        panel = JobTrackingPanel(parent)
        panel.frame().pack(side=LEFT)
        
if __name__ == '__main__':
    root = Tk()
    app = JMApp(root)
    root.mainloop()
