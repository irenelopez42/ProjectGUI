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
import NewAnalysisHelpers as AH
import glob
import os

window = Tk()

#Define a drop down menu in case we need it
menu = Menu(window)
window.config(menu=menu)
submenu = Menu(menu)
menu.add_cascade(label="File", menu=submenu)

#Canvas and scrollbar

#scrollbar = Scrollbar(window)
#scrollbar.pack(side=RIGHT, fill=Y)
#canvas = Canvas(window, width=1200, height=900, yscrollcommand=scrollbar.set, scrollregion=(0,0,0,900))
#canvas.pack()
#scrollbar.config(command=canvas.yview)

#Create invisible frames to organize layout
frame1 = Frame(window, width="200", padx=50, height="450") #where widgets will be
frame1.pack(side=LEFT)
frameOUT = Frame(window, width="1000", height="900", bg="thistle4") #where plots will show
frameOUT.pack(side=LEFT)

#Widgets:
    
#Want specific number of lepton? Enter number.

nlep_val = IntVar()
nlep_val.set(0) # initialize a string for number of leptons


OptionsLep = Frame(frame1) #Frame to share extra options for leptons

#initialize values for extra options
LepTmass_val = IntVar()
LepTmass_val.set(0)  #Lepton transverse mass
st_lepchargecb = IntVar()
TwoLepcharge_val = IntVar()
TwoLepcharge_val.set(1) #2 Leptons: same/diferent charge
st_lepflavourcb = IntVar()
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


slider_LepTMass = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL, 
			length=170, width=10, variable = LepTmass_val, bg = "lavender",label="Transverse mass") #slider for transverse mass
chooseLepchargecb = Checkbutton(OptionsLep, text="Choose leptons' charges", bg ="lavender", variable = st_lepchargecb, onvalue=1,offvalue=0, 				command=chooseLepcharge)
chooseLepflavourcb = Checkbutton(OptionsLep, text="Choose leptons' flavours", bg = "lavender", variable = st_lepflavourcb, onvalue=1,offvalue=0, command=chooseLepflavour)
slider_InvariantM = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL,
			length=170, width=10, variable = InvariantM_val, bg = "lavender") #Slider for invariant mass
slider_InvariantM2 = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL,
			length=170, width=10, variable = InvariantM2_val, bg = "lavender",label="Invariant mass of 2nd pair") #Slider for invariant mass of 2nd pair (4 leptons case)  
slider_Range = Scale(OptionsLep, from_=0, to=100, orient=HORIZONTAL,
			length=170, width=10, variable = Range_val, bg = "lavender",label="Range") #Slider for range of invariant mass 

def clearFrame():    #function to clear all extra options
    OptionsLep.grid_forget()
    slider_LepTMass.grid_forget()
    chooseLepchargecb.grid_forget()
    chooseLepflavourcb.grid_forget()
    slider_InvariantM.grid_forget()
    slider_InvariantM2.grid_forget()
    slider_Range.grid_forget()
    LepTmass_val.set(0)
    st_lepchargecb.set(0)
    st_lepflavourcb.set(0)
    chooseLepcharge()
    chooseLepflavour()
    InvariantM_val.set(0)
    InvariantM2_val.set(0)
    Range_val.set(0)

