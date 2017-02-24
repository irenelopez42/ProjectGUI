config = {
"Luminosity": 1000,
"InputDirectory": "results",

"Histograms" : {
    "WtMass"             : {"xtitle" : "m_{T}^{W} [GeV]"},
    "etmiss"             : {"xtitle" : "E_{T}^{Miss} [GeV]"},
    "lep_n"              : {"xndiv" : 10},
    "lep_pt"             : {},
    "lep_eta"            : {},
    "lep_E"              : {},
    "lep_phi"            : {"y_margin" : 1},
    "lep_charge"         : {"y_margin" : 1, "xndiv" : 4},
    "lep_type"           : {"y_margin" : 0.5, "xtitle" : "|PDG id|^{lep}"},
    "leadlep_pt"           : {},
    "leadlep_eta"          : {"y_margin" : 0.5},
    "leadlep_E"            : {},
    "leadlep_phi"          : {"y_margin" : 1},
    "leadlep_charge"       : {"y_margin" : 1, "xndiv" : 4},
    "leadlep_type"         : {"y_margin" : 0.5, "xtitle" : "|PDG id|^{leadlep}"},
    "traillep_pt"          : {},
    "traillep_eta"         : {"y_margin" : 0.5},
    "traillep_E"           : {},
    "traillep_phi"         : {"y_margin" : 1},
    "traillep_charge"      : {"y_margin" : 1, "xndiv" : 4},
    "traillep_type"        : {"y_margin" : 0.5, "xtitle" : "|PDG id|^{traillep}"},
    "deltaTheta" 	 : {},
    "invMass"              : {"xtitle" : "m_{ll} [GeV]"},
    "invMass2"              : {"xtitle" : "m_{ll} [GeV]"},
    "WtMass"          : {"xtitle" : "m_{T}^{W} [GeV]"},


   
   # "lep_ptconerel30"    : {},
   # "lep_etconerel20"    : {},
   # "lep_d0"             : {},
   # "lep_z0"             : {},
    "n_jets"             : {"xndiv" : 10},
    "jet_pt"             : {},
    "jet_m"              : {},
    "jet_jvf"            : {"y_margin" : 0.4},
    "jet_eta"            : {"y_margin" : 0.5},
    "jet_MV1"            : {"y_margin" : 0.3},
    "vxp_z"              : {},
   # "pvxp_n"             : {},
},

"Paintables": {
    "Stack": {
        "Order"     : ["WW","WZ","ZZ", "DrellYan", "W", "Z", "stop", "ttbar"],
        "Processes" : {                
            "WW" : {
                "Color"         : "#fa7921",
                "Contributions" : ["WW"]},
            "WZ" : {
                "Color"         : "#fa6021",
                "Contributions" : ["WZ"]},
            "ZZ" : {
                "Color"         : "#fa3021",
                "Contributions" : ["ZZ"]},
                                
            "DrellYan": {       
                "Color"         : "#5bc0eb",
                "Contributions" : ["DYeeM08to15", "DYeeM15to40", "DYmumuM08to15", "DYmumuM15to40", "DYtautauM08to15", "DYtautauM15to40"]},
            
            "W": {              
                "Color"         : "#e55934",
                "Contributions" : ["WenuJetsBVeto", "WenuWithB", "WenuNoJetsBVeto", "WmunuJetsBVeto", "WmunuWithB", "WmunuNoJetsBVeto", "WtaunuJetsBVeto", "WtaunuWithB", "WtaunuNoJetsBVeto"]},
                                
            "Z": {              
                "Color"         : "#086788",
                "Contributions" : ["Zee", "Zmumu", "Ztautau"]},
                  
            "stop": {
                "Color"         : "#fde74c",
                "Contributions" : ["stop_tchan_top", "stop_tchan_antitop", "stop_schan", "stop_wtchan"]},
            
            "ttbar": {
                "Color"         : "#9bc53d",
                "Contributions" : ["ttbar_lep", "ttbar_had"]}
        }
    },

    "data" : {
        "Contributions": ["data_Egamma", "data_Muons"]}
},

"Depictions": {
    "Order": ["Main", "Data/MC"],
    "Definitions" : {
        "Data/MC": {
            "type"       : "Agreement",
            "Paintables" : ["data", "Stack"]
        },
        
        "Main": {
            "type"      : "Main",
            "Paintables": ["Stack", "data"]
        },
    }
},
}
