import NewAnalysisHelpers as AH
import itertools 


class CheckFile(object):
    """The base class for checking that a certain condition
    has been fulfilled"""
    
    def __init__(self):
        super(CheckFile,self).__init__()
        
    def check(self,EventObject,histogramDic):
        """does the checking"""
        return True

           
class CheckNJets(CheckFile):
    """checking the number of jets"""
    
    def __init__(self, nJets):
        super(CheckNJets,self).__init__()
        self.nJets = nJets

    def check(self,EventObject,histogramDic):
        goodJets = EventObject["jets"]
        if not len(goodJets)==self.nJets:
            return False
	return True
            
class CheckBTag(CheckFile):
    """checking the minimum number of B tagged jets"""
    
    def __init__(self,numBTag):
        super(CheckBTag,self).__init__()
        self.numBTag = numBTag

    def check(self,EventObject,histogramDic):
        goodJets = EventObject["jets"]
        btags = sum([1 for jet in goodJets if jet.mv1() > 0.7892])    
        if btags<self.numBTag:
            return False 
        return True
            
class CheckNLep(CheckFile):
    """checking the number of leptons"""
    
    def __init__(self,numJets):
        super(CheckNLep,self).__init__()
        self.nLep = numJets
        
    def check(self,EventObject,histogramDic):
        leptons = EventObject["leptons"]
        if not len(leptons) == self.nLep:
            return False
        return True
        
class CheckEtMiss(CheckFile):
    """checking the minimum transverse missing momentum"""
    
    def __init__(self,EtMiss):
        super(CheckEtMiss,self).__init__()
        self.etmiss = EtMiss
        
    def check(self,EventObject,histogramDic):
        EtMiss = EventObject["EtMiss"]
        if self.etmiss >= EtMiss.et():
            return False
        return True
        
class CheckLepCharge(CheckFile):
    """checks if the charges are same or opposite"""
    
    def __init__(self,condition,first,second):
        super(CheckLepCharge,self).__init__()
        self.condition = condition
	self.first = first
	self.second = second
        
    def check(self,EventObject,histogramDic):
        leptons = EventObject["leptons"]
        boolCon = True if self.condition == "same" else False        
        
        if leptons[self.first].charge()*leptons[self.second].charge()>0 == boolCon:
            return True
        else:
            return False
            
class CheckLepFlavour(CheckFile):
    """checks if the lepton flavours are the same"""
    
    def __init__(self,condition,first,second):
        super(CheckLepFlavour, self).__init__()
        self.condition = condition
	self.first = first
	self.second = second
        
    def check(self,EventObject,histogramDic):
        leptons = EventObject["leptons"]
        boolCon = True if self.condition == "same" else False
        
        if (leptons[self.first].pdgId() ==leptons[self.second].pdgId())== boolCon:
            return True
        
        else:
            return False
            
class CheckTMass(CheckFile):
    """checks the minimum transverse momentum"""
    
    def __init__(self,minMass,num,histogram):
        super(CheckTMass,self).__init__()
        self.minMass = minMass
        self.num = num
        self.histogram = histogram
        
    def check(self,EventObject,histogramDic):
        etmiss = EventObject["EtMiss"]
        lepton = EventObject["leptons"][self.num]
        mass =AH.WTransverseMass(lepton,etmiss)
        if mass > self.minMass:   
            histogramDic[self.histogram] = mass
            return True
        else:
            return False
 

class CheckAngle(CheckFile):
    """checks angle between lepton and momentum"""
    
    def __init__(self,minAng,histogram):
        super(CheckAngle,self).__init__()
        self.angle=float("inf")
        self.histogram = histogram
        self.minAng = minAng

    def check(self,EventObject,histogramDic):
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
            histogramDic[self.histogram] = self.angle
        return True

def InvariantMass(lepton1,lepton2):
    return (lepton1.tlv()+lepton2.tlv()).m()

def TestLeptonCandidate(lepton1,lepton2,mass):
    return abs(InvariantMass(lepton1,lepton2)-mass)
    
def TestDoubleLepton(lepton1,lepton2,lepton3,lepton4,mass):
    return abs(InvariantMass(lepton1,lepton2)-mass)
    +abs(InvariantMass(lepton3,lepton4)-mass)
        
