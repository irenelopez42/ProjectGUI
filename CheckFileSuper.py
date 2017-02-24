
class CheckFile(object):
    """The base class for checking that a certain condition
    has been fulfilled"""
    
    def __init__(self):
        super(CheckFile,self).__init__()
        
    def check(self,EventObject):
        """does the checking"""
        
        return True
           
class CheckNJets(CheckFile):
    """checking the number of jets"""
    
    def __init__(self, nMinJets,nMaxJets):
        super(CheckNJets,self).__init__()
        self.nMinJets = nMinJets
        self.nMaxJets = nMaxJets

    def check(self,EventObject):
        goodJets = EventObject["jets"]
        if len(goodJets)<self.nMinJets or len(goodJets) > self.nMaxJets:
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
        return True
            
class CheckNLep(CheckFile):
    """checking the number of leptons"""
    
    def __init__(self,numJets):
        super(CheckNLep,self).__init__()
        self.nLep = numJets
        
    def check(self,EventObject):
        leptons = EventObject["leptons"]
        if not len(leptons) == self.nLep:
            return False
        return True
        
class CheckEtMiss(CheckFile):
    """checking the minimum transverse missing momentum"""
    
    def __init__(self,EtMissMin,EtMissMax):
        super(CheckEtMiss,self).__init__()
        self.etmissMin = EtMissMin
        self.etmissMax = EtMissMax
        
    def check(self,EventObject):
        EtMiss = EventObject["EtMiss"]
        if self.etmissMin > EtMiss.et() or self.etmissMax < EtMiss.et():
            return False
        return True
        
        
        

