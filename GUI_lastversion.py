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
import glob
import os

window = Tk()

#Define a drop down menu in case we need it
menu = Menu(window)
window.config(menu=menu)
submenu = Menu(menu)
menu.add_cascade(label="File", menu=submenu)

#Create invisible frames to organize layout
frame1 = Frame(window, width="300", padx=25, height="450") #where widgets will be
frame1.pack(side=LEFT)
frameOUT = Frame(window, width="500", height="450", bg="thistle4") #where plots will show
frameOUT.pack(side=LEFT)

#Widgets:
    
#Want specific number of lepton? Enter number.

nlep_val = IntVar()
nlep_val.set(0) # initialize a string for number of leptons


OptionsLep = Frame(frame1) #Frame to share extra options for leptons

#initialize values for extra options
LepMom_val = IntVar()
LepMom_val.set(0)    #Lepton momentum
LepTmass_val = IntVar()
LepTmass_val.set(0)  #Lepton transverse mass
st_lepchargecb = IntVar()
TwoLepcharge_val = IntVar()
TwoLepcharge_val.set(1) #2 Leptons: same/diferent charge
st_lepflavourcb = IntVar()
TwoLepflavour_val = IntVar()
TwoLepflavour_val.set(1)  #2 Leptons: same/diferent flavour
angleLepMP_val = IntVar()
angleLepMP_val.set(0)  #Angle between miss momentum and lepton
LeadLepMom_val = IntVar()
LeadLepMom_val.set(0)    #Lead Lepton momentum
TrailLepMom_val = IntVar()
TrailLepMom_val.set(0)    #Trail Lepton momentum


b1_LepCharge = Radiobutton(OptionsLep, text="Same charge",
                        variable=TwoLepcharge_val, value=1)
b2_LepCharge = Radiobutton(OptionsLep, text="Opposite charge",
                        variable=TwoLepcharge_val, value=-1)  #Checkboxes for same/opposite charge

def chooseLepcharge():
    TwoLepcharge_val = IntVar()
    TwoLepcharge_val.set(1)
    if  st_lepchargecb.get() == 1:
        b1_LepCharge.grid(row=1, sticky=W)
        b2_LepCharge.grid(row=2, sticky=W)
    else:
        b1_LepCharge.grid_forget()
        b2_LepCharge.grid_forget()
        del TwoLepcharge_val

b1_LepFlavour = Radiobutton(OptionsLep, text="Same flavour",
                        variable=TwoLepflavour_val, value=1)
b2_LepFlavour = Radiobutton(OptionsLep, text="Different flavour",
                        variable=TwoLepflavour_val, value=-1)  #Checkboxes for same/diferent flavour

def chooseLepflavour():
    TwoLepflavour_val = IntVar()
    TwoLepflavour_val.set(1)
    if  st_lepflavourcb.get() == 1:
        b1_LepFlavour.grid(row=4, sticky=W)
        b2_LepFlavour.grid(row=5, sticky=W)
    else:
        b1_LepFlavour.grid_forget()
        b2_LepFlavour.grid_forget()
        del TwoLepflavour_val


slider_LepMom = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL,
			length=125, width=10, variable = LepMom_val, bg = "lavender",label="Momentum") #Slider for momentum
slider_LepTMass = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL, 
			length=125, width=10, variable = LepTmass_val, bg = "lavender",label="Transverse mass") #slider for transverse mass
chooseLepchargecb = Checkbutton(OptionsLep, text="Choose leptons' charges", bg ="lavender", variable = st_lepchargecb, onvalue=1,offvalue=0, 				command=chooseLepcharge)
chooseLepflavourcb = Checkbutton(OptionsLep, text="Choose leptons' flavours", bg = "lavender", variable = st_lepflavourcb, onvalue=1,offvalue=0, command=chooseLepflavour)
slider_angleLepMP = Scale(OptionsLep, from_=0, to=180, orient=HORIZONTAL, 
			length=170, width=10, variable = angleLepMP_val, bg = "lavender", label="θ between lep and miss P") #slider for angle
slider_LeadLepMom = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL,
			length=170, width=10, variable = LeadLepMom_val, bg = "lavender",label="Lead Lepton Momentum") #Slider for lead lepton momentum
slider_TrailLepMom = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL,
			length=170, width=10, variable = TrailLepMom_val, bg = "lavender",label="Trail Lepton Momentum") #Slider for trail lepton momentum