def extLepOpts():
    if nlep_val.get() == 1:
        clearFrame()
        OptionsLep.grid(row=1, column=2)
        slider_LepTMass.grid(row=0)
    if nlep_val.get() == 2:
        clearFrame()
        OptionsLep.grid(row=1, column=2, rowspan=5)
        chooseLepchargecb.grid(row=0)
        chooseLepflavourcb.grid(row=3)
        slider_InvariantM.config(label="Invariant mass")
        slider_InvariantM.grid(row=7, sticky=W)
	slider_Range.grid(row=8, sticky=W)
    if nlep_val.get() == 3:
        clearFrame()
        OptionsLep.grid(row=1, column=2, rowspan=5)
	chooseLepchargecb.grid(row=0)
	chooseLepflavourcb.grid(row=3)
	slider_InvariantM.config(label="Invariant mass of best pair")
        slider_InvariantM.grid(row=6, sticky=W)
	slider_Range.grid(row=7, sticky=W)
	slider_LepTMass.grid(row=8, sticky=W)
    if nlep_val.get() == 4:
        clearFrame()
        OptionsLep.grid(row=1, column=2, rowspan=5)
	chooseLepchargecb.grid(row=0)
	chooseLepflavourcb.grid(row=3)
	slider_InvariantM.config(label="Invariant mass of 1st pair")
        slider_InvariantM.grid(row=6, sticky=W)
        slider_InvariantM2.grid(row=7, sticky=W)
	slider_Range.grid(row=8, sticky=W)

b1_lep = Radiobutton(frame1, text="1 Lepton",
                        variable=nlep_val, value=1, command=extLepOpts)
b2_lep = Radiobutton(frame1, text="2 Leptons",
                        variable=nlep_val, value=2, command=extLepOpts)
b3_lep = Radiobutton(frame1, text="3 Leptons",
                        variable=nlep_val, value=3, command=extLepOpts)
b4_lep = Radiobutton(frame1, text="4 Leptons",
                        variable=nlep_val, value=4, command=extLepOpts)

leppt_val = IntVar() #Want to select min lepton momentum?
leppt_val.set(0)

slider_leppt = Scale(frame1, from_=0, to=100, orient=HORIZONTAL, length=150,variable=leppt_val) #Define slider

st_lepptcb= IntVar() #Checkbutton state
def chooseleppt():  #Function for checkbutton
    if st_lepptcb.get()==1:
        slider_leppt.grid(row=6) #If state 1, show slider
    else:
        slider_leppt.grid_forget()
	leppt_val.set(0)
	st_lepptcb.set(0)

lepptyes = Checkbutton(frame1, bg="LightCyan2", text="Choose lepton momentum (GeV)\n (default 25)",  
	variable = st_lepptcb, onvalue=1,offvalue=0, command=chooseleppt)

st_lepcb = IntVar() #State of checkbox
def chooseNlep(): #function for checkbox
    if st_lepcb.get()==1:
	b1_lep.grid(row=1)
	b2_lep.grid(row=2)
	b3_lep.grid(row=3)
	b4_lep.grid(row=4)
	lepptyes.grid(row=5)
    else:
	nlep_val.set(0)
        clearFrame()
        b1_lep.grid_forget()
	b2_lep.grid_forget()
	b3_lep.grid_forget()
	b4_lep.grid_forget()
	lepptyes.grid_forget()
	st_lepptcb.set(0)
	chooseleppt()

lyes = Checkbutton(frame1, text="Choose number leptons", font=("Calibri",10),bg="LightCyan2",
	variable = st_lepcb, onvalue=1,offvalue=0, command=chooseNlep)
lyes.grid(row=0,column=0, sticky=W) #Define and show checkbox

frame1.grid_rowconfigure(1, minsize=50, weight=1)
frame1.grid_rowconfigure(2, minsize=50, weight=1)
frame1.grid_rowconfigure(3, minsize=50, weight=1)
frame1.grid_rowconfigure(4, minsize=50, weight=1)
frame1.grid_rowconfigure(5, minsize=50, weight=1)
frame1.grid_rowconfigure(6, minsize=50, weight=1)

#Want specific number jets? Enter number.

labelminjet= Label(frame1, text="Minimum:")
labelmaxjet= Label(frame1, text="Maximum:")

minnjet_val = IntVar()
minnjet_val.set(0) # initialize integer for min number of jets
maxnjet_val = IntVar()
maxnjet_val.set(0) # initialize integer for max number of jets

minjet_entry = Spinbox(frame1, textvariable=minnjet_val, from_=0, to=6, width=4) #Entry for min number of jets
maxjet_entry = Spinbox(frame1, textvariable=maxnjet_val, from_=0, to=6, width=4) #Entry for max number of jets

