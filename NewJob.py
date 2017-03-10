import ROOT
import glob
import sys
import CustomAnalysis

#==================================================================
class NewJob(object):
    """This class is a carrier class for a given analysis. It takes care of the technical details like
    file writing, setting up the input tree and providing statistics about the status of the analysis.    
    """
    def __init__(self, processName, configuration, inputLocation,list_check,histograms):
        super(NewJob, self).__init__()
        #Configurables
        self.Name       = processName
        self.Configuration = configuration
        self.MaxEvents     = configuration["MaxEvents"]
        self.InputFiles    = glob.glob(inputLocation)
        self.list_check = list_check
        self.histograms = histograms
        
        # Outputs
        self.OutputFileLocation = configuration["OutputDirectory"] + processName
        self.OutputFile = None

        # Classes - InputTree and Analysis have to be created later otherwise parallel running does not work
        self.InputTree     = None
        self.Analysis      = None

    #Setup functions
    def setupTree(self):
      tree = ROOT.TChain("mini")
      for filename in self.InputFiles:
        tree.Add(filename)
      return tree                    
    def createAnalysis(self, analysisName):
        analysisName = "CustomAnalysis"
        analysis = CustomAnalysis.CustomAnalysis(self.Name,self.list_check,self.histograms)
        analysis.Store.initializeTuple(self.InputTree)
        analysis.setIsData("data" in self.Name.lower())
        return analysis
    
    #Execution functions                    
    def run(self):
      self.initialize()
      self.execute()
      self.finalize()
      
    def initialize(self):
        self.OutputFile = ROOT.TFile.Open(self.OutputFileLocation + ".root","RECREATE")
        self.InputTree = self.setupTree()
        self.Analysis  = self.createAnalysis(self.Configuration["Analysis"])
        self.determineMaxEvents()
        self.Analysis.doInitialization()
        
    def execute(self):
      for n in xrange(self.MaxEvents):
        self.InputTree.GetEntry(n)
        self.Analysis.doAnalysis()
        
    def finalize(self):
        self.Analysis.doFinalization()
        self.OutputFile.Close()
    
    # Helper functions
    def determineMaxEvents(self):
      nentries= self.InputTree.GetEntries()
      if nentries==0:
        sys.exit(1)
      
      if self.MaxEvents > nentries:
        self.MaxEvents = nentries
      
      self.MaxEvents = int(self.MaxEvents*self.Configuration["Fraction"]) 

        

