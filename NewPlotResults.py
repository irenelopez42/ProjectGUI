import argparse
import sys
import os
import glob
import ROOT
import Plotting.PlotStyle as PS
import Plotting.Paintable as Paintable
import Plotting.Depiction as Depiction
import Plotting.Database  as Database
import importlib
import PlotConf_CustomAnalysis
from collections import OrderedDict
 
def collectPaintables(definition):
    paintables = {}
    for key, item in definition.items():
        if   "Stack" in key: paintables["Stack"] = Paintable.StackPaintable("stack", definition["Stack"])
        elif "data"  in key: paintables["data"]  = Paintable.DataPaintable("data", definition["data"]) 
        else:                paintables[key]     = Paintable.OverlayPaintable(key, definition[key])
    return paintables

def collectDepictions(configuration):
    depictions = []
    definitions = configuration["Definitions"]
    for depiction in configuration["Order"]:
        if definitions[depiction]["type"] == "Main"     : depictions.append(Depiction.MainDepiction(      definitions[depiction], depiction))
        if definitions[depiction]["type"] == "Ratio"    : depictions.append(Depiction.RatioDepiction(     definitions[depiction], depiction))
        if definitions[depiction]["type"] == "Agreement": depictions.append(Depiction.AgreementDepiction( definitions[depiction], depiction))
    return depictions

def initializeDepictions(Depictions):
    n = len(Depictions)
    
    if n == 1:
        Depictions[0].initializeDepiction( 0.0, 0.0, 1.0, 1.0, 0.05, 0.2)        
    elif n == 2:
        Depictions[0].initializeDepiction( 0.0, 0.35, 1.0, 1.0, 0.08,  0.004)
        Depictions[1].initializeDepiction( 0.0, 0.02, 1.0, 0.35, 0.007, 0.05)

    elif n == 3:
        Depictions[0].initializeDepiction( 0.0,  0.5, 1.0,  1.0, 0.1, 0.01)
        Depictions[1].initializeDepiction( 0.0,  0.3, 1.0,  0.5, 0.025, 0.025)
        Depictions[2].initializeDepiction( 0.0,  0.0, 1.0,  0.3, 0.017, 0.5)

    else:
        print "Not Supported Yet"
        sys.exit()
        
    bottomPad = Depictions[-1].pad
    bottomPad.SetBottomMargin(0.1/bottomPad.GetAbsHNDC())

def drawItem(x, y, text, font = 42, size = 0.03, align = 11):
    l = ROOT.TLatex() 
    l.SetNDC();
    l.SetTextAlign(align)                   
    l.SetTextFont(font);
    l.SetTextSize(size)
    l.DrawLatex(x,y,text);

def writeXaxisTitle(Paintables):
    xAxisTitle = Database.histoptions.get("xtitle", Paintables[Paintables.keys()[0]].getHistogram().GetXaxis().GetTitle())
    [p.getHistogram().SetXTitle("") for p in Paintables.values()]
    drawItem(0.95, 0.0675, xAxisTitle, 42, 0.045, 33)
    
def ATLASLabel( x, y):
    drawItem(x    , y,      "ATLAS",              72,  0.03)
    drawItem(x+0.1, y,      "Open Data",          42,  0.03)

def drawLegend(paintables, paintingOrder):
    y1 = 0.92
    y2 = y1 - 0.03*sum([i.getNumberOfLegendItems() for i in paintables.values()])
    legend = ROOT.TLegend(0.70,y1,0.90,y2)  
    legend.SetBorderSize(0)
    for key in paintingOrder:
        paintables[key].addToLegend(legend)
    legend.Draw()
    return legend

def DrawPlot(configuration, histlocation):
    print "Drawing plot: " + histlocation 
    canvas = ROOT.TCanvas( histlocation, "title", 900, 900 )
    
    Paintables = collectPaintables(configuration["Paintables"])
    Depictions = collectDepictions(configuration["Depictions"])
    initializeDepictions(Depictions)

    ATLASLabel(0.2,0.90)
    writeXaxisTitle(Paintables)
    # legend has to be attached to canvas otherwise the garbage collector deletes it
    canvas.legend = drawLegend(Paintables, Depictions[0].PaintingOrder)
    [d.drawDepiction(Paintables) for d in Depictions]

    canvas.SaveAs("Output/" + histlocation+ ".pdf")  
 
#======================================================================
def plot_results(histograms):
    """
    Main function to be executed when starting the code.
    """
    ROOT.gROOT.SetBatch()
    ROOT.TGaxis.SetMaxDigits(4)
    ROOT.TH1.AddDirectory(False)
    PS.setStyle();
    
    #parser = argparse.ArgumentParser( description = 'Plotting Tool using YAML files for configuration' )
    #parser.add_argument('configfile', type=str, help='configuration file to be used')
    #configModuleName = "PlotConf_CustomAnalysis"
    #args = parser.parse_args()
    
    #configModuleName = args.configfile.replace("/", ".").strip(".py")
    configuration = PlotConf_CustomAnalysis.config
    
    for histogram in histograms:
        Database.UpdateDataBase(configuration, histogram)
        DrawPlot(configuration, histogram)
	
    Database.config      = dict()
    Database.histoptions = OrderedDict()
    Database.rootFiles   = dict()
    
#======================================================================   
#if __name__ == "__main__":
#    main( sys.argv[1:] )
