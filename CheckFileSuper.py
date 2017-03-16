import NewAnalysisHelpers as AH
import itertools 

class CheckFile(object):
    """The base class for checking that a certain condition
    has been fulfilled"""
    
    def __init__(self):
        super(CheckFile,self).__init__()
        
    def check(self,EventObject,histogramDic):
        """checks the condition using the EventObject which contains
        the event information and histogramDic is the dictionary used in 
        custom analysis which may be needed if the check function also
        adds event data into a histogram"""
        
        return True

           
class CheckNJets(CheckFile):
    """checks the number of jets is within nMinJets and 
    nMaxJets"""
    
    def __init__(self, nMinJets,nMaxJets):
        super(CheckNJets,self).__init__()
        self.nMinJets = nMinJets
        self.nMaxJets = nMaxJets

    def check(self,EventObject,histogramDic):
        goodJets = EventObject["jets"]
        if len(goodJets)<self.nMinJets or len(goodJets) > self.nMaxJets:
            return False
        return True
            
class CheckBTag(CheckFile):
    """checks the number of B tagged jets is within minBTag and
    maxBTag"""
    
    def __init__(self,minBTag,maxBTag,histogram):
        super(CheckBTag,self).__init__()
        self.minBTag = minBTag
        self.maxBTag = maxBTag
        self.histogram =histogram        
        
    def check(self,EventObject,histogramDic):
        goodJets = EventObject["jets"]
        btags = sum([1 for jet in goodJets if jet.mv1() > 0.7892])    
        if btags<self.minBTag or btags > self.maxBTag:
            return False 
        histogramDic[self.histogram] = btags
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
    """checks that the transverse missing energy is within EtMissMin and
    EtMissMax"""
    
    def __init__(self,EtMissMin,EtMissMax):
        super(CheckEtMiss,self).__init__()
        self.etmissMin = EtMissMin
        self.etmissMax = EtMissMax
        
        
    def check(self,EventObject,histogramDic):
        EtMiss = EventObject["EtMiss"]
        if self.etmissMin > EtMiss.et() or self.etmissMax < EtMiss.et():
            return False
        return True
        
class CheckLepCharge(CheckFile):
    """Checks if the charges in the first and second postition of the 
    lepton list are the same or different depending on the specified condition"""
    
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
    """Checks if the flavours in the first and second postition of the 
    lepton list are the same or different depending on the specified condition"""
    
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
    """Checks that the transverse mass of the num lepton with the missing 
    momentum is within minMass and maxMass"""
    
    def __init__(self,minMass,maxMass,num,histogram):
        super(CheckTMass,self).__init__()
        self.minMass = minMass
        self.maxMass = maxMass
        self.num = num
        self.histogram = histogram
        
    def check(self,EventObject,histogramDic):
        etmiss = EventObject["EtMiss"]
        lepton = EventObject["leptons"][self.num]
        mass =AH.WTransverseMass(lepton,etmiss)
        if mass >= self.minMass and mass <=self.maxMass:   
            histogramDic[self.histogram] = mass
            return True
        else:
            return False
 

class CheckAngle(CheckFile):
    """Checks that the angle between the lepton closest to the missing 
    momentum is at least minAng. The histogram in the constructor is the 
    name of the one which will be drawn with these angles"""
    
    def __init__(self,minAng,histogram):
        super(CheckAngle,self).__init__()
        self.angle=float("inf")
        self.histogram = histogram
        self.minAng = minAng

    def check(self,EventObject,histogramDic):
        leptons = EventObject["leptons"]
        etmiss = EventObject["EtMiss"]
        self.angle  =float("inf") # infinite initial smallest angle

        # tlv() is the four vector and Vect() returns the 3 momentum vector
        #component. Angle() with a three vector argument finds the 
        #angle of the three vector component of the four vector with the 
        #three vector.
        #The code goes through each lepton and finds the one whose angle 
        #gives the smallest value
        for lepton in leptons:
            angle = abs(lepton.tlv().Angle(etmiss.tlv().Vect())) 
            if self.angle > angle:
                self.angle = angle
           
        if self.minAng > self.angle:
            return False
        else:
            histogramDic[self.histogram] = self.angle
        return True
        
class CheckLepEta(CheckFile):
    """Checks that each lepton eta value in an event is within minEta and
    maxEta. If switch is one true then the angles must be outside of the 
    range"""

    def __init__(self,minEta,maxEta,switch):
        super(CheckLepEta,self).__init__()
        self.minEta = minEta
        self.maxEta = maxEta
        self.switch = switch
        
    def check(self,EventObject,histogramDic):
        leptons = EventObject["leptons"]
        for lepton in leptons:
            if lepton.eta() < self.minEta or lepton.eta() > self.maxEta:
                if not self.switch:
                    return False
        if self.switch:
            return False
        return True
        
def InvariantMass(lepton1,lepton2):
    return (lepton1.tlv()+lepton2.tlv()).M()

def TestLeptonCandidate(lepton1,lepton2,mass):
    return abs(InvariantMass(lepton1,lepton2)-mass)
    
def TestDoubleLepton(lepton1,lepton2,lepton3,lepton4,mass1,mass2):
    return abs(InvariantMass(lepton1,lepton2)-mass1)
    +abs(InvariantMass(lepton3,lepton4)-mass2)
        