btag_val = IntVar()
btag_entry = Spinbox(frame1, textvariable=btag_val, from_=0, to=6, width=4) #Entry for number of b-tagged jets

def Nbtagjet(): #function that will show the entry when checkbox clicked
	if st_btagjetcb.get() ==1:
		btag_entry.grid(row=10, column=1)
	else:
		btag_entry.grid_forget()
		btag_val.set(0)

st_btagjetcb = IntVar()
btaggedyes = Checkbutton(frame1, text="Any b-tagged jets?", bg="LightCyan2",
	 variable = st_btagjetcb, onvalue=1,offvalue=0, command=Nbtagjet) #Extra checkbox for b-tagged jets

st_jetcb = IntVar() #State of checkbox
def chooseNjet(): #Function for checkbox
    if st_jetcb.get()==1:

	labelminjet.grid(row=8)
	labelmaxjet.grid(row=9)
	minjet_entry.grid(row=8, column=1)
	maxjet_entry.grid(row=9, column=1)
        btaggedyes.grid(row=10)
    else:
        minnjet_val.set(0)
	maxnjet_val.set(0)
	labelminjet.grid_forget()
	labelmaxjet.grid_forget()
	minjet_entry.grid_forget()
	maxjet_entry.grid_forget()
        btaggedyes.grid_forget()
        st_btagjetcb.set(0)
        btag_val.set(0)
        btag_entry.grid_forget()

jyes = Checkbutton(frame1, text="Choose number jets", bg="LightCyan2", font=("Calibri",10),
	 variable = st_jetcb, onvalue=1,offvalue=0, command=chooseNjet)

jyes.grid(row=7,column=0, sticky=W) #Define and show checkbox

frame1.grid_rowconfigure(8, minsize=30, weight=1)
frame1.grid_rowconfigure(9, minsize=30, weight=1)
frame1.grid_rowconfigure(10, minsize=30, weight=1)



#Sliders for missing momentum

minmissE_val = IntVar() #initialize integer for min
minmissE_val.set(0)
maxmissE_val = IntVar() #initialize integer for max
maxmissE_val.set(0)

slider_minmissP = Scale(frame1, label="Minimum:", from_=0, to=100, orient=HORIZONTAL, length=150, variable = minmissE_val) #Define slider
slider_maxmissP = Scale(frame1, label="Maximum:", from_=0, to=100, orient=HORIZONTAL, length=150, variable = maxmissE_val)

st_missPcb= IntVar() #Checkbutton state
def choosemissP():  #Function for checkbutton
    if st_missPcb.get()==1:

        slider_minmissP.grid(row=12, column=0) #If state 1, show slider
	slider_maxmissP.grid(row=13, column=0)
    else:
        slider_minmissP.grid_forget()
        minmissE_val.set(0)
	slider_maxmissP.grid_forget()
        maxmissE_val.set(0)

minmissPyes = Checkbutton(frame1, text="Missing\n transverse momentum (GeV)", font=("Calibri",10), bg="LightCyan2", 
	variable = st_missPcb, onvalue=1,offvalue=0, command=choosemissP)

minmissPyes.grid(row=11,column=0, sticky=W) #Define and show checkbutton

frame1.grid_rowconfigure(12, minsize=60, weight=1)
frame1.grid_rowconfigure(13, minsize=60, weight=1)

#Percentage of data to analize
percentg_val = IntVar()
percentg_val.set(0)
PercentgEntry = Scale(frame1, label="Percentage of data to analize:", bg="LightCyan2",from_=0, to=100, orient=HORIZONTAL, length=300, resolution=0.5,variable = percentg_val)
PercentgEntry.grid(row=14, column=0, columnspan=2, sticky=W)

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


#rbrowser = Button(frame1, text="Root Browser", font=("Calibri", 10) ,bg="Blue", 
#             activebackground="Black", fg= "White",activeforeground="White", command=browser)
#rbrowser.grid(row=19)
submenu.add_command(label="Root Browser", command=browser)


