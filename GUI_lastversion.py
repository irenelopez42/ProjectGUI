# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:25:40 2017

@author: Irene
"""

import ROOT
from Tkinter import * 
import tkMessageBox
import threading
import CheckFileSuper
import NewRunScript
import NewPlotResults
import NewAnalysisHelpers as AH
import glob
import os
import CustomConfiguration
import NewJob
import ttk
import multiprocessing

window = Tk()
window.wm_title("Event Analyser") #GUI Name

#Define a drop down menu in case we need it
#menu = Menu(window)
#window.config(menu=menu)
#submenu = Menu(menu)
#menu.add_cascade(label="More", menu=submenu)

#Canvas and scrollbar

scrollbar = Scrollbar(window)
canvas = Canvas(window, width=460, height=700, yscrollcommand=scrollbar.set, scrollregion=(0,0,0,890))
canvas.pack(side=LEFT)
scrollbar.pack(side=LEFT, fill=Y)
scrollbar.config(command=canvas.yview)

#Create invisible frames to organize layout
frame1 = Frame(window, width="200", padx=10) #where widgets will be
canvas.create_window(230,440, window=frame1)
frameOUT = Frame(window, width="812", height="700", bg="thistle4") #where plots will show
frameOUT.pack(side=LEFT, fill=BOTH, expand=1)
frameOUT.grid_rowconfigure(0, minsize=83, weight=1)
frameOUT.grid_rowconfigure(6, minsize=83, weight=1)
frameOUT.grid_columnconfigure(0, minsize=50, weight=1)
frameOUT.grid_columnconfigure(6, minsize=50, weight=1) #These will make the plots appear centered

##Physicist on corner
physicist = PhotoImage(file="physicist.png")
physCanvas = Canvas(frameOUT, width=90, height=87)
physCanvas.place(relx=1, rely=1, anchor=SE)
physCanvas.create_image(46,44, image=physicist)

questionmark = PhotoImage(file="questionmark2.png") #define photo for the question marks with info

#Widgets:
    
#Want specific number of lepton? Enter number.

nlep_val = IntVar()
nlep_val.set(0) # initialize a string for number of leptons

OptionsLep = Frame(frame1) #Frame to share extra options for leptons

#initialize values for extra options
LepTmass_val = IntVar()
LepTmass_val.set(0)  #Lepton min transverse mass
LepTmassMax_val = IntVar()
LepTmassMax_val.set(0)  #Lepton max transverse mass
st_lepchargecb = IntVar()
TwoLepcharge_val = IntVar()
TwoLepcharge_val.set(1) #2 Leptons: same/diferent charge
st_lepflavourcb = IntVar()
st_InvMasscb = IntVar()
TwoLepflavour_val = IntVar()
TwoLepflavour_val.set(1)  #2 Leptons: same/diferent flavour
InvariantM_val = IntVar()
InvariantM_val.set(0)    #Invariant mass
InvariantM2_val = IntVar()
InvariantM2_val.set(0)    #Invariant mass
Range_val = IntVar()
Range_val.set(0)    #Range of invariant mass

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

def validate(action, index, value_if_allowed, prior_value, text, 
             validation_type, trigger_type, widget_name):
    if text in '0123456789+':
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False

vcmd = (window.register(validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
emptyf = Frame(OptionsLep)
entry_InvariantM = Entry(emptyf, textvariable=InvariantM_val, validate='key', 
                         vcmd=vcmd, width=3)
entry_Range = Entry(emptyf, textvariable=Range_val, validate='key', 
                    vcmd=vcmd, width=3)
plusminus = Label(emptyf, text="±")

def chooseInvMass():
    if st_InvMasscb.get() == 1:
	emptyf.grid(row=8)
	entry_InvariantM.pack(side=LEFT)
	plusminus.pack(side=LEFT)
	entry_Range.pack(side=LEFT)
    else:
	emptyf.grid_forget()
	entry_InvariantM.pack_forget()
	plusminus.pack_forget()
	entry_Range.pack_forget()
	InvariantM_val.set(0)
        Range_val.set(0)

slider_LepTMass = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL, 
			length=170, width=10, variable = LepTmass_val, bg = "lavender",label="Minimum transverse mass") #slider for min transverse mass
slider_maxLepTMass = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL, 
			length=170, width=10, variable = LepTmassMax_val, bg = "lavender",label="Maximum transverse mass") #slider for max transverse mass
chooseLepchargecb = Checkbutton(OptionsLep, text="Leptons' charges", bg ="lavender", variable = st_lepchargecb, onvalue=1,offvalue=0, 				command=chooseLepcharge)
chooseLepflavourcb = Checkbutton(OptionsLep, text="Leptons' flavours", bg = "lavender", variable = st_lepflavourcb, onvalue=1,offvalue=0, command=chooseLepflavour)
chooseInvMass = Checkbutton(OptionsLep, bg="lavender", text="What invariant mass",  
	variable = st_InvMasscb, onvalue=1,offvalue=0, command=chooseInvMass)
LabelInvMass = Label(OptionsLep, bg="lavender")
LabelInvMass2 = Label(OptionsLep, text="Invariant mass of pair 2:", bg="lavender")
entry_InvariantM2 =Entry(OptionsLep, textvariable=InvariantM2_val, validate='key', vcmd=vcmd, width=3) #Entry for invariant mass of 2nd pair (4 leptons case)  
emptyf2 = Frame(OptionsLep, width="170") #just to mantain OptionsLep width

qinvmass = Canvas(OptionsLep, width=16, height=16) 
qinvmass.create_image(8,8, image=questionmark) #Question mark to be next to "invariant mass" option
infoinvmass= Message(OptionsLep, text= "This is the sum of the leptons' rest masses.\nWrite the uncertainty too.",
 bg="White", aspect=300) #Information message
 
def on_enterinvmass(event):
    infoinvmass.grid(row=0, rowspan=8, sticky=SW)
    
def on_leaveinvmass(event):
    infoinvmass.grid_forget()
    
qinvmass.bind("<Enter>", on_enterinvmass)
qinvmass.bind("<Leave>", on_leaveinvmass)  #Def and bind two functions for when cursor is over question mark or leaves

qbinvmass = Canvas(OptionsLep, width=16, height=16) 
qbinvmass.create_image(8,8, image=questionmark) #Question mark to be next to "invariant mass of pair" option
infobinvmass= Message(OptionsLep, text= "Sum of the rest masses of two of these leptons.",
 bg="White", aspect=300) #Information message
 
def on_enterbinvmass(event):
    infobinvmass.grid(row=0, rowspan=8, sticky=SW)
    
def on_leavebinvmass(event):
    infobinvmass.grid_forget()
    
qbinvmass.bind("<Enter>", on_enterbinvmass)
qbinvmass.bind("<Leave>", on_leavebinvmass)  #Def and bind two functions for when cursor is over question mark or leaves

qinvmass2 = Canvas(OptionsLep, width=16, height=16) 
qinvmass2.create_image(8,8, image=questionmark) #Question mark to be next to "invariant mass of pair" option
infoinvmass2= Message(OptionsLep, text= "Sum of the rest masses of the other 2 leptons. Same uncertainty as above",
 bg="White", aspect=300) #Information message
 
def on_enterinvmass2(event):
    infoinvmass2.grid(row=2, rowspan=8, sticky=SW)
    
def on_leaveinvmass2(event):
    infoinvmass2.grid_forget()
qinvmass2.bind("<Enter>", on_enterinvmass2)
qinvmass2.bind("<Leave>", on_leaveinvmass2)  #Def and bind two functions for when cursor is over question mark or leaves

qcharges = Canvas(OptionsLep, width=16, height=16) 
qcharges.create_image(8,8, image=questionmark) #Question mark to be next to "Leptons' charges" option
infocharges= Message(OptionsLep, text= "Within a pair, but not necessarily with others",
 bg="White", aspect=300) #Information message
 
def on_entercharges(event):
    infocharges.grid(row=0, rowspan=8, sticky=N)
    
def on_leavecharges(event):
    infocharges.grid_forget()
    
qcharges.bind("<Enter>", on_entercharges)
qcharges.bind("<Leave>", on_leavecharges)  #Def and bind two functions for when cursor is over question mark or leaves

qflavours = Canvas(OptionsLep, width=16, height=16) 
qflavours.create_image(8,8, image=questionmark) #Question mark to be next to "Flavours' charges" option
infoflavours= Message(OptionsLep, text= "Within a pair, but not necessarily with others",
 bg="White", aspect=300) #Information message
 
def on_enterflavours(event):
    infoflavours.grid(row=3,rowspan=8, sticky=N)
    
def on_leaveflavours(event):
    infoflavours.grid_forget()
    
qflavours.bind("<Enter>", on_enterflavours)
qflavours.bind("<Leave>", on_leaveflavours)  #Def and bind two functions for when cursor is over question mark or leaves

def clearFrame():    #function to clear all extra options
    OptionsLep.grid_forget()
    slider_LepTMass.grid_forget()
    slider_maxLepTMass.grid_forget()
    chooseLepchargecb.grid_forget()
    chooseLepflavourcb.grid_forget()
    chooseInvMass.grid_forget()
    emptyf.grid_forget()
    entry_InvariantM.pack_forget()
    plusminus.pack_forget()
    entry_Range.pack_forget()
    LabelInvMass.grid_forget()
    LabelInvMass2.grid_forget()
    entry_InvariantM2.grid_forget()
    qinvmass.grid_forget()
    qbinvmass.grid_forget()
    qinvmass2.grid_forget()
    qcharges.grid_forget()
    qflavours.grid_forget()
    emptyf2.grid_forget
    LepTmass_val.set(0)
    LepTmassMax_val.set(0)
    st_lepchargecb.set(0)
    st_lepflavourcb.set(0)
    st_InvMasscb.set(0)
    chooseLepcharge()
    chooseLepflavour()
    InvariantM_val.set(0)
    InvariantM2_val.set(0)
    Range_val.set(0)
    chooseLepchargecb.config(text="Leptons' charge")
    chooseLepflavourcb.config(text="Leptons' flavour")

def extLepOpts():
    if nlep_val.get() == 0:
	clearFrame()
    if nlep_val.get() == 1:
        clearFrame()
        OptionsLep.grid(row=1, column=1, rowspan=2)
        slider_LepTMass.grid(row=0)
	slider_maxLepTMass.grid(row=1)
    if nlep_val.get() == 2:
        clearFrame()
        OptionsLep.grid(row=1, column=1, rowspan=5)
	chooseLepchargecb.config(text="Choose leptons' charge")
        chooseLepchargecb.grid(row=0, sticky=W)
	chooseLepflavourcb.config(text="Choose leptons' flavour")
        chooseLepflavourcb.grid(row=3, sticky=W)
        chooseInvMass.grid(row=7, sticky=W)
	qinvmass.grid(row=7, sticky=E)
    if nlep_val.get() == 3:
        clearFrame()
        OptionsLep.grid(row=1, column=1, rowspan=7)
	chooseLepchargecb.grid(row=0,sticky=W)
	qcharges.grid(row=0, sticky=E)
	chooseLepflavourcb.grid(row=3,sticky=W)
	qflavours.grid(row=3, sticky=E)
	LabelInvMass.config(text="Invariant mass of pair:")
	LabelInvMass.grid(row=6, sticky=W)
	qbinvmass.grid(row=6, sticky=E)
	emptyf.grid(row=7)
	entry_InvariantM.pack(side=LEFT)
	plusminus.pack(side=LEFT)
	entry_Range.pack(side=LEFT)
	slider_LepTMass.grid(row=8, sticky=W)
	slider_maxLepTMass.grid(row=9)
    if nlep_val.get() == 4:
        clearFrame()
        OptionsLep.grid(row=1, column=1, rowspan=7)
	chooseLepchargecb.grid(row=0, sticky=W)
	qcharges.grid(row=0, sticky=E)
	chooseLepflavourcb.grid(row=3, sticky=W)
	qflavours.grid(row=3, sticky=E)
	LabelInvMass.config(text = "Invariant mass of pair 1:")
	LabelInvMass.grid(row=6, sticky=W)
	qinvmass.grid(row=6, sticky=E)
	emptyf.grid(row=7)
	entry_InvariantM.pack(side=LEFT)
	plusminus.pack(side=LEFT)
	entry_Range.pack(side=LEFT)
	LabelInvMass2.grid(row=8, sticky=W)
	qinvmass2.grid(row=8, sticky=E)
        entry_InvariantM2.grid(row=9)
	emptyf2.grid(row=10)

b0_lep = Radiobutton(frame1, text="0 Leptons",
                        variable=nlep_val, value=0, command=extLepOpts)
b1_lep = Radiobutton(frame1, text="1 Lepton",
                        variable=nlep_val, value=1, command=extLepOpts)
b2_lep = Radiobutton(frame1, text="2 Leptons",
                        variable=nlep_val, value=2, command=extLepOpts)
b3_lep = Radiobutton(frame1, text="3 Leptons",
                        variable=nlep_val, value=3, command=extLepOpts)
b4_lep = Radiobutton(frame1, text="4 Leptons",
                        variable=nlep_val, value=4, command=extLepOpts)

leppt_val = IntVar() #Want to select min lepton momentum?
leppt_val.set(25)

slider_leppt = Scale(frame1, from_=0, to=100, orient=HORIZONTAL, length=150,variable=leppt_val) #Define slider

st_lepptcb= IntVar() #Checkbutton state

def chooseleppt():  #Function for checkbutton
    if st_lepptcb.get()==1:
        slider_leppt.grid(row=7) #If state 1, show slider
    else:
        slider_leppt.grid_forget()
	leppt_val.set(25)
	st_lepptcb.set(0)

lepptyes = Checkbutton(frame1, bg="LightCyan2", text="Choose lepton momentum (GeV)\n (default 25)",  
	variable = st_lepptcb, onvalue=1,offvalue=0, command=chooseleppt)

st_lepcb = IntVar() #State of checkbox

def chooseNlep(): #function for checkbox
    if st_lepcb.get()==1:
	b0_lep.grid(row=1)
	b1_lep.grid(row=2)
	b2_lep.grid(row=3)
	b3_lep.grid(row=4)
	b4_lep.grid(row=5)
	lepptyes.grid(row=6)
    else:
	nlep_val.set(0)
        clearFrame()
	b0_lep.grid_forget()
        b1_lep.grid_forget()
	b2_lep.grid_forget()
	b3_lep.grid_forget()
	b4_lep.grid_forget()
	lepptyes.grid_forget()
	st_lepptcb.set(0)
	chooseleppt()

lyes = Checkbutton(frame1, text="Choose number of charged leptons", font=("Calibri",10),bg="LightCyan2",
	variable = st_lepcb, onvalue=1,offvalue=0, command=chooseNlep)
lyes.grid(row=0,column=0, sticky=W) #Define and show checkbox

frame1.grid_rowconfigure(1, minsize=50, weight=1)
frame1.grid_rowconfigure(2, minsize=50, weight=1)
frame1.grid_rowconfigure(3, minsize=50, weight=1)
frame1.grid_rowconfigure(4, minsize=50, weight=1)
frame1.grid_rowconfigure(5, minsize=50, weight=1)
frame1.grid_rowconfigure(6, minsize=50, weight=1)
frame1.grid_rowconfigure(7, minsize=50, weight=1)
frame1.grid_columnconfigure(1, minsize=180, weight=1)

qlep = Canvas(frame1, width=16, height=16) 
qlep.place(relx=0.61, rely=0.001, anchor=N)
qlep.create_image(8,8, image=questionmark) #Question mark to be next to "choose lep" option
infolep= Message(frame1, text= "Choose number of leptons.\nRemember that neutrinos won't be detected",
 bg="White", aspect=300) #Information message
 
def on_enterlep(event):
    infolep.place(relx=0.625, rely=0.0155, anchor=NW)
    
def on_leavelep(event):
    infolep.place_forget()
    
qlep.bind("<Enter>", on_enterlep)
qlep.bind("<Leave>", on_leavelep)  #Def and bind two functions for when cursor is over question mark or leaves

#Want specific number jets? Enter number.

labelminjet= Label(frame1, text="Minimum:")
labelmaxjet= Label(frame1, text="Maximum:")

minnjet_val = IntVar()
minnjet_val.set(0) # initialize integer for min number of jets
maxnjet_val = IntVar()
maxnjet_val.set(9) # initialize integer for max number of jets

minjet_entry = Spinbox(frame1, textvariable=minnjet_val, from_=0, to=9, width=4) #Entry for min number of jets
maxjet_entry = Spinbox(frame1, textvariable=maxnjet_val, from_=0, to=9, width=4) #Entry for max number of jets

btagmin_val = IntVar()
btagmin_val.set(0) #Initialise minimum b-jets
btagmin_entry = Spinbox(frame1, textvariable=btagmin_val, from_=0, to=9, width=4) #Entry for minimum number of b-tagged jets
btagmax_val = IntVar()
btagmax_val.set(9) #Initialise maximum b-jets
btagmax_entry = Spinbox(frame1, textvariable=btagmax_val, from_=0, to=9, width=4) #Entry for maximum number of b-tagged jets
labelminbjet= Label(frame1, text="Minimum:")
labelmaxbjet= Label(frame1, text="Maximum:") #Labels for b-jets entries

def Nbtagjet(): #function that will show the entry when checkbox clicked
    if st_btagjetcb.get() ==1:
	labelminbjet.grid(row=12, column=0)
	labelmaxbjet.grid(row=13, column=0)
	btagmin_entry.grid(row=12, column=1)
	btagmax_entry.grid(row=13, column=1)
    else:
	btagmin_entry.grid_forget()
	btagmax_entry.grid_forget()
	labelminbjet.grid_forget()
	labelmaxbjet.grid_forget()
	btagmin_val.set(0)
	btagmax_val.set(9)

st_btagjetcb = IntVar()
btaggedyes = Checkbutton(frame1, text="Any b-tagged jets?", bg="LightCyan2",
	 variable = st_btagjetcb, onvalue=1,offvalue=0, command=Nbtagjet) #Extra checkbox for b-tagged jets

st_jetcb = IntVar() #State of checkbox
def chooseNjet(): #Function for checkbox
    if st_jetcb.get()==1:
        labelminjet.grid(row=9)
        labelmaxjet.grid(row=10)
        minjet_entry.grid(row=9, column=1)
        maxjet_entry.grid(row=10, column=1)
        btaggedyes.grid(row=11)
	qbjet.place(relx=0.45, rely=0.54)

    else:
        minnjet_val.set(0)
        maxnjet_val.set(9)
        labelminjet.grid_forget()
        labelmaxjet.grid_forget()
        minjet_entry.grid_forget()
        maxjet_entry.grid_forget()
        btaggedyes.grid_forget()
	qbjet.place_forget()
        st_btagjetcb.set(0)
	btagmin_entry.grid_forget()
	btagmax_entry.grid_forget()
	labelminbjet.grid_forget()
	labelmaxbjet.grid_forget()
	btagmin_val.set(0)
	btagmax_val.set(9)

jyes = Checkbutton(frame1, text="Choose number jets", bg="LightCyan2", font=("Calibri",10),
	 variable = st_jetcb, onvalue=1,offvalue=0, command=chooseNjet)

jyes.grid(row=8,column=0, sticky=W) #Define and show checkbox

frame1.grid_rowconfigure(9, minsize=30, weight=1)
frame1.grid_rowconfigure(10, minsize=30, weight=1)
frame1.grid_rowconfigure(11, minsize=30, weight=1)
frame1.grid_rowconfigure(12, minsize=30, weight=1)
frame1.grid_rowconfigure(13, minsize=30, weight=1)

qjet = Canvas(frame1, width=16, height=16)
qjet.place(relx=0.36, rely=0.442)
qjet.create_image(8,8, image=questionmark)  #Question mark for jets
infojet= Message(frame1, text= "A quark can decay into a gluon and a quark, creating a jet, which is how we detect them",
 bg="White", aspect=300) #Info message
 
def on_enterjet(event):
    infojet.place(relx=0.395, rely=0.4565, anchor=NW)
    
def on_leavejet(event):
    infojet.place_forget()
    
qjet.bind("<Enter>", on_enterjet)
qjet.bind("<Leave>", on_leavejet) #Def and bind two functions for when cursor is over question mark or leaves

qbjet = Canvas(frame1, width=16, height=16)
qbjet.create_image(8,8, image=questionmark)  #Question mark for b-tagged jets
infobjet= Message(frame1, text= "B-tagged jets are jets produced by bottom quarks",
 bg="White", aspect=300) #Info message
 
def on_enterbjet(event):
    infobjet.place(relx=0.51, rely=0.555, anchor=NW)
    
def on_leavebjet(event):
    infobjet.place_forget()
    
qbjet.bind("<Enter>", on_enterbjet)
qbjet.bind("<Leave>", on_leavebjet) #Def and bind two functions for when cursor is over question mark or leaves

#Sliders for missing momentum

minmissE_val = IntVar() #initialize integer for min
minmissE_val.set(0)
maxmissE_val = IntVar() #initialize integer for max
maxmissE_val.set(200)

slider_minmissP = Scale(frame1, label="Minimum:", from_=0, to=200, orient=HORIZONTAL, length=200, variable = minmissE_val) #Define slider
slider_maxmissP = Scale(frame1, label="Maximum:", from_=0, to=200, orient=HORIZONTAL, length=200, variable = maxmissE_val)

st_missPcb= IntVar() #Checkbutton state
def choosemissP():  #Function for checkbutton
    if st_missPcb.get()==1:

        slider_minmissP.grid(row=15, column=0) #If state 1, show slider
	slider_maxmissP.grid(row=16, column=0)
    else:
        slider_minmissP.grid_forget()
        minmissE_val.set(0)
	slider_maxmissP.grid_forget()
        maxmissE_val.set(200)

minmissPyes = Checkbutton(frame1, text="Missing\n transverse momentum (GeV)", font=("Calibri",10), bg="LightCyan2", 
	variable = st_missPcb, onvalue=1,offvalue=0, command=choosemissP)

minmissPyes.grid(row=14,column=0, sticky=W) #Define and show checkbutton0
frame1.grid_rowconfigure(15, minsize=60, weight=1)
frame1.grid_rowconfigure(16, minsize=60, weight=1)

qmom = Canvas(frame1, width=16, height=16)
qmom.place(relx=0.51, rely=0.655)
qmom.create_image(8,8, image=questionmark) #Question mark for missing momentum
infomom= Message(frame1, text= "Since neutrinos aren't detected at the ATLAS experiment, we can look for events with missing momentum",
 bg="White", aspect=300)  #Info message
 
def on_entermom(event):
    infomom.place(relx=0.545, rely=0.675, anchor=NW)
    
def on_leavemom(event):
    infomom.place_forget()
    
qmom.bind("<Enter>", on_entermom)
qmom.bind("<Leave>", on_leavemom) #Def and bind two functions for when cursor is over question mark or leaves

#Percentage of data to analize
percentg_val = DoubleVar()
percentg_val.set(0)
PercentgEntry = Scale(frame1, label="Percentage of data to analize:", bg="LightCyan2",from_=0, to=100, orient=HORIZONTAL, length=300, resolution=0.5,variable = percentg_val)
PercentgEntry.grid(row=17, column=0, columnspan=2, sticky=W)

#Button to open root browser
latestThread = None #analysis thread
#analysisThread=None # last opened thread
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
                
def abort():
    """aborts analysis"""
    
    global makeplots #do not draw plots if abort is pressed
    makeplots = False
    global pool
    while pool == None:
        continue
    for process in pool:
        process.terminate()
        process.join()
    
def browser():
    """creates new browser_thread closing
    the previous one"""    
    
    global b
    global latestThread
    if latestThread!= None:
        latestThread.shutdown()
    latestThread =browser_thread()
    latestThread.setDaemon(True)
    latestThread.start()

#rbrowser = Button(frame1, text="Root Browser", font=("Calibri", 10) ,bg="Blue", 

#             activebackground="Black", fg= "White",activeforeground="White", command=browser)
#rbrowser.grid(row=19)
#submenu.add_command(label="Root Browser", command=browser)

## Fuction for analysis

#analysis = None

#Button to start analysis
run = Button(frame1, text="RUN", font=("Calibri",12) ,bg="Green", 
             activebackground="Black", fg= "White", activeforeground="White")

run.grid(row=20, column=0)

frame1.grid_rowconfigure(19, minsize=30, weight=1)
frame1.grid_rowconfigure(20, minsize=30, weight=1)
frame1.grid_rowconfigure(21, minsize=30, weight=1)

test = Button(frame1, text="TEST", font=("Calibri",12) ,bg="White", 
             activebackground="Black", fg= "Black", activeforeground="White")

#Abort button (doesn't do anything at the moment)
abortb = Button(frame1, text="ABORT", font=("Calibri",12), bg="Red", 
             activebackground="Black", fg= "White", activeforeground="White",command = abort
             )

#Progress bar
MAX = 29
k = 0
progress_var = DoubleVar()
progressbar = ttk.Progressbar(frame1, variable=progress_var, maximum=MAX)

def update_bar():
    global k
    progress_var.set(k)
    k += 1
    window.update_idletasks()

#Label for when plots are being drawn
drawingp = Label(frame1, text="Drawing plots...",fg="black", height=2, font=("Calibri", 12))

histograms =[]

#analyser = None
pool= None #the pool of jobs
makeplots = True #whether to draw the plots

def run_analysis():
    """runs the analysis"""  

    global makeplots #draw the plots
    makeplots = True
    
    selection = []
    global histograms
    
    del histograms[:]
    
    CustomConfiguration.Job["Fraction"] = percentg_val.get()/100.0   

    histograms.append("n_jets")
    histograms.append("lep_n")
    
    if minmissE_val.get()<=maxmissE_val.get() or maxmissE_val.get()!=0:
        histograms.append("etmiss")
        
    if st_lepcb.get() == 0 or nlep_val.get() !=0:
        histograms.append("lep_pt")
        histograms.append("lep_eta")
        histograms.append("lep_phi")
        histograms.append("lep_E")

    if minnjet_val.get()<=maxnjet_val.get() or maxnjet_val.get()!=0:
               
        histograms.append("jet_pt")
        histograms.append("jet_m")
        histograms.append("jet_eta")

    if st_lepptcb.get()==1:
        AH.lep_num = leppt_val.get()
    
    if st_jetcb.get() ==1: #number of jets
        jetn_chk = CheckFileSuper.CheckNJets(minnjet_val.get(),maxnjet_val.get())
        selection.append(jetn_chk)
 
        
        if st_btagjetcb.get()==1: #btagging
            btag_chk = CheckFileSuper.CheckBTag(btagmin_val.get(),btagmin_val.get())

            selection.append(btag_chk)
            
    if st_lepcb.get() != 0: #number of leptons
    
        lepn_chk = CheckFileSuper.CheckNLep(nlep_val.get())
        selection.append(lepn_chk)
    
        #if nlep_val.get()!=0:
         #   histograms.append("leadlep_pt")
          #  histograms.append("leadlep_eta")
           # histograms.append("leadlep_phi")
            #histograms.append("leadlep_E")
            #histograms.append("leadlep_charge")
            #histograms.append("leadlep_type")  
        
        if nlep_val.get()==1:        
            #transverse mass
            checkTMass = CheckFileSuper.CheckTMass(LepTmass_val.get(),LepTmassMax_val.get(),0,"WtMass")
            selection.append(checkTMass)
            histograms.append("WtMass")
	 
        if nlep_val.get()==2:   
 	    #checkAngle = CheckFileSuper.CheckAngle(angleLepMP_val.get(),"deltaTheta")
	    #selection.append(checkAngle)
	    #histograms.append("deltaTheta")
           
           if st_lepchargecb.get()!=0: #lepton charge
                if TwoLepcharge_val.get()==1:
                    twoLepCharge = CheckFileSuper.CheckLepCharge("same",0,1)
                else:
                    twoLepCharge = CheckFileSuper.CheckLepCharge("different",0,1)
                selection.append(twoLepCharge)
            
           if st_lepflavourcb.get()!=0: #lepton flavour
               if TwoLepflavour_val.get()==1:
                   twoLepFlavour = CheckFileSuper.CheckLepFlavour("same",0,1)    
               else:
                   twoLepFlavour = CheckFileSuper.CheckLepFlavour("different",0,1)
               selection.append(twoLepFlavour)
               
           if st_InvMasscb.get()==1: #invariant mass of pair
               invMassCheck = CheckFileSuper.CheckInvMass(InvariantM_val.get(),Range_val.get(),0,1,"invMass")
               selection.append(invMassCheck)
               histograms.append("invMass")
               
        if nlep_val.get()==3:

            subselection =[]
        
            if st_lepchargecb.get()!=0: #lepton charge
                if TwoLepcharge_val.get()==1:
                    twoLepCharge = CheckFileSuper.CheckLepCharge("same",0,1)
                else:
                    twoLepCharge = CheckFileSuper.CheckLepCharge("different",0,1)
                    
                subselection.append(twoLepCharge)
       
            if st_lepflavourcb.get()!=0: #lepton flavour
                if TwoLepflavour_val.get()==1:
                    twoLepFlavour = CheckFileSuper.CheckLepFlavour("same",0,1)    
                else:
                    twoLepFlavour = CheckFileSuper.CheckLepFlavour("different",0,1)
               
                subselection.append(twoLepFlavour)

            threeLepton = CheckFileSuper.CheckThreeLepton("invMass",InvariantM_val.get(),
                    Range_val.get(), LepTmass_val.get(),LepTmassMax_val.get(),"WtMass", subselection)                                               
            selection.append(threeLepton)
            
            histograms.append("WtMass")
            histograms.append("invMass")
            
        if nlep_val.get() == 4:           
            subselection =[]
        
            if st_lepchargecb.get()!=0: #lepton charge
                if TwoLepcharge_val.get()==1:
                    twoLepCharge = CheckFileSuper.CheckLepCharge("same",0,1)
                else:
                    twoLepCharge = CheckFileSuper.CheckLepCharge("different",0,1)
                    
                subselection.append(twoLepCharge)
       
            if st_lepflavourcb.get()!=0: #lepton flavour
                if TwoLepflavour_val.get()==1:
                    twoLepFlavour = CheckFileSuper.CheckLepFlavour("same",0,1)    
                else:
                    twoLepFlavour = CheckFileSuper.CheckLepFlavour("different",0,1)
               
                subselection.append(twoLepFlavour)
                
            fourLepton =CheckFileSuper.CheckFourLepton("invMass","invMass2",
            InvariantM_val.get(),InvariantM2_val.get(),Range_val.get(),subselection)

            selection.append(fourLepton)

            histograms.append("invMass")
            histograms.append("invMass2")

    if st_missPcb.get()==1: #missing momentum
        missE_chk = CheckFileSuper.CheckEtMiss(minmissE_val.get(),maxmissE_val.get())

        selection.append(missE_chk) 
        
    processingDict = CustomConfiguration.Processes
    print CustomConfiguration.Job["Fraction"]
        
    CustomConfiguration.Job["Batch"] = True
    jobs = [NewJob.NewJob(processName,CustomConfiguration.Job, fileLocation,selection,histograms) for processName, fileLocation in processingDict.items()]
    jobs = NewRunScript.SortJobsBySize(jobs)
    global pool
    pool = []
    for job in jobs:
        process = JobPool(job)
        process
        process.start()
        pool.append(process)
                
    pool.reverse()
    for process in pool:
        process.join()
        update_bar()
   
    progressbar.grid_forget()
    global k
    k = 0
    progress_var.set(0)
    abortb.grid_forget()
    drawingp.grid(row=20)
    global runpressed
    if not makeplots:
        drawingp.grid_forget()
        plotb.grid(row=20, sticky=E) 
        run.grid(row=20)
        runpressed = False
        return
    
    global listphotos
    del listphotos[:]
    global listphotosbig
    del listphotosbig[:]
    global listcommands
    del listcommands[:]
    global listbuttons
    if len(listbuttons) > 0:
        for i in range(0,len(listbuttons)):
            listbuttons[i].grid_forget()
    del listbuttons[:]
    global listlabels
    del listlabels[:]
    previousplots=glob.glob('Output/*.png')
    for plot in previousplots: 
        os.remove(plot)

    if not histograms == []:
        NewPlotResults.plot_results(histograms)

    plotting()
    drawingp.grid_forget()
    plotb.grid(row=20, sticky=E) 
    run.grid(row=20)
    runpressed = False
    
class JobPool(multiprocessing.Process):
    
    def __init__(self,job):
        super(JobPool,self).__init__()
        self.job = job
    
    def run(self):
        self.job.run()
        
    
class run_thread(threading.Thread):
    """thread object for running the analysis"""
    
    def __init__(self):
        super(run_thread,self).__init__()

    def run(self):
        run_analysis()
              
runpressed = False
    
def run_a():
    """creates an analysis therad"""  
    abortb.grid(row=20)
    plotb.grid_forget()  
    run.grid_forget()
    progressbar.grid(row=21) 
    global runpressed
    runpressed = True

    global latestThread
    latestThread =run_thread()
    latestThread.setDaemon(True)
    latestThread.start()

run.config(command = run_a)

def plotting():
    
    plots = glob.glob('Output/*.png')
    lplots = len(plots)
    try:
	    for j in range(0, 6):
		    for i in range(0,4):
			    photo = PhotoImage(file= plots[i+j*4])
			    listphotosbig.insert(i+j*4, photo)
			    photo2 = photo.subsample(6)
			    listphotos.insert(i+j*4, photo2)
			    def showplot(p=i,q=j):
				    newwin = Toplevel()
				    topscrollbar = Scrollbar(newwin)
				    topscrollbar.pack(side=RIGHT, fill=Y)
				    topcanvas = Canvas(newwin, width=900, height=2000, yscrollcommand=topscrollbar.set, scrollregion=(0,0,0,850))
				    topcanvas.pack()
				    bigplot = topcanvas.create_image(450,420, image = listphotosbig[p+q*4])
				    topscrollbar.config(command=topcanvas.yview)
			    listcommands.insert(i+j*4, showplot)
			    listbuttons.insert(i+j*4, Button(frameOUT, command=listcommands[i+j*4], compound=BOTTOM, text=plots[i+j*4][7:][:-4], image=listphotos[i+j*4]))
			    listbuttons[i+j*4].grid(row=j+1, column=i+1)
    except IndexError:
	    pass

#Button to plot results

listphotos = [] #some lists needed
listphotosbig = []
listcommands = []
listbuttons = []
listlabels = []

plotb = Button(frame1, text="PLOT", font=("Calibri", 11) ,bg="Blue", 
             activebackground="Black", fg= "White",activeforeground="White", command=plotting)

plotb.grid(row=20, column=0, sticky=E)

#Add a few functions to menu
#submenu.add_command(label="Run Analysis", command=run_analysis)
#submenu.add_command(label="Plot Results", command=plotting)

#When they try to leave analysis aborted

def on_closing():
    if runpressed:
	 tkMessageBox.showwarning("WARNING","Analysis still runnin.\n Please, press abort")
    else:
         window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

#Wellcome message
wellcome = PhotoImage(file="Wellcome.png")
wellcomeCanvas = Canvas(window, width=881, height=471)
wellcomeCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
wellcomeCanvas.create_image(441,236, image=wellcome)

okbutton = Button(window, text="OK", font=("Calibri",20), bg="white", 
             activebackground="Black", fg= "black", activeforeground="White") #Button to close wellcome message and start
okbutton.place(relx=0.5, rely=0.77, anchor=CENTER)

def start():
   wellcomeCanvas.place_forget()
   okbutton.place_forget()

okbutton.config(command=start)
            
window.mainloop()