class CheckInvMass(CheckFile):
    """checks that the invariant mass of the first and second lepton 
    in the lepton list is within mrange of mass"""
    
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
        
        if abs(invMass-self.mass)<self.mrange: 
            histogramDic[self.histogram] = invMass 
            return True
        else:
            return False
         
def BestThreeCandidate(EventObject,histogramDic,mass,checks):
    """finds the lepton pair whose mass is closest to mass and that also
    satisfy the checks. The checks that are supported are the lepton flavour
    and the lepton charge"""     
    
    bestCandidate = None
    leptons = EventObject["leptons"]
    for p in itertools.permutations([0,1,2],3): #all possible lepton pairs
        for check in checks:
            #check.first and check.second are the first and second 
            #leptons used in the flavour or charge check
            check.first = p[0] 
            check.second = p[1]
            if not check.check(EventObject,histogramDic):
                break
        if bestCandidate is None:
            #bestCandidate is the permutation which is what actually will be 
            #returned but currentValue and previousBestValue are the mass 
            #differences from the invariant mass specified
            bestCandidate = p
            previousBestValue = TestLeptonCandidate(leptons[p[0]],leptons[p[1]],mass)
            
        currentValue = TestLeptonCandidate(leptons[p[0]],leptons[p[1]],mass)
        if currentValue<previousBestValue:
            bestCandidate = p
            previousBestValue = currentValue
            
    return bestCandidate
		
class CheckThreeLepton(CheckFile):
    """finds the best candidate for three leptons and ensures
    they satisfy the checks and also have a mass of mass within mrange. minMass
    and maxMass are the minimum and maximum transverse masses of the extra lepton
    , respectively. Thistogram is the transverse mass histogram. Histogram is 
    the invariant mass histogram. Checks are the flavour and mass checks"""

    def __init__(self,histogram,mass,mrange,minMass,maxMass,Thistogram,checks):
        super(CheckThreeLepton,self).__init__()
        self.mass = mass
        self.mrange = mrange
        self.checks = checks
        self.minMass = minMass
        self.maxMass = maxMass
        self.histogram = histogram
        self.Thistogram = Thistogram
        

    def check(self,EventObject,histogramDic):
        bestThree = BestThreeCandidate(EventObject,histogramDic,self.mass,self.checks)
        candidate = bestThree
        
        if candidate is None: 
            return False
            
        if self.Thistogram is None:
            pass
        else:
            #candidate[2] as the first and second leptons are the Z leptons
            Tcheck = CheckTMass(self.minMass,self.maxMass,candidate[2],self.Thistogram)	
            if Tcheck.check(EventObject,histogramDic) is False:
                return False
        InvCheck = CheckInvMass(self.mass,self.mrange,candidate[0],candidate[1],self.histogram)
        if InvCheck.check(EventObject,histogramDic) is False:
            return False 
        return True

def BestFourCandidate(EventObject,histogramDic,mass1,mass2,checks):
    """finds the best pairs whose mass is closest to mass1 and mass2, respectively, 
    and also satisfies the checks. This is similar to the 3 lepton case. Checks
    are currently the flavour and charge checks"""
    
    bestCandidate = None
    leptons = EventObject["leptons"]
    for p in itertools.permutations([0,1,2,3],4):
        for checktype in checks:
            checktype.first = p[0]
            checktype.second = p[1]
            if not checktype.check(EventObject,histogramDic):
                break
            checktype.first = p[2]
            checktype.second = p[3]
            if not checktype.check(EventObject,histogramDic):
                break
        if bestCandidate is None:
            bestCandidate = p
            previousBestValue = TestDoubleLepton(leptons[p[0]],leptons[p[1]],
                                                     leptons[p[2]],leptons[p[3]],mass1,mass2)
            
        currentValue = TestDoubleLepton(leptons[p[0]],leptons[p[1]],
                                                leptons[p[2]],leptons[p[3]],mass1,mass2)           
        if currentValue <previousBestValue:
            bestCandidate = p
            previousBestValue = currentValue
    return bestCandidate
    
class CheckFourLepton(CheckFile):
    """finds the best candidate for two lepton pairs whose masses are closest 
    to mass1 and mass2, repsectively, and within mrange of the mass. histogram1
    and histogram2 are the invariant mass histograms of the first and second
    histograms. Checks are currently the flavour and charge checks"""
        
    def __init__(self,histogram1,histogram2,mass1,mass2,mrange,checks):
        self.mass1 = mass1
        self.mass2 = mass2
        self.mrange = mrange
        self.histogram1 = histogram1
        self.histogram2 = histogram2
        self.checks = checks
        self.count = 0
        
    def check(self,EventObject,histogramDic):
        candidate = BestFourCandidate(EventObject,histogramDic,self.mass1,
                                      self.mass2,self.checks)
        if candidate is None: 
            return False
            
        InvCheck1 = CheckInvMass(self.mass1,self.mrange,candidate[0],candidate[1],
                                 self.histogram1)
        if InvCheck1.check(EventObject,histogramDic) is False:
            return False
        
        InvCheck2 = CheckInvMass(self.mass2,self.mrange,candidate[2],candidate[3],
                                 self.histogram2)
        if InvCheck2.check(EventObject,histogramDic) is False:
            return False
            
        return True
        

  
	
	

	
		

	
	

        

