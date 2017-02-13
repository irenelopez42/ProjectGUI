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

nlep_val = IntVar()
nlep_val.set(0) # initialize a string for number of leptons

b1_lep = Radiobutton(frame1, text="1 Lepton",
                        variable=nlep_val, value=1)
b2_lep = Radiobutton(frame1, text="2 Leptons",
                        variable=nlep_val, value=2)
b3_lep = Radiobutton(frame1, text="3 Leptons",
                        variable=nlep_val, value=3)
b4_lep = Radiobutton(frame1, text="4 Leptons",
                        variable=nlep_val, value=4)

st_lepcb = IntVar() #State of checkbox
def chooseNlep(): #function for checkbox
    if st_lepcb.get()==1:
	b1_lep.grid(row=1)
	b2_lep.grid(row=2)
	b3_lep.grid(row=3)
	b4_lep.grid(row=4)
    else:
	nlep_val.set(0)
        b1_lep.grid_forget()
	b2_lep.grid_forget()
	b3_lep.grid_forget()
	b4_lep.grid_forget()

lyes = Checkbutton(frame1, text="Choose number leptons", font=("Calibri",10),bg="LightCyan2",
	variable = st_lepcb, onvalue=1,offvalue=0, command=chooseNlep)
lyes.grid(row=0,column=0, sticky=W) #Define and show checkbox


#Want specific number jets? Enter number.

njet_val = IntVar()
njet_val.set(0) # initialize a string for number of jets

b1_jet = Radiobutton(frame1, text="1 Jet",
                        variable=njet_val, value=1)
b2_jet = Radiobutton(frame1, text="2 Jets",
                        variable=njet_val, value=2)
b3_jet = Radiobutton(frame1, text="3 Jets",
                        variable=njet_val, value=3)
b4_jet = Radiobutton(frame1, text="4 Jets",
                        variable=njet_val, value=4)
b5_jet = Radiobutton(frame1, text="5 Jets",
                        variable=njet_val, value=5)
b6_jet = Radiobutton(frame1, text="6 Jets",
                        variable=njet_val, value=6)

st_jetcb = IntVar() #State of checkbox
def chooseNjet(): #Function for checkbox
    if st_jetcb.get()==1:
	b1_jet.grid(row=7)
	b2_jet.grid(row=8)
	b3_jet.grid(row=9)
	b4_jet.grid(row=10)
	b5_jet.grid(row=11)
	b6_jet.grid(row=12)
    else:
	njet_val.set(0)
        b1_jet.grid_forget()
	b2_jet.grid_forget()
	b3_jet.grid_forget()
	b4_jet.grid_forget()
	b5_jet.grid_forget()
	b6_jet.grid_forget()

jyes = Checkbutton(frame1, text="Choose number jets", bg="LightCyan2", font=("Calibri",10),
	 variable = st_jetcb, onvalue=1,offvalue=0, command=chooseNjet)
jyes.grid(row=6,column=0, sticky=W) #Define and show checkbox

#Want to select min W transverse mass?

slider_WTmass = Scale(frame1, from_=0, to=100, orient=HORIZONTAL, length=150) #Define slider

st_WTmasscb= IntVar() #Checkbutton state
def chooseWTmass():  #Function for checkbutton
    if st_WTmasscb.get()==1:
        slider_WTmass.grid(row=14, column=0) #If state 1, show slider
    else:
        slider_WTmass.grid_forget()

WTmassyes = Checkbutton(frame1, text="Choose minimum\n W transverse mass (GeV)", font=("Calibri",10), bg="LightCyan2", 
	variable = st_WTmasscb, onvalue=1,offvalue=0, command=chooseWTmass)
WTmassyes.grid(row=13,column=0, sticky=W) #Define and show checkbutton

#Slider for missing momentum

slider_missP = Scale(frame1, from_=0, to=100, orient=HORIZONTAL, length=150) #Define slider

st_missPcb= IntVar() #Checkbutton state
def choosemissP():  #Function for checkbutton
    if st_missPcb.get()==1:
        slider_missP.grid(row=16, column=0) #If state 1, show slider
    else:
        slider_missP.grid_forget()

missPyes = Checkbutton(frame1, text="Minimum missing\n transverse momentum (Gev)", font=("Calibri",10), bg="LightCyan2", 
	variable = st_missPcb, onvalue=1,offvalue=0, command=choosemissP)
missPyes.grid(row=15,column=0, sticky=W) #Define and show checkbutton

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

rbrowser = Button(frame1, text="Root Browser", font=("Calibri", 10) ,bg="Blue", 
             activebackground="Black", fg= "White",activeforeground="White", command=browser)
rbrowser.grid(row=17)


#Button to start analysis
run = Button(frame1, text="Run Analysis", font=("Calibri",16) ,bg="Green", 
             activebackground="Black", fg= "White", activeforeground="White")
run.grid(row=18, columnspan=2, sticky=S)


window.mainloop()
