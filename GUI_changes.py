# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:25:40 2017

@author: Irene
"""

import ROOT
from Tkinter import * 
import threading

window = Tk()

#Define a drop down menu in case we need it
menu = Menu(window)
window.config(menu=menu)
submenu = Menu(menu)
menu.add_cascade(label="File", menu=submenu)

#Create invisible frames to organize layout
frame1 = Frame(window, width="30", padx=25, height="450") #where widgets will be
frame1.pack(side=LEFT)
frameOUT = Frame(window, width="500", height="450", bg="thistle4") #where plots will show
frameOUT.pack(side=LEFT)

#Widgets:
    
#Want specific number of lepton? Enter number.
wantlep = Label(frame1, text="Choose number leptons:", bg="LightCyan2", 
                relief=RAISED, font=("Calibri",11))
wantlep.grid(sticky=W)

def test():
    print "test"

# create a popup menu
menu = Menu(window, tearoff=0)
menu.add_command(label="1", command=test)
menu.add_command(label="2", command=test)
menu.add_command(label="3", command=test)
menu.add_command(label="4", command=test)
menu.add_command(label="5", command=test)
menu.add_command(label="6", command=test)

nlep = Label(frame1, text ="Select", bg="Cyan")
def popup(event):
    menu.post(event.x_root, event.y_root)
nlep.bind("<Button-1>", popup)

st_lepcb = IntVar()
def chooseNlep():
    if st_lepcb.get()==1:
	nlep.grid(row=1,column=0, sticky=E)
    else:
        nlep.grid_forget()
lyes = Checkbutton(frame1, variable = st_lepcb, onvalue=1,offvalue=0, command=chooseNlep)
lyes.grid(row=0,column=1, sticky=W)

#Want specific number jets? Enter number.
wantjet = Label(frame1, text="Choose number jets:", bg="LightCyan2",
                relief=RAISED, font=("Calibri",11))
wantjet.grid(row=2, sticky=W)
njet = Label(frame1, text="Number of jets:")
entrynjet = Entry(frame1, width=5)
st_jetcb= IntVar()
def chooseNjet():
    if st_jetcb.get()==1:
        njet.grid(row=3)
        entrynjet.grid(row=3, column=1)
    else:
        njet.grid_forget()
        entrynjet.grid_forget()
jyes = Checkbutton(frame1, variable = st_jetcb, onvalue=1,offvalue=0, command=chooseNjet)
jyes.grid(row=2,column=1, sticky=W)

#Want to select min W transverse mass?
wantWTmass = Label(frame1, text="Choose minimum\n W transverse mass (GeV):", bg="LightCyan2",
                relief=RAISED, font=("Calibri",11))
wantWTmass.grid(row=4, sticky=W)
slider_WTmass = Scale(frame1, from_=0, to=100, orient=HORIZONTAL, length=150)
st_WTmasscb= IntVar()
def chooseWTmass():
    if st_WTmasscb.get()==1:
        slider_WTmass.grid(row=5, column=0)
    else:
        slider_WTmass.grid_forget()
WTmassyes = Checkbutton(frame1, variable = st_WTmasscb, onvalue=1,offvalue=0, command=chooseWTmass)
WTmassyes.grid(row=4,column=1, sticky=W)

#Slider for missing momentum
missp = Label(frame1, text="Minimum missing\n transverse momentum (Gev):",
              font=("Calibri",11), justify=LEFT, relief=RAISED, bg="LightCyan2")
missp.grid(row=6, columnspan=2,sticky=W)
misspnum = Scale(frame1, from_=0, to=100, orient=HORIZONTAL, length=150)
misspnum.grid(row=7, columnspan=2)

#Button to open root browser

latestThread=None # last opened thread

class browser_thread(threading.Thread):
    """thread for opening a TBrowser"""
    
    def __init__(self):
        self.exit = threading.Event()
        threading.Thread.__init__(self)

        
    def run(self):
        b= ROOT.TBrowser()
        while not self.exit.is_set():
            continue
        
    def shutdown(self):
        self.exit.set()


def browser():
    """creates new browser_thread closing
    the previous one"""    
    
    global latestThread
    if latestThread!= None:
        latestThread.shutdown()
    latestThread =browser_thread()
    latestThread.setDaemon(True)
    latestThread.start()

rbrowser = Button(frame1, text="Root Browser", font=("Calibri", 11) ,bg="Blue", 
             activebackground="Black", fg= "White",activeforeground="White", command=browser)
rbrowser.grid(row=12)


#Button to start analysis
run = Button(frame1, text="Run Analysis", font=("Calibri",16) ,bg="Green", 
             activebackground="Black", fg= "White", activeforeground="White")
run.grid(row=13, columnspan=2, sticky=S)

window.mainloop()
