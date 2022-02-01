#!/usr/bin/env python
import sys, os
import os.path
import ntpath
import importlib
import ROOT
import copy
import re

#__________________________________________________________
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

#__________________________________________________________
def mapHistos(var, label, sel, param):
    print ('run plots for var:{}     label:{}     selection:{}'.format(var,label,sel))
    signal=param.plots[label]['signal']
    backgrounds=param.plots[label]['backgrounds']

    hsignal = {}
    for s in signal:
        hsignal[s]=[]
        for f in signal[s]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(var)
                hh = copy.deepcopy(h)
                #scaleSig=1.
                if hh.GetSumOfWeights()!=0.:
                    scaleSig=1./hh.GetSumOfWeights()
                else:
                    scaleSig=1.
                try:
                    scaleSig=param.scaleSig
                except AttributeError:
                    print ('no scale signal, using 1')
                if scaleSig != 0.:
                    hh.Scale(scaleSig) 
                #hh.Scale(param.intLumi*scaleSig)
                #hh.Scale(scaleSig)
                if len(hsignal[s])==0:
                    hsignal[s].append(hh)
                else:
                    hh.Add(hsignal[s][0])
                    hsignal[s][0]=hh


    hbackgrounds = {}
    for b in backgrounds:
        hbackgrounds[b]=[]
        for f in backgrounds[b]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(var)
                hh = copy.deepcopy(h)
                if hh.GetSumOfWeights()!=0.:
                    scale=1./hh.GetSumOfWeights()
                else:
                    scale=1.
                try:
                    scale=param.scaleBack
                except AttributeError:
                    print ('no scale background, using 1')
                if scale != 0.:
                    hh.Scale(scale)
                print('entries ', hh.GetEntries())
                #hh.Scale(param.intLumi)
                if len(hbackgrounds[b])==0:
                    hbackgrounds[b].append(hh)
                else:
                    hh.Add(hbackgrounds[b][0])
                    hbackgrounds[b][0]=hh

    for s in hsignal:
        if len(hsignal[s])==0:
            hsignal=removekey(hsignal,s)

    for b in hbackgrounds:
        if len(hbackgrounds[b])==0:
            hbackgrounds=removekey(hbackgrounds,b)

    return hsignal,hbackgrounds


#__________________________________________________________
def mapEffHistos(denVar, numVar, label, sel, param):
    print ('run efficiency plots for denVar:{}  numVar:{}   label:{}     selection:{}'.format(denVar,numVar,label,sel))
    signal=param.plots[label]['signal']
    backgrounds=param.plots[label]['backgrounds']

    hsignal = {}
    for s in signal:
        hsignal[s]=[]
        for f in signal[s]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                denh=tf.Get(denVar)
                denhh = copy.deepcopy(denh)

                numh=tf.Get(numVar)
                numhh = copy.deepcopy(numh)

                #don't scale histograms

                numhh.Divide(denhh)
                if len(hsignal[s])==0:
                    hsignal[s].append(numhh)
                else:
                    hh.Add(hsignal[s][0])
                    hsignal[s][0]=numhh


    hbackgrounds = {}
    for b in backgrounds:
        hbackgrounds[b]=[]
        for f in backgrounds[b]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                denh=tf.Get(denVar)
                denhh = copy.deepcopy(denh)

                numh=tf.Get(numVar)
                numhh = copy.deepcopy(numh)

                #don't scale histograms

                numhh.Divide(denhh)
                if len(hbackgrounds[b])==0:
                    hbackgrounds[b].append(numhh)
                else:
                    hh.Add(hbackgrounds[b][0])
                    hbackgrounds[b][0]=numhh

    for s in hsignal:
        if len(hsignal[s])==0:
            hsignal=removekey(hsignal,s)

    for b in hbackgrounds:
        if len(hbackgrounds[b])==0:
            hbackgrounds=removekey(hbackgrounds,b)

    return hsignal,hbackgrounds

