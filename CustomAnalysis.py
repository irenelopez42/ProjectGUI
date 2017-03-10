import NewBaseAnalysis
import NewAnalysisHelpers as AH
import NewHistManager as HM

class CustomAnalysis(NewBaseAnalysis.Analysis):
    """the object for the analysis specified by the selected options in the GUI."""
	
    def __init__(self, store, checkList,histograms):
        """checkList is the list of CheckFile objects. Histograms
           is the histograms that will be plotted. HistObjDic is the dictionary
           with key/value histogram name/ histrogram ROOT objects. HistValDic
           is the dictionary with key/value  histogram name/ appropriate event 
           data"""
        super(CustomAnalysis, self).__init__(store)
        self.checkList = checkList
        self.histograms = histograms
        self.histValDic ={}
        self.histObjDic ={}

    def initialize(self):
        """build a dictionary with the key being the histogram name 
           and the value being the ROOT histogram object"""
        for histogram in self.histograms:
		self.histObjDic[histogram] = HM.returnHistogram(histogram)

    def analyze(self):
         """checks an event satisfies the conditions"""
         eventinfo = self.Store.getEventInfo() #Store contains the current event
         leptons = AH.selectAndSortContainer(self.Store.getLeptons(),AH.isGoodLepton, lambda p: p.pt())
         jets = AH.selectAndSortContainer(self.Store.getJets(),AH.isGoodJet, lambda p: p.pt())
         EtMiss = self.Store.getEtMiss()
         EventObject = {"eventinfo" :eventinfo, "leptons" : leptons, "jets" : jets, "EtMiss" :EtMiss}
         self.histValDic = {}
         weight = eventinfo.scalefactor()*eventinfo.eventWeight() if not self.getIsData() else 1		
		
         for checktype in self.checkList:
            if checktype.check(EventObject,self.histValDic) is False:
                return False
                    
         histogramAppend(EventObject,self.histValDic)
                
         for histogram in self.histograms:
             if not isinstance(self.histValDic[histogram],list):
                 self.histObjDic[histogram].Fill(self.histValDic[histogram],weight)
             else:
                 for item in self.histValDic[histogram]:
                     self.histObjDic[histogram].Fill(item,weight)			
         return True


    def finalize(self):
        HM.writeHist(self.histObjDic)

def histogramAppend(EventObject,histogramDictionary):

	jets = EventObject["jets"]
	histogramDictionary["n_jets"] =  len(jets)

	histogramDictionary["jet_pt"]= []
	histogramDictionary["jet_m"] =[]
	histogramDictionary["jet_jvf"]=[]
	histogramDictionary["jet_eta"]=[]
	histogramDictionary["jet_MV1"] =[]

	for jet in jets:
		histogramDictionary["jet_pt"].append(jet.pt())
		histogramDictionary["jet_jvf"].append(jet.jvf())
		histogramDictionary["jet_m"].append(jet.m())
		histogramDictionary["jet_eta"].append(jet.eta())
		histogramDictionary["jet_MV1"].append(jet.mv1())

	leptons = EventObject["leptons"]
	histogramDictionary["lep_n"] = len(leptons)
		
	histogramDictionary["lep_pt"]= []
	histogramDictionary["lep_eta"] =[]
	histogramDictionary["lep_phi"]=[]
	histogramDictionary["lep_E"]=[]
	histogramDictionary["lep_charge"] =[]
	histogramDictionary["lep_type"]=[]

	for lepton in leptons:
		histogramDictionary["lep_pt"].append(lepton.pt())
		histogramDictionary["lep_eta"].append(lepton.eta())
		histogramDictionary["lep_phi"].append(lepton.phi())
		histogramDictionary["lep_E"].append(lepton.e())
		histogramDictionary["lep_charge"].append(lepton.charge())
		histogramDictionary["lep_type"].append(lepton.pdgId())
	if len(leptons) > 0:
		leadLepton = leptons[0]		

		histogramDictionary["leadlep_pt"] = leadLepton.pt()
		histogramDictionary["leadlep_eta"] = leadLepton.eta()
		histogramDictionary["leadlep_phi"] = leadLepton.phi()
		histogramDictionary["leadlep_E"] = leadLepton.e()
		histogramDictionary["leadlep_charge"] = leadLepton.charge()
		histogramDictionary["leadlep_type"] = leadLepton.pdgId()

		if len(leptons) >1:
			trailLepton = leptons[1]
			histogramDictionary["traillep_pt"] = trailLepton.pt()
			histogramDictionary["traillep_eta"] = trailLepton.eta()
			histogramDictionary["traillep_phi"] = trailLepton.phi()
			histogramDictionary["traillep_E"] = trailLepton.e()
			histogramDictionary["traillep_charge"] = trailLepton.charge()
			histogramDictionary["traillep_type"] = trailLepton.pdgId()
   
	etmiss = EventObject["EtMiss"]
	histogramDictionary["etmiss"] = etmiss.et()