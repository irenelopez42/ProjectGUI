import Analysis.AnalysisHelpers as AH
import copy


class CheckFile(object):
    """The base class for checking that a certain condition
    has been fulfilled"""
    
    def __init__(self):
        super(CheckFile,self).__init__()
        
    def check(self,EventObject):
        """does the checking"""
        return None
        
    def plot(self,histogram,EventObject):
        """plots anything necessary"""
        pass
           
class CheckNJets(CheckFile):
    """checking the number of jets"""
    
    def __init__(self, nJets):
        super(CheckNJets,self).__init__()
        self.nJets = nJets

    def check(self,EventObject):
        goodJets = EventObject["jets"]
        if not len(goodJets)==self.nJets:
            return False
	
	return True
            
class CheckBTag(CheckFile):
    """checking the minimum number of B tagged jets"""
    
    def __init__(self,numBTag):
        super(CheckBTag,self).__init__()
        self.numBTag = numBTag

    def check(self,EventObject):
        goodJets = EventObject["jets"]
        btags = sum([1 for jet in goodJets if jet.mv1() > 0.7892])        
        if not btags>=self.numBTag:
            return False
        return None
            
class CheckNLep(CheckFile):
    """checking the number of leptons"""
    
    def __init__(self,numJets):
        super(CheckNLep,self).__init__()
        self.nLep = numJets
        
    def check(self,EventObject):
        leptons = EventObject["leptons"]
        if not len(leptons) == self.nLep:
            return False
        return None
        
class CheckEtMiss(CheckFile):
    """checking the minimum transverse missing momentum"""
    
    def __init__(self,EtMiss):
        super(CheckEtMiss,self).__init__()
        self.etmiss = EtMiss
        
    def check(self,EventObject):
        EtMiss = EventObject["EtMiss"]
        if self.etmiss >= EtMiss.et():
            return False
        return None
        
class CheckLepCharge(CheckFile):
    """checks if the charges are same or opposite"""
    
    def __init__(self,condition):
        super(CheckLepCharge,self).__init__()
        self.condition = condition
        
    def check(self,EventObject):
        leptons = EventObject["leptons"]
        boolCon = True if self.condition == "same" else False        
        
        if leptons[0].charge()*leptons[0].charge()>0 == boolCon:
            return None
        else:
            return False
            
class CheckLepFlavour(CheckFile):
    """checks if the lepton flavours are the same"""
    
    def __init__(self,condition):
        super(CheckLepFlavour, self).__init__()
        self.condition = condition
        
    def check(self,EventObject):
        leptons = EventObject["leptons"]
        boolCon = True if self.condition == "same" else False
        
        if (leptons[0].pdgId() ==leptons[1].pdgId())== boolCon:
            return None
        
        else:
            return False
            
class CheckTMass(CheckFile):
    """checks the minimum lepton momentum"""
    
    def __init__(self,minMass,num,histogram):
        super(CheckTMass,self).__init__()
        self.minMass = minMass
        self.num = num
        self.histogram = histogram
        
    def check(self,EventObject):
        etmiss = EventObject["EtMiss"]
        lepton = EventObject["leptons"][self.num]
        if AH.WTransverseMass(lepton,etmiss) > self.minMass:
            return self.histogram
        else:
            return False
            
    def plot(self,EventObject,histogram,weight):
        lepton = EventObject["leptons"][self.num]
        etmiss = EventObject["EtMiss"]
        histogram.Fill(AH.WTransverseMass(lepton,etmiss),weight)
            

        
        
        