## Fuction for analysis

histograms =[]

def run_analysis():
    """runs the analysis"""
    
    global latestThread
    if latestThread!= None:
        latestThread.shutdown()
        latestThread=None
        
    selection = []
    global histograms
    
    del histograms[:]

    
    histograms.append("n_jets")
    histograms.append("lep_n")
    histograms.append("etmiss")
    
    histograms.append("jet_pt")
    histograms.append("jet_m")
    histograms.append("jet_eta")

    histograms.append("lep_pt")
    histograms.append("lep_eta")
    histograms.append("lep_phi")
    histograms.append("lep_E")
    histograms.append("lep_charge")
    histograms.append("lep_type")

    if st_lepptcb.get()==1:
        print AH.lep_num
        AH.lep_num = leppt_val.get()
        print AH.lep_num
    
    if st_jetcb.get() ==1: #number of jets
        jetn_chk = CheckFileSuper.CheckNJets(njet_val.get())
        selection.append(jetn_chk)
 
        
        if st_btagjetcb.get()==1: #btagging
            btag_chk = CheckFileSuper.CheckBTag(btag_val.get())
            selection.append(btag_chk)
            
    if nlep_val.get() != 0: #number of leptons
    
        lepn_chk = CheckFileSuper.CheckNLep(nlep_val.get())
        selection.append(lepn_chk)
    
        histograms.append("leadlep_pt")
        histograms.append("leadlep_eta")
        histograms.append("leadlep_phi")
        histograms.append("leadlep_E")
        histograms.append("leadlep_charge")
        histograms.append("leadlep_type")  
        
        if nlep_val.get()==1:        
            #Tmass
            checkTMass = CheckFileSuper.CheckTMass(LepTmass_val.get(),0,"WtMass")
            selection.append(checkTMass)
            histograms.append("WtMass")
	 
	if nlep_val.get()==2:   
 	    checkAngle = CheckFileSuper.CheckAngle(angleLepMP_val.get(),"deltaTheta")
	    selection.append(checkAngle)
	    histograms.append("deltaTheta")
           
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
            
        if nlep_val.get()>1:
            histograms.append("traillep_pt")
            histograms.append("traillep_eta")
            histograms.append("traillep_E")
            histograms.append("traillep_phi")
            histograms.append("traillep_charge")
            histograms.append("traillep_type")
    
    if st_missPcb.get()==1: #missing momentum
        missE_chk = CheckFileSuper.CheckEtMiss(missE_val.get())
        selection.append(missE_chk)
     
    NewRunScript.run(selection,histograms)
    ROOT.gApplication.Terminate(0) 
 
def plotting():
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
     
    global histograms
    if not histograms == []:
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
				    topscrollbar = Scrollbar(newwin)
				    topscrollbar.pack(side=RIGHT, fill=Y)
				    topcanvas = Canvas(newwin, width=900, height=2000, yscrollcommand=topscrollbar.set, scrollregion=(0,0,0,850))
				    topcanvas.pack()
				    bigplot = topcanvas.create_image(450,420, image = listphotosbig[p+q*6])
				    topscrollbar.config(command=topcanvas.yview)
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
    
plot = Button(frame1, text="Plot Results", font=("Calibri", 12) ,bg="Blue", 
             activebackground="Black", fg= "White",activeforeground="White", command=plotting)

plot.grid(row=20, column=1, sticky=W)



#Button to start analysis
run = Button(frame1, text="Run Analysis", font=("Calibri",14) ,bg="Green", 
             activebackground="Black", fg= "White", activeforeground="White", command = run_analysis)

run.grid(row=20, column=0, sticky=E)

frame1.grid_rowconfigure(19, minsize=30, weight=1)

#Add a few functions to menu
submenu.add_command(label="Run Analysis", command=run_analysis)
submenu.add_command(label="Plot Results", command=plotting)


window.mainloop()