#__________________________________________________________
def runPlots(var,param,hsignal,hbackgrounds,extralab):
    legsize = 0.04*(len(hbackgrounds)+len(hsignal))
    #leg = ROOT.TLegend(0.58,0.86 - legsize,0.86,0.88)
    leg = ROOT.TLegend(0.18,0.66 - legsize,0.46,0.68)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

    for s in hsignal:
        leg.AddEntry(hsignal[s][0],param.legend[s],"l")
    for b in hbackgrounds:
        leg.AddEntry(hbackgrounds[b][0],param.legend[b],"f")
 

    histos=[]
    colors=[]

    for s in hsignal:
        histos.append(hsignal[s][0])
        colors.append(param.colors[s])

    for b in hbackgrounds:
        histos.append(hbackgrounds[b][0])
        colors.append(param.colors[b])

    intLumiab = param.intLumi/1e+06 

    
    lt = "FCC-hh Simulation (Delphes)"    
    rt = "#sqrt{{s}} = {:.1f} TeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    if 'ee' in param.collider:
        lt = "FCC-ee Simulation (Delphes)"
        rt = "#sqrt{{s}} = {:.1f} GeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    if 'stack' in param.stacksig:
        if 'lin' in param.yaxis:
            drawStack(var+"_stack_lin", 'Events', leg, lt, rt, param.formats, param.outdir, False , True , histos, colors, param.ana_tex, extralab)
        if 'log' in param.yaxis:
            drawStack(var+"_stack_log", 'Events', leg, lt, rt, param.formats, param.outdir, True , True , histos, colors, param.ana_tex, extralab)
        if 'lin' not in param.yaxis and 'log' not in param.yaxis:
            print ('unrecognised option in formats, should be [\'lin\',\'log\']'.format(param.formats))

    if 'nostack' in param.stacksig:
        if 'lin' in param.yaxis:
            drawStack(var+"_nostack_lin", 'Events', leg, lt, rt, param.formats, param.outdir, False , False , histos, colors, param.ana_tex, extralab)
        if 'log' in param.yaxis:
            drawStack(var+"_nostack_log", 'Events', leg, lt, rt, param.formats, param.outdir, True , False , histos, colors, param.ana_tex, extralab)
        if 'lin' not in param.yaxis and 'log' not in param.yaxis:
            print ('unrecognised option in formats, should be [\'lin\',\'log\']'.format(param.formats))
    if 'stack' not in param.stacksig and 'nostack' not in param.stacksig:
        print ('unrecognised option in stacksig, should be [\'stack\',\'nostack\']'.format(param.formats))



#__________________________________________________________
def runEffPlots(denVar,numVar,param,hsignal,hbackgrounds,extralab):
    legsize = 0.04*(len(hbackgrounds)+len(hsignal))
    #leg = ROOT.TLegend(0.58,0.86 - legsize,0.86,0.88)
    leg = ROOT.TLegend(0.18,0.66 - legsize,0.46,0.68)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

    for s in hsignal:
    #    leg.AddEntry("")
        leg.AddEntry(hsignal[s][0],param.legend[s],"l")
    for b in hbackgrounds:
    #    leg.AddEntry("")
        leg.AddEntry(hbackgrounds[b][0],param.legend[b],"f")

    histos=[]
    colors=[]

    for s in hsignal:
        histos.append(hsignal[s][0])
        colors.append(param.colors[s])

    for b in hbackgrounds:
        histos.append(hbackgrounds[b][0])
        colors.append(param.colors[b])

    intLumiab = param.intLumi/1e+06

    lt = "FCC-hh Simulation (Delphes)"
    rt = "#sqrt{{s}} = {:.1f} TeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    if 'ee' in param.collider:
        lt = "FCC-ee Simulation (Delphes)"
        rt = "#sqrt{{s}} = {:.1f} GeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    if 'lin' in param.yaxis:
        drawEffPlots("eff_"+denVar+"_"+numVar+"_lin", 'Reco/Gen Efficiency', leg, lt, rt, param.formats, param.outdir, False , True , histos, colors, param.ana_tex, extralab)
    if 'log' in param.yaxis:
        drawEffPlots("eff_"+denVar+"_"+numVar+"_log", 'Reco/Gen Efficiency', leg, lt, rt, param.formats, param.outdir, True , True , histos, colors, param.ana_tex, extralab)
    if 'lin' not in param.yaxis and 'log' not in param.yaxis:
        print ('unrecognised option in formats, should be [\'lin\',\'log\']'.format(param.formats))


