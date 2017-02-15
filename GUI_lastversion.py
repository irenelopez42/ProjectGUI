# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:25:40 2017

@author: Irene
"""

import ROOT
from Tkinter import * 
import threading
import CheckFileSuper
import NewRunScript
import NewPlotResults

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
btag_val = IntVar()
btag_entry = Spinbox(frame1, textvariable=btag_val, from_=0, to=6, width=4) #Entry for number of b-tagged jets

def Nbtagjet(): #function that will show the entry when checkbox clicked
	if st_btagjetcb.get() ==1:
		btag_entry.grid(row=13, column=1)
	else:
		btag_entry.grid_forget()
		btag_val.set(0)

st_btagjetcb = IntVar()
btaggedyes = Checkbutton(frame1, text="Any b-tagged jets?", bg="LightCyan2",
	 variable = st_btagjetcb, onvalue=1,offvalue=0, command=Nbtagjet) #Extra checkbox for b-tagged jets

st_jetcb = IntVar() #State of checkbox
def chooseNjet(): #Function for checkbox
    if st_jetcb.get()==1:
	b1_jet.grid(row=7)
	b2_jet.grid(row=8)
	b3_jet.grid(row=9)
	b4_jet.grid(row=10)
	b5_jet.grid(row=11)
	b6_jet.grid(row=12)
	btaggedyes.grid(row=13)
    else:
	njet_val.set(0)
        b1_jet.grid_forget()
	b2_jet.grid_forget()
	b3_jet.grid_forget()
	b4_jet.grid_forget()
	b5_jet.grid_forget()
	b6_jet.grid_forget()
	btaggedyes.grid_forget()
	st_btagjetcb.set(0)
	btag_val.set(0)
	btag_entry.grid_forget()

jyes = Checkbutton(frame1, text="Choose number jets", bg="LightCyan2", font=("Calibri",10),
	 variable = st_jetcb, onvalue=1,offvalue=0, command=chooseNjet)
jyes.grid(row=6,column=0, sticky=W) #Define and show checkbox

#Want to select min W transverse mass?

slider_WTmass = Scale(frame1, from_=0, to=100, orient=HORIZONTAL, length=150) #Define slider

st_WTmasscb= IntVar() #Checkbutton state
def chooseWTmass():  #Function for checkbutton
    if st_WTmasscb.get()==1:
        slider_WTmass.grid(row=15, column=0) #If state 1, show slider
    else:
        slider_WTmass.grid_forget()

WTmassyes = Checkbutton(frame1, text="Choose minimum\n W transverse mass (GeV)", font=("Calibri",10), bg="LightCyan2", 
	variable = st_WTmasscb, onvalue=1,offvalue=0, command=chooseWTmass)
WTmassyes.grid(row=14,column=0, sticky=W) #Define and show checkbutton

#Slider for missing momentum



missE_val = IntVar()
missE_val.set(0)

slider_missP = Scale(frame1, from_=0, to=100, orient=HORIZONTAL, length=150, variable = missE_val) #Define slider

st_missPcb= IntVar() #Checkbutton state
def choosemissP():  #Function for checkbutton
    if st_missPcb.get()==1:
        slider_missP.grid(row=17, column=0) #If state 1, show slider
    else:
        slider_missP.grid_forget()
        missE_val.set(0)

missPyes = Checkbutton(frame1, text="Minimum missing\n transverse momentum (GeV)", font=("Calibri",10), bg="LightCyan2", 
	variable = st_missPcb, onvalue=1,offvalue=0, command=choosemissP)
missPyes.grid(row=16,column=0, sticky=W) #Define and show checkbutton

#Button to open root browser

latestThread=None # last opened thread
b= None

class browser_thread(threading.Thread):
    """thread for opening a TBrowser"""
    
    def __init__(self):
        self.exit = threading.Event()
        threading.Thread.__init__(self)

        
    def run(self):
        global b
        b=ROOT.TBrowser()
        while not self.exit.is_set():
            continue

        
    def shutdown(self):
        self.exit.set()


def browser():
    """creates new browser_thread closing
    the previous one"""    
    
    global b
    global latestThread
    if latestThread!= None:
        latestThread.shutdown()
       # b.Destructor()  
    latestThread =browser_thread()
    latestThread.setDaemon(True)
    latestThread.start()

rbrowser = Button(frame1, text="Root Browser", font=("Calibri", 10) ,bg="Blue", 
             activebackground="Black", fg= "White",activeforeground="White", command=browser)
rbrowser.grid(row=18)

histograms =[]


def run_analysis():
    """runs the analysis"""
    
    global latestThread
    if latestThread!= None:
        latestThread.shutdown()
        latestThread=None
        
    selection = []
    global histograms
    
    histograms.append("n_jets")
    histograms.append("lep_n")
    histograms.append("etmiss")
    
    
    
    if njet_val.get() != 0:
        print njet_val.get()
        print "test"
        jetn_chk = CheckFileSuper.CheckNJets(njet_val.get())
        selection.append(jetn_chk)
        
        histograms.append("jet_pt")
        histograms.append("jet_m")
        histograms.append("jet_jvf")
        histograms.append("jet_eta")
        histograms.append("jet_MV1")
        
        if st_btagjetcb.get()==1:
            btag_chk = CheckFileSuper.CheckBTag(btag_val.get())
            selection.append(btag_chk)
            
    if nlep_val.get() != 0:
        lepn_chk = CheckFileSuper.CheckNLep(nlep_val.get())
        selection.append(lepn_chk)
        
        histograms.append("lep_pt")
        histograms.append("lep_eta")
        histograms.append("lep_phi")
        histograms.append("lep_E")
        histograms.append("lep_charge")
        histograms.append("lep_type")

        histograms.append("leadlep_pt")
        histograms.append("leadlep_eta")
        histograms.append("leadlep_phi")
        histograms.append("leadlep_E")
        histograms.append("leadlep_charge")
        histograms.append("leadlep_type")  
        
        if nlep_val.get()>1:
            histograms.append("traillep_pt")
            histograms.append("traillep_eta")
            histograms.append("traillep_E")
            histograms.append("traillep_phi")
            histograms.append("traillep_charge")
            histograms.append("traillep_type")
    
    if st_missPcb.get()==1:
        missE_chk = CheckFileSuper.CheckEtMiss(missE_val.get())
        selection.append(missE_chk)
     
    NewRunScript.run(selection,histograms)
    ROOT.gApplication.Terminate(0) 
 
def plotting():
    global histograms
    if histograms == []:
        return
    NewPlotResults.plot_results(histograms)   
    
plot = Button(frame1, text="Plot Results", font=("Calibri", 10) ,bg="Blue", 
             activebackground="Black", fg= "White",activeforeground="White", command=plotting)
plot.grid(row=20)




#Button to start analysis
run = Button(frame1, text="Run Analysis", font=("Calibri",16) ,bg="Green", 
             activebackground="Black", fg= "White", activeforeground="White",command  = run_analysis)
run.grid(row=19, columnspan=2, sticky=S)

    
    
    
    


window.mainloop()