class CheckInvMass(CheckFile):
    
    def __init__(self,mass,mrange,first,second,histogram):
        super(CheckInvMass,self).__init__()
        self.mass = mass
        self.histogram = histogram
        self.first = first
        self.second = second
        self.mrange = mrange
    
    def check(self,EventObject,histogramDic):
        leptons = EventObject["leptons"]
        lepton1 = leptons[self.first]
        lepton2 = leptons[self.second]
        
        invMass = InvariantMass(lepton1,lepton2)
        
        if invMass<self.mrange:
            histogramDic[self.histogram]
            return True
        else:
            return False
         
def BestThreeCandidate(EventObject,histogramDic,mass,*checks):
    bestCandidate = None
    leptons = EventObject["leptons"]
    for p in itertools.permutations([0,1,2],3):
        for check in checks:
            check.self.first, check.self.second = p[0],p[1]
            if not check.check(EventObject,histogramDic):
                break
            if bestCandidate is None:
                bestCandidate = p
                previousCandidate = TestLeptonCandidate(leptons[p[0]],leptons[p[1]],mass)
            
            currentCandidate = TestLeptonCandidate(leptons[p[0]],leptons[p[1]],mass)
            if currentCandidate <previousCandidate:
                bestCandidate = p
                previousCandidate = currentCandidate
            
            return bestCandidate
		
class CheckThreeLepton(CheckFile):
    """gets the best candidate for three leptons"""

    def __init__(self,histogram,mass,mrange,minMass,Thistogram,*checks):
        super(CheckThreeLepton,self).__init__()
        self.mass = mass
        self.mrange = mrange
        self.checks = checks
        self.minMass = minMass
        self.histogram = histogram
        self.Thistogram = Thistogram

    def check(self,EventObject,histogramDic):
        bestThree = BestThreeCandidate(EventObject,self.histogramDic,self.mass,self.checks)
        candidate = bestThree
        
        if candidate is None: return False
    
        if self.Thistogram is None:
            pass
        else:
            Tcheck = CheckTMass(self.minMass,candidate[2],self.Thistogram)	
            if Tcheck.check(EventObject,histogramDic) is False:
                return False
                
        InvCheck = CheckInvMass(self.mass,self.mrange,candidate[0],candidate[1],self.histogram)
        if InvCheck.check(EventObject,histogramDic) is False:
            return False 
        return True

def BestFourCandidate(EventObject,histogramDic,mass1,mass2,checks):
    bestCandidate = None
    leptons = EventObject["leptons"]
    for p in itertools.permutations([0,1,2,3],3):
        for checktype in checks:
            checktype.self.first, checktype.self.second = p[0],p[1]
            if not checktype.check(EventObject,histogramDic):
                break
            checktype.self.first, checktype.self.second = p[2],p[3]
            if not checktype.check(EventObject,histogramDic):
                break
            if bestCandidate is None:
                bestCandidate = p
                previousCandidate = TestDoubleLepton(leptons[p[0]],leptons[p[1]],
                                                     leptons[p[2]],leptons[p[3]],mass1)
            
            currentCandidate = TestDoubleLepton(leptons[p[0]],leptons[p[1]],
                                                leptons[p[2]],leptons[p[3]],mass2)           
            if currentCandidate <previousCandidate:
                bestCandidate = p
                previousCandidate = currentCandidate
            return bestCandidate
    
class CheckFourLepton(CheckFile):
    """gets the best candidate for four leptons"""
        
    def __init__(self,histogram1,histogram2,mass1,mass2,mrange,*checks):
        self.mass1 = mass1
        self.mass2=mass2
        self.mrange = mrange
        self.histogram1 = histogram1
        self.histogram2 = histogram2
        self.checks = checks
        
    def check(self,EventObject,histogramDic):
        candidate =BestFourCandidate(EventObject,histogramDic,self.mass,self.mass2,self.checks)
        
        if candidate is None: return False
            
        InvCheck1 = CheckInvMass(self.mass1,self.mrange,candidate[0],candidate[1],self.histogram1)
        if InvCheck1.check(EventObject,histogramDic) is False:
            return False
        
        InvCheck2 = CheckInvMass(self.mass2,self.mrange,candidate[2],candidate[3],self.histogram2)
        if InvCheck2.check(EventObject,histogramDic) is False:
            return False
            
        return True

  
	
	

	
		

	
	

        