#_____________________________________________________________________________________________________________
def drawStack(name, ylabel, legend, leftText, rightText, formats, directory, logY, stacksig, histos, colors, ana_tex, extralab):

    canvas = ROOT.TCanvas(name, name, 600, 600) 
    canvas.SetLogy(logY)
    canvas.SetTicks(1,1)
    canvas.SetLeftMargin(0.1)
    canvas.SetRightMargin(0.1)
 

    # first retrieve maximum 
    sumhistos = histos[0].Clone()
    iterh = iter(histos)
    next(iterh)


    try:
        histos[1]
    except IndexError:
        histos1_exists = False
    else:
        histos1_exists = True

    xAxisLabel = histos[0].GetXaxis().GetTitle()
    unitBeginIndex = xAxisLabel.find(" [")
    unitEndIndex = xAxisLabel.endswith("]")
    width = str(histos[0].GetXaxis().GetBinWidth(1))

    if unitBeginIndex is not -1 and unitEndIndex is not -1: #x axis has a unit
        ylabel += " / " + width + " " + xAxisLabel[unitBeginIndex+2:-1]
    else:
        ylabel += " per bin (" + width + " width)"

        
    for h in iterh:
      sumhistos.Add(h)

    maxh = histos[0].GetMaximum()
    minh = histos[0].GetMinimum()

    if logY: 
       canvas.SetLogy(1)

    # define stacked histo
    #hStack = ROOT.THStack("hstack","")

    # first plot backgrounds

    #if(histos1_exists):
    #    histos[1].SetLineWidth(0)
    #    histos[1].SetFillColor(colors[1])
    
    #    hStack.Add(histos[1])
    

    # now loop over other background (skipping first)
    #iterh = iter(histos)
    #next(iterh)
    #if(histos1_exists):
    #    next(iterh)
    
    k = 0
    for h in histos:
       h.SetLineWidth(3)
       #h.SetLineColor(ROOT.kBlack)
       h.SetLineColor(colors[k])
       #h.SetFillColor(colors[k])
       #hStack.Add(h)
       k += 1
    
    
    # finally add signal on top
    #histos[0].SetLineWidth(3)
    #histos[0].SetLineColor(colors[0])
    
    #if stacksig:
    #    hStack.Add(histos[0])

    #hStack.Draw("hist")


    # fix names if needed
    if(histos1_exists):
        xlabel = histos[1].GetXaxis().GetTitle()
        if xlabel.find('m_{RSG}')>=0 : xlabel = xlabel.replace('m_{RSG}','m_{G_{RS}}')
        ## remove/adapt X title content (should be done in config)
        fix_str=" (pf04)"
        if xlabel.find(fix_str)>=0 : xlabel = xlabel.replace(fix_str,'')
        fix_str=" (pf08)"
        if xlabel.find(fix_str)>=0 : xlabel = xlabel.replace(fix_str,'')
        fix_str=" (pf08 metcor)"
        if xlabel.find(fix_str)>=0 : xlabel = xlabel.replace(fix_str,'')
        if ana_tex.find("Q*")>=0 :
            fix_str="Z'"
            if xlabel.find(fix_str)>=0 : xlabel = xlabel.replace(fix_str,'Q*')

        #histos[0].GetXaxis().SetTitleFont(font)
        #histos[0].GetXaxis().SetLabelFont(font)
        histos[0].GetXaxis().SetTitle(xlabel)
        histos[0].GetYaxis().SetTitle(ylabel)
        #histos[0].GetYaxis().SetTitleFont(font)
        #histos[0].GetYaxis().SetLabelFont(font)
        '''histos[0].GetXaxis().SetTitleOffset(1.3)
        histos[0].GetYaxis().SetTitleOffset(1.3)
        histos[0].GetXaxis().SetLabelOffset(0.02)
        histos[0].GetYaxis().SetLabelOffset(0.02)
        histos[0].GetXaxis().SetTitleSize(0.06)
        histos[0].GetYaxis().SetTitleSize(0.06)
        histos[0].GetXaxis().SetLabelSize(0.06)
        histos[0].GetYaxis().SetLabelSize(0.06)
        histos[0].GetXaxis().SetNdivisions(505);
        histos[0].GetYaxis().SetNdivisions(505);
        histos[0].SetTitle("") '''
        
        histos[0].GetYaxis().SetTitleOffset(1.45)
        histos[0].GetXaxis().SetTitleOffset(1.3)
    

        #hStack.SetMaximum(1.5*maxh) 

        lowY=0.
        if logY:
            # old
            #highY=100000*maxh
            #lowY=0.000001*maxh
            # automatic
            highY=200.*maxh/ROOT.gPad.GetUymax()
            #
            threshold=0.5
            bin_width=histos[0].GetXaxis().GetBinWidth(1)
            lowY=threshold*bin_width
            if ana_tex.find("Q*")>=0 : lowY=10.
            if ana_tex.find("tau^")>=0 :
                lowY=1.
                highY=220.*maxh/ROOT.gPad.GetUymax()
            if xlabel.find("Flow")>=0 : 
                lowY=100.
                highY=600.*maxh/ROOT.gPad.GetUymax()
            if xlabel.find("#tau_{")>=0:
                lowY=1000.
                highY=500.*maxh/ROOT.gPad.GetUymax()
            #
            #histos[0].SetMaximum(highY)
            #histos[0].SetMinimum(lowY)
            histos[0].SetMaximum(100)
            #histos[0].SetMinimum(0.001)
            histos[0].SetMinimum(0.00001)
        else:
            histos[0].SetMaximum(1.5*maxh)
            histos[0].SetMinimum(0.)


    escape_scale_Xaxis=True
    #if(histos1_exists):
    #    if xlabel.find("#tau_{")>=0: escape_scale_Xaxis=True
        #
    #    hStacklast = hStack.GetStack().Last()
    #    lowX_is0=True
    #    lowX=hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.)
    #    highX_ismax=False
    #    highX=hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.)
        #
    #    if escape_scale_Xaxis==False:
    #        for i_bin in range( 1, hStacklast.GetNbinsX()+1 ):
    #            bkg_val=hStacklast.GetBinContent(i_bin)
    #            sig_val=histos[0].GetBinContent(i_bin)
    #            if bkg_val/maxh>0.1 and i_bin<15 and lowX_is0==True :
    #                lowX_is0=False
    #                lowX=hStacklast.GetBinCenter(i_bin)-(hStacklast.GetBinWidth(i_bin)/2.)
    #                if ana_tex.find("e^")>=0 or ana_tex.find("mu^")>=0 : lowX+=1
    #            
    #        val_to_compare=bkg_val
    #        if sig_val>bkg_val : val_to_compare=sig_val
    #        if val_to_compare<lowY and i_bin>15 and highX_ismax==False: 
    #            highX_ismax=True
    #            highX=hStacklast.GetBinCenter(i_bin)+(hStacklast.GetBinWidth(i_bin)/2.)
    #            highX*=1.1
    #        # protections
    #        if lowX<hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.) :
    #            lowX=hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.)
    #        if highX>hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.) :
    #            highX=hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.)
    #        if lowX>=highX :
    #            lowX=hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.)
    #            highX=hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.)
    #        hStack.GetXaxis().SetLimits(int(lowX),int(highX))


    mean = []
    stdDev = []
    
    if not stacksig:
        if logY:
            maxh=200.*maxh/ROOT.gPad.GetUymax()
            histos[0].SetMaximum(5000)
        else:
            histos[0].SetMaximum(2.3*maxh)         
        histos[0].Draw("histe")
        for h in histos:
            mean.append(h.GetMean(1))
            stdDev.append(h.GetStdDev(1))
            if h!=histos[0]:
                h.Draw("histesame")
        
    #legend.SetTextFont(font) 
    legend.Draw()
     
    #pave = ROOT.TPaveText(0.63,0.42,0.88,0.68,"ndc") #6 entries
    #pave = ROOT.TPaveText(0.63,0.46,0.88,0.68,"ndc") #5 entries
    #pave = ROOT.TPaveText(0.63,0.5,0.88,0.68,"ndc") #4 entries
    #pave = ROOT.TPaveText(0.63,0.54,0.88,0.68,"ndc") #3 entries
    #pave = ROOT.TPaveText(0.63,0.46,0.88,0.68,"ndc") #5 entries
    #pave = ROOT.TPaveText(0.63,0.5,0.88,0.68,"ndc") #4 entries
    pave = ROOT.TPaveText(0.63,0.54,0.88,0.68,"ndc") #3 entries
    pave.SetFillColor(0)
    pave.SetBorderSize(0)
    for m,s in zip(mean, stdDev):
        #print(", mean = "+str(m)+", s.d. = "+str(s))
        pave.AddText(", mean = {:.1e}, s.d. = {:.1e}".format(m,s))
    #pave.Draw()
    
    Text = ROOT.TLatex()
    
    Text.SetNDC()
    Text.SetTextAlign(31)
    Text.SetTextSize(0.04)

    text = '#it{' + leftText +'}'
    
    Text.DrawLatex(0.90, 0.92, text)

    rightText = re.split(",", rightText)
    text = '#bf{#it{' + rightText[0] +'}}'
    
    Text.SetTextAlign(12)
    Text.SetNDC(ROOT.kTRUE)
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.83, text)

    rightText[1]=rightText[1].replace("   ","")
    text = '#bf{#it{' + rightText[1] +'}}'
    Text.SetTextSize(0.035)
    Text.DrawLatex(0.18, 0.78, text)

    text = '#bf{#it{' + ana_tex +'}}'
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.73, text)

    text = '#bf{#it{' + extralab +'}}'
    Text.SetTextSize(0.025)
    Text.DrawLatex(0.18, 0.68, text)
    
    canvas.RedrawAxis()
    #canvas.Update()
    canvas.GetFrame().SetBorderSize( 12 )
    canvas.Modified()
    canvas.Update()

    printCanvas(canvas, name, formats, directory)