def clearFrame():    #function to clear all extra options
    OptionsLep.grid_forget()
    slider_LepMom.grid_forget()
    slider_LepTMass.grid_forget()
    chooseLepchargecb.grid_forget()
    chooseLepflavourcb.grid_forget()
    slider_angleLepMP.grid_forget()
    slider_LeadLepMom.grid_forget()
    slider_TrailLepMom.grid_forget()
    LepMom_val.set(0)
    LepTmass_val.set(0)
    TwoLepflavour_val.set(1)
    angleLepMP_val.set(0)
    TrailLepMom_val.set(0)
    LeadLepMom_val.set(0)

def extLepOpts():
    if nlep_val.get() == 1:
        clearFrame()
        OptionsLep.grid(row=1, column=2)
        slider_LepMom.grid(row=0)
        slider_LepTMass.grid(row=1)
    if nlep_val.get() == 2:
        clearFrame()
        OptionsLep.grid(row=2, column=2)
        chooseLepchargecb.grid(row=0)
        chooseLepflavourcb.grid(row=3)
        slider_angleLepMP.grid(row=6, sticky=W)
        slider_LeadLepMom.grid(row=7, sticky=W)
        slider_TrailLepMom.grid(row=8, sticky=W)

    if nlep_val.get() == 3:
        clearFrame()
        OptionsLep.grid(row=3, column=2)
    if nlep_val.get() == 4:
        clearFrame()
        OptionsLep.grid(row=4, column=2)

b1_lep = Radiobutton(frame1, text="1 Lepton",
                        variable=nlep_val, value=1, command=extLepOpts)
b2_lep = Radiobutton(frame1, text="2 Leptons",
                        variable=nlep_val, value=2, command=extLepOpts)
b3_lep = Radiobutton(frame1, text="3 Leptons",
                        variable=nlep_val, value=3, command=extLepOpts)
b4_lep = Radiobutton(frame1, text="4 Leptons",
                        variable=nlep_val, value=4, command=extLepOpts)

st_lepcb = IntVar() #State of checkbox
def chooseNlep(): #function for checkbox
    if st_lepcb.get()==1:
	b1_lep.grid(row=1)
	b2_lep.grid(row=2)
	b3_lep.grid(row=3)
	b4_lep.grid(row=4)
    else:
	nlep_val.set(0)
        clearFrame()
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


## Fuction for analysis

histograms =[]

def run_analysis():
    """runs the analysis"""
    del histograms[:]
    
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
    del listphotos[:]
    del listphotosbig[:]
    del listcommands[:]
    del listbuttons[:]
    del listlabels[:]
    previousplots=glob.glob('Output/*.png')
    for i in range(0, len(previousplots)): 
    	os.remove(previousplots[i])
    global histograms
    if histograms == []:
        return
    NewPlotResults.plot_results(histograms)
    plots = glob.glob('Output/*.png')
    lplots = len(plots)
    try:
	    for j in range(0, 6):
		    for i in range(0,6):
			    photo = PhotoImage(file= plots[i+j*6])
			    listphotosbig.insert(i+j*6, photo)
			    photo2 = photo.subsample(9)
			    listphotos.insert(i+j*6, photo2)
			    def showplot(p=i,q=j):
				    newwin = Toplevel()
				    bigplot = Label(newwin, compound=BOTTOM,text = plots[p+q*6][7:][:-4], image = listphotosbig[p+q*6])
				    bigplot.grid()
			    listcommands.insert(i+j*6, showplot)
			    listbuttons.insert(i+j*6, Button(frameOUT, command=listcommands[i+j*6], compound=BOTTOM, text=plots[i+j*6][7:][:-4], image=listphotos[i+j*6]))
			    listbuttons[i+j*6].grid(row=j, column=i)

    except IndexError:
	    pass


#Button to plot results

listphotos = [] #some lists needed
listphotosbig = []
listcommands = []
listbuttons = []
listlabels = []
    
plot = Button(frame1, text="Plot Results", font=("Calibri", 10) ,bg="Blue", 
             activebackground="Black", fg= "White",activeforeground="White", command=plotting)
plot.grid(row=20)




#Button to start analysis
run = Button(frame1, text="Run Analysis", font=("Calibri",16) ,bg="Green", 
             activebackground="Black", fg= "White", activeforeground="White", command = run_analysis)
run.grid(row=19, columnspan=2, sticky=S)


window.mainloop()
