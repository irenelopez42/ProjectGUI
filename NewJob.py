import ROOT
import glob
import importlib
import sys
import time
import CustomAnalysis

import Analysis.JobStatistics


#==================================================================





class NewJob(object):
    """This class is a carrier class for a given analysis. It takes care of the technical details like
    file writing, setting up the input tree and providing statistics about the status of the analysis.    
    """

    
    def __init__(self, processName, configuration, inputLocation,list_check,histograms,stopping):
        super(NewJob, self).__init__()
        #Configurables
        self.Name       = processName
        self.Configuration = configuration
        self.MaxEvents     = configuration["MaxEvents"]
        self.InputFiles    = glob.glob(inputLocation)
        self.list_check = list_check
        self.histograms = histograms
        self.st = stopping
        
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
        #self.log("Adding file: " + filename)
        tree.Add(filename)
      return tree

                    
    def createAnalysis(self, analysisName):
        analysisName = "CustomAnalysis"
        #importedAnalysisModule = importlib.import_module("Analysis." + analysisName)
        analysis = CustomAnalysis.CustomAnalysis(self.Name,self.list_check,self.histograms)
        analysis.Store.initializeTuple(self.InputTree)
        analysis.setIsData("data" in self.Name.lower())
        #analysis.setIsQuiet(self.Configuration["Quiet"])
        return analysis
    
    #Execution functions                    
    def run(self):
      self.initialize()
      self.execute()
      self.finalize()
      
    def initialize(self):
      if self.st.doNotStop:
          self.OutputFile = ROOT.TFile.Open(self.OutputFileLocation + ".root","RECREATE")
          self.InputTree = self.setupTree()
          self.Analysis  = self.createAnalysis(self.Configuration["Analysis"])
          self.determineMaxEvents()
          self.Analysis.doInitialization()
        
    def execute(self):
      n=0
      while self.st.doNotStop and n < self.MaxEvents:
        self.InputTree.GetEntry(n)
        self.Analysis.doAnalysis()
        n = n+1
            
    def finalize(self):
      if self.st.doNotStop:
          self.Analysis.doFinalization()
      if self.OutputFile!= None:
          self.OutputFile.Close()
    
      print self.st.doNotStop


    # Helper functions
    def determineMaxEvents(self):
      nentries= self.InputTree.GetEntries()
      if nentries==0:
        #self.log("Empty files! Abort!")
        sys.exit(1)
      
      if self.MaxEvents > nentries:
        self.MaxEvents = nentries
      
      self.MaxEvents = int(self.MaxEvents*self.Configuration["Fraction"]) 

        