#_____________________________________________________________________________________________________________
def drawEffPlots(name, ylabel, legend, leftText, rightText, formats, directory, logY, stacksig, histos, colors, ana_tex, extralab):

    canvas = ROOT.TCanvas(name, name, 600, 600)
    canvas.SetLogy(logY)
    canvas.SetTicks(1,1)
    canvas.SetLeftMargin(0.1)
    canvas.SetRightMargin(0.1)

    # first retrieve maximum
    sumhistos = histos[0].Clone()
    iterh = iter(histos)
    next(iterh)

    try:
        histos[1]
    except IndexError:
        histos1_exists = False
    else:
        histos1_exists = True

    for h in iterh:
      sumhistos.Add(h)

    maxh = 2.3

    if logY:
       canvas.SetLogy(1)

    k = 0
    for h in histos:
       h.SetLineWidth(3)
       h.SetLineColor(colors[k])
       k += 1


    # fix names if needed
    if(histos1_exists):
        #xlabel = histos[1].GetXaxis().GetTitle()
        xlabel = "Electron p [GeV]"

        #histos[0].GetXaxis().SetTitleFont(font)
        #histos[0].GetXaxis().SetLabelFont(font)
        histos[0].GetXaxis().SetTitle(xlabel)
        histos[0].GetYaxis().SetTitle(ylabel)
        #histos[0].GetYaxis().SetTitleFont(font)
        #histos[0].GetYaxis().SetLabelFont(font)
        '''histos[0].GetXaxis().SetTitleOffset(1.3)
        histos[0].GetYaxis().SetTitleOffset(1.3)
        histos[0].GetXaxis().SetLabelOffset(0.02)
        histos[0].GetYaxis().SetLabelOffset(0.02)
        histos[0].GetXaxis().SetTitleSize(0.06)
        histos[0].GetYaxis().SetTitleSize(0.06)
        histos[0].GetXaxis().SetLabelSize(0.06)
        histos[0].GetYaxis().SetLabelSize(0.06)
        histos[0].GetXaxis().SetNdivisions(505);
        histos[0].GetYaxis().SetNdivisions(505);
        histos[0].SetTitle("") '''

        histos[0].GetYaxis().SetTitleOffset(1.45)
        histos[0].GetXaxis().SetTitleOffset(1.3)


        #hStack.SetMaximum(1.5*maxh)

        #if logY:
        #    histos[0].SetMaximum(3)
        #    histos[0].SetMinimum(0.00001)
        #else:
    histos[0].SetMaximum(maxh)
    histos[0].SetMinimum(0.)

    escape_scale_Xaxis=True

    #if not stacksig:
        #if logY:
        #    maxh=200.*maxh/ROOT.gPad.GetUymax()
        #    histos[0].SetMaximum(5000)
        #else:
        #    histos[0].SetMaximum(2.3*maxh)         
    histos[0].Draw("e")
    for h in histos:
        if h!=histos[0]:
            h.Draw("esame")

    #legend.SetTextFont(font)
    legend.Draw()

    Text = ROOT.TLatex()

    Text.SetNDC()
    Text.SetTextAlign(31)
    Text.SetTextSize(0.04)

    text = '#it{' + leftText +'}'

    Text.DrawLatex(0.90, 0.92, text)

    rightText = re.split(",", rightText)
    text = '#bf{#it{' + rightText[0] +'}}'

    Text.SetTextAlign(12)
    Text.SetNDC(ROOT.kTRUE)
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.83, text)

    rightText[1]=rightText[1].replace("   ","")
    text = '#bf{#it{' + rightText[1] +'}}'
    Text.SetTextSize(0.035)
    Text.DrawLatex(0.18, 0.78, text)

    text = '#bf{#it{' + ana_tex +'}}'
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.73, text)

    text = '#bf{#it{' + extralab +'}}'
    Text.SetTextSize(0.025)
    Text.DrawLatex(0.18, 0.68, text)

    canvas.RedrawAxis()
    canvas.GetFrame().SetBorderSize( 12 )
    canvas.Modified()
    canvas.Update()

    printCanvas(canvas, name, formats, directory)

    


