# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 21:19:29 2017

@author: tom
"""
import sys
import os
import importlib
import NewJob
import CustomConfiguration
from multiprocessing import Pool 

import threading 
import stopping as st


    

def buildProcessingDict(configuration, samples):
    if samples == "": 
        return configuration.Processes
    processingDict = {}
    listOfSamples = [substring.strip() for substring in samples.split(',')]
    for sample in listOfSamples:
        try:
            processingDict[sample] = configuration.Processes[sample]
        except :
            print "Name of Sample %s not recognized. Sample was not added to processing list!" % sample
    return processingDict

def checkAnalysis(configuration, analysisOption):
    analysisName = analysisOption if analysisOption != "" else configuration.Job["Analysis"]
    try:
        importedAnalysisModule = importlib.import_module(analysisName)
        configuration.Job["Analysis"] = analysisName
    except ImportError:
        print "Error when trying to read the analysis code for %s. Please check name validity" % analysisName
        sys.exit(1)

def BuildJob(configuration, processName, fileLocation,list_check,histograms,stopping):
    job = NewJob.NewJob(processName, configuration, fileLocation,list_check,histograms,stopping)
    return job


def SortJobsBySize(jobs):  
    def jobSize(job):
        return sum([os.lstat(f).st_size for f in job.InputFiles])
    return sorted(jobs, key=jobSize, reverse=True)
    

def RunJob(job):
    job.run()

class JobThread(threading.Thread):
    def __init__(self,job):
        super(JobThread,self).__init__()
        self.job = job
         
    def run(self):
        RunJob(self.job)
 
#======================================================================

class Analyser(object):
    def __init__(self):
        super(Analyser,self).__init__()
        self.jobs = None
        self.stopping = True
        self.pool = None

    def run(self,listChecker,histograms):
         """
         Main function to be executed when starting the code.
         """
    # global configuration
   # parser = argparse.ArgumentParser( description = 'Analysis Tool using XMLs' )
   # parser.add_argument('-n', '--nWorkers',   default=4,                                 type=int,   help='number of workers' )  
   # parser.add_argument('-p', '--parallel',   default=False,   action='store_const',     const=True, help='enables running in parallel')
   # parser.add_argument('-c', '--configfile', default="Configurations/Configuration.py", type=str,   help='files to be analysed')
   # parser.add_argument('-a', '--analysis',   default=""                               , type=str,   help='overrides the analysis specified in configuration file')
   # parser.add_argument('-s', '--samples',    default=""                               , type=str,   help='string with comma separated list of samples to analyse')
   # parser.add_argument('-o', '--output',     default=""                               , type=str,   help='name of the output directory')
   # args = parser.parse_args()
    
    #configModuleName = "CustomConfiguration"
    #configuration = importlib.import_module(configModuleName)
  
    #checkAnalysis(configuration, args.analysis)
         processingDict = CustomConfiguration.Processes
         print CustomConfiguration.Job["Fraction"]

        
         CustomConfiguration.Job["Batch"] = True
         self.jobs = [BuildJob(CustomConfiguration.Job, processName, fileLocation,listChecker,histograms,self.stopping) for processName, fileLocation in processingDict.items()]
         self.jobs = SortJobsBySize(self.jobs)
         self.pool = mp.ProcessingPool(4)
             # start with n worker processes
         self.pool.map(RunJob, self.jobs)
         
         """jobThreads =[]
         for job in self.jobs:
             jobThread = JobThread(job)
             jobThreads.append(jobThread)
             jobThread.start()
             
         for jobThread in jobThreads:
             jobThread.join()
         """
        
             
        
         print "test2"
         print NewJob.stop
         
  
    #else:
        #for processName, fileLocation in processingDict.items():
         #   RunJob(BuildJob(CustomConfiguration.Job, processName, fileLocation,listChecker,histograms)) 


