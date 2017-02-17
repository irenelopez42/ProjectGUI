import NewAnalysisHelpers as AH
import copy
import itertools 


class CheckFile(object):
    """The base class for checking that a certain condition
    has been fulfilled"""
    
    def __init__(self):
        super(CheckFile,self).__init__()
        
    def check(self,EventObject):
        """does the checking"""
        return None
        
    def add(self,histogramDic,EventObject):
        """adds to dictionary anything necessary"""
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
	return None
            
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
    
    def __init__(self,condition,first,second):
        super(CheckLepCharge,self).__init__()
        self.condition = condition
	self.first = first
	self.second = second
        
    def check(self,EventObject):
        leptons = EventObject["leptons"]
        boolCon = True if self.condition == "same" else False        
        
        if leptons[self.first].charge()*leptons[self.second].charge()>0 == boolCon:
            return None
        else:
            return False
            
class CheckLepFlavour(CheckFile):
    """checks if the lepton flavours are the same"""
    
    def __init__(self,condition,first,second):
        super(CheckLepFlavour, self).__init__()
        self.condition = condition
	self.first = first
	self.second = second
        
    def check(self,EventObject):
        leptons = EventObject["leptons"]
        boolCon = True if self.condition == "same" else False
        
        if (leptons[self.first].pdgId() ==leptons[self.second].pdgId())== boolCon:
            return None
        
        else:
            return False
            
class CheckTMass(CheckFile):
    """checks the minimum transverse momentum"""
    
    def __init__(self,minMass,num,histogram):
        super(CheckTMass,self).__init__()
        self.minMass = minMass
        self.num = num
        self.histogram = histogram
	self.Tmass
        
    def check(self,EventObject):
        etmiss = EventObject["EtMiss"]
        lepton = EventObject["leptons"][self.num]
        if AH.WTransverseMass(lepton,etmiss) > self.minMass:
	    self.Tmass =AH.WTransverseMass(lepton,etmiss)
            return self.histogram
        else:
            return False
            
    def add(self,histogramDic,EventObject):
        lepton = EventObject["leptons"][self.num]
        etmiss = EventObject["EtMiss"]
        histogramDic[self.histogram] = self.Tmass

class CheckAngle(CheckFile):
    """checks angle between lepton and momentum"""
    
    def __init__(self,minAng,histogram):
        super(CheckAngle,self).__init__()
	self.angle=float("inf")
	self.histogram = histogram
	self.minAng = minAng

    def check(self,EventObject):
 	leptons = EventObject["leptons"]
	etmiss = EventObject["EtMiss"]
	self.angle  =float("inf")

	for lepton in leptons:
	    angle = abs(lepton.tlv().Angle(etmiss.tlv().Vect()))
	    if self.angle > angle:
		self.angle = angle
	if self.minAng > self.angle:
	    return False
	else:
	    return self.histogram
		
    def add(self,histogramDic,EventObject):
	histogramDic[self.histogram] = self.angle


	
def TestLeptonCandidate(lepton1,lepton2,mass):
    return abs(InvariantMass(lepton1,lepton2)-mass)

def InvariantMass(lepton1,lepton2):
    return (lepton1.tlv()+lepton2.tlv()).m()
        

def BestThreeCandidate(leptons,mass,checks*)

    bestCandidate = None
    Tcheck = None	
    for p in itertools.permutations([0,1,2],3):
        for check in checks:
   	    if isinstance(check,CheckTMass):
		Tcheck = check
		continue
	    else:
	        check.first,check.second = p[0],p[1]
	    if not check(self,EventObject):
		break
	if bestCandidate is None
	    bestCandidate =p
	    previousCandidate = TestLeptonCandidate(leptons[p[0]],leptons[p[1]],self.mass)
	
	currentCandidate = TestLeptonCandidate(leptons[p[0]],leptons[p[1]],mass)
	if  currentCandidate < previousCandidate:
   	    bestCandidate = p
	    previousCandidate = currentCandidate
	
	Tcheck.num = p[2]
	return [bestCandidate,Tcheck]
		
class CandidateThreeLepton(CheckFile):
    """gets the best candidate for three leptons"""

    def __init__(self,histogram,mass,mrange, checks*):
	self.mass = mass
	self.mrange = mrange
	self.checks = checks
	self.histogram = histogram
	self.Tcheck = None
	self.Thistogram = None	
	self.cand = None

    def check(self,EventObject):
	leptons = EventObject["leptons"]
	bestThree = BestThreeCandidate(leptons,self.mass,self.checks)
	self.cand = bestThree[0]
	self.Tcheck = bestThree[1]

	if cand is None: return False
	
	z1Lepton = candidate[0]
	z2Lepton = candidate[1]
	wLepton = candidate[2]


	Tcheck = self.Tcheck.check(EventObject)	
	if Tcheck is False:
	    return False
	else: 
	    self.Thistogram = Tcheck
	
	if abs(TestLeptonCandidate(cand[0],cand[1],mass))>self.mrange:
	    return False

	return self.histogram

    def add(self,histogramDic,EventObject)
	leptons = EventObject["leptons"]
	etmiss = EventObject["EtMiss"]
		

	histogramDic[self.histogram] = InvariantMass(leptons[cand[0]],leptons[cand[1]])
	histogramDic[self.Thistogram] = AH.WTransverseMass(leptons[cand[2]],etmiss)
	
	
	

	
		

	
	

        