#____________________________________________________
def printCanvas(canvas, name, formats, directory):

    if format != "":
        if not os.path.exists(directory) :
                os.system("mkdir -p "+directory)
        for f in formats:
            outFile = os.path.join(directory, name) + "." + f
            canvas.SaveAs(outFile)



#__________________________________________________________
if __name__=="__main__":
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    ROOT.gStyle.SetOptStat(0)
    # param file
    paramFile = sys.argv[1]

    module_path = os.path.abspath(paramFile)
    module_dir = os.path.dirname(module_path)
    base_name = os.path.splitext(ntpath.basename(paramFile))[0]

    sys.path.insert(0, module_dir)
    param = importlib.import_module(base_name)
        

    for var in param.variables:
        for label, sels in param.selections.items():
            for sel in sels:
                hsignal,hbackgrounds=mapHistos(var,label,sel, param)
                runPlots(var+"_"+label+"_"+sel,param,hsignal,hbackgrounds,param.extralabel[sel])
                if var in param.effPlots.keys():
                    print("variable in effPlots.keys() is: "+var+", value is then: "+param.effPlots.get(var))
                    effsignal,effbackgrounds=mapEffHistos(param.effPlots.get(var),var,label,sel, param)
                    runEffPlots(param.effPlots.get(var),var+"_"+label+"_"+sel,param,effsignal,effbackgrounds,param.extralabel[sel])

