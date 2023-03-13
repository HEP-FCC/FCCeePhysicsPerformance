import sys,os, argparse
import json
from particle import pdgid, Particle
#import numpy as np
import argparse
from collections import OrderedDict
import ROOT


#Local code
from userConfig import loc, mode_names, train_vars, train_vars_vtx, train_vars_2, Ediff_cut, Nsig_min, MVA_cuts
from decay_mode_xs import modes as bkg_modes
from decay_mode_xs import prod

VERBOSE = False

class MC_part:
  def __init__(self, evt, index):
    self.idx     = index
    self.pdg     = evt.MC_PDG.           at(index)
    self.m1      = evt.MC_M1.            at(index)
    self.m2      = evt.MC_M2.            at(index)
    self.d1      = evt.MC_D1.            at(index)
    self.d2      = evt.MC_D2.            at(index)
    self.px      = evt.MC_px.            at(index)
    self.py      = evt.MC_py.            at(index)
    self.pz      = evt.MC_pz.            at(index)
    self.mass    = evt.MC_mass.          at(index)
    self.p_angle = evt.MC_p_thrust_angle.at(index)

    self.sig_like   = (self.p_angle > 0.5)
    self.one_mom    = (self.m1 == self.m2)
    if self.m1 > 0:
      self.hadron_mom = ( pdgid.is_hadron(evt.MC_PDG.at(self.m1)) and pdgid.is_hadron(evt.MC_PDG.at(self.m2)) )
    else:
      self.hadron_mom = False
    try:
      Particle.from_pdgid(self.pdg)
    except:
      self.name = 'pdg%d'%self.pdg
    else:
      self.name = Particle.from_pdgid(self.pdg).name

  def is_type(self, criteria):
    if   criteria == '': return True
    elif criteria == 'has b': return pdgid.has_bottom(self.pdg)
    elif criteria == 'has c': return pdgid.has_charm(self.pdg)
    elif criteria == 'heavy flavor': return (pdgid.has_bottom(self.pdg) or pdgid.has_charm(self.pdg))
    elif criteria == 'not final':  return (self.d1 != 0 and self.d1 < self.d2)
    else:
      print (f'MC_part: Invalid criteria, {criteria}, for particle type')
      return False


def find_decay_chain(in_tree, original, decay_further = 'has b'):
  generation = 0
  decay_chain = {}
  decay_chain[generation] = [original]
  is_final = False
  while not is_final:
    decay_chain[generation+1] = []
    for p in decay_chain[generation]:
      if p.is_type(decay_further):
        for d in range(p.d1, p.d2+1):
          daughter = MC_part(in_tree, d)
          decay_chain[generation+1].append(daughter)
      else: decay_chain[generation+1].append(p)
    generation += 1
    is_final = True
    for p in decay_chain[generation]:
      if p.is_type(decay_further):
        is_final = False

  return decay_chain


def write_decay_str(decay_chain, only_final = False):
  decay_str = ''
  for generation in decay_chain:
    if only_final and (generation != 0 and generation != list(decay_chain.keys())[-1]): continue
    if generation > 0 : decay_str += ' --> '
    for p in decay_chain[generation]: decay_str += p.name + ' '
  if only_final: 
    decay_str = decay_str.replace(' gamma', '')
    decay_str = decay_str.replace('- ', '+/- ').replace('+ ', '+/- ')
    decay_str = decay_str.replace('~', '')
  return decay_str


def output_summary(out_name, cat, special_cases, summary_count):
  out_f = open(out_name, 'w')
  out_f.write(f'Category selection: MVA1 > {MVA_cuts["base"]["MVA1"]}, MVA2_{cat} > {MVA_cuts["base"]["MVA2_sig"]}\n')
  out_f.write(f'Total number of events passing selection: {summary_count["total"]}\n')
  out_f.write('----Event type----\n')
  for case in special_cases:
    out_f.write(case.ljust(30) + f'{len(special_cases[case])}'.ljust(10) + f'{1.0 *len(special_cases[case]) / summary_count["total"] :.4%}\n')
  out_f.write(f'\n total cases of decay chains {len(summary_count)-1}\n')
  out_f.write('----Decay chain counts----\n')

  sort_count = sorted(summary_count.items(), key=lambda x: x[1], reverse=True)
  # sort is a list of tuples not a dict
  for decay in sort_count:
    out_f.write(decay[0].ljust(80) + f'{decay[1]}'.ljust(10) + f'{1.0 * decay[1]/summary_count["total"] :.4%}\n')



def run(bkg_samples, cat, find_further_decay):

  path = loc.EXTRA 

  trees = {}
  for samp in bkg_samples:
    trees[samp] = ROOT.TChain('events')
    trees[samp].Add(f'{path}/{bkg_samples[samp]}')

    special_cases = {}
    special_cases['multi_mom but not from quarks'] = []
    special_cases['0 b-hadrons in event'] = []
    special_cases['1 b-hadrons in event'] = []
    special_cases['3 b-hadrons in event'] = []
    special_cases['4 b-hadrons in event'] = []
    special_cases['> 4 b-hadrons in event'] = []
    special_cases['no signal-like b decay'] = []

    summary_count = {}
    summary_count['total'] = 0

    print (trees[samp].GetEntries())
    for iEvt in range(trees[samp].GetEntries()):
    #for iEvt in range(20000):
      if iEvt % 1000 == 0: print (f'=============\nat {iEvt} event')
      trees[samp].GetEntry(iEvt)
      if trees[samp].EVT_MVA1 < MVA_cuts["base"]["MVA1"]: continue
      if cat == 'bu' and trees[samp].EVT_MVA2_bu < MVA_cuts["base"]["MVA2_sig"]: continue
      if cat == 'bc' and trees[samp].EVT_MVA2_bc < MVA_cuts["base"]["MVA2_sig"]: continue
      if VERBOSE: print ('--------------------')
      if VERBOSE: print (f'at {iEvt} event')
      summary_count['total'] += 1

      # find all independent b hadrons
      original_Bs = {}
      for iPart in range(trees[samp].MC_n):
        part = MC_part(trees[samp], iPart)
        if part.is_type(find_further_decay):
#        if pdgid.has_bottom(trees[samp].MC_PDG.at(iPart)):
          #part = MC_part(trees[samp], iPart)
          if not part.one_mom and not part.hadron_mom:
            if part.idx not in original_Bs: original_Bs[part.idx] = part            
          elif not (part.one_mom and part.hadron_mom): 
            special_cases['multi_mom but not from quarks'].append(iEvt)
      if VERBOSE: print (f'number of independent b hadrons: {len(original_Bs)}')
      if len(original_Bs) == 0: special_cases['0 b-hadrons in event'].append(iEvt) 
      if len(original_Bs) == 1: special_cases['1 b-hadrons in event'].append(iEvt)
      if len(original_Bs) == 3: special_cases['3 b-hadrons in event'].append(iEvt)
      if len(original_Bs) == 4: special_cases['4 b-hadrons in event'].append(iEvt)
      if len(original_Bs) >  4: special_cases['> 4 b-hadrons in event'].append(iEvt)


      num_sig = 0
      closest_angle = -1
      for idx in original_Bs:
        if original_Bs[idx].sig_like: num_sig += 1
        if original_Bs[idx].p_angle > closest_angle:
          closest_angle = original_Bs[idx].p_angle
      if VERBOSE: print (f'number of signal like b decays: {num_sig}')
      if VERBOSE: print (f'closest b decay is: {closest_angle}')
      if num_sig == 0: special_cases['no signal-like b decay'].append(iEvt)
      if num_sig != 1: continue

      # only write signal like b decay chains
      for idx in original_Bs:
        if original_Bs[idx].sig_like: 
          decay_chain = find_decay_chain(trees[samp], original_Bs[idx], decay_further = find_further_decay ) 
          decay_str = write_decay_str(decay_chain, only_final = (find_further_decay == 'not final'))
          if decay_str in summary_count: summary_count[decay_str] += 1
          else:                          summary_count[decay_str]  = 1

    out_name = f'output/{samp}_in_{cat}_cat.txt'
    output_summary(out_name, cat, special_cases, summary_count)



def main():
    parser = argparse.ArgumentParser(description='Analyse toys for template fit')
    parser.add_argument("--bkgSF", required=False,help="Scale factor for background, for optimistic or pessimistic estimates",default=1)
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    parser.add_argument("--optDim", choices=["2D", "2var"],required=False,help="multi-variable fit",default="2D")
    args = parser.parse_args()


    bkg_samples = {#'Zbb':  'p8_ee_Zbb_ecm91.root'}#,
                   #'Zcc':  'p8_ee_Zcc_ecm91.root'}#,
#                   'Zuds': 'p8_ee_Zuds_ecm91.root'}


#                   'Bd2D3Pi'  : 'p8_ee_Zbb_ecm91_EvtGen_Bd2D3Pi.root'}
#                   'Bd2DDs'   : 'p8_ee_Zbb_ecm91_EvtGen_Bd2DDs.root'}
#                   'Bd2DTauNu': 'p8_ee_Zbb_ecm91_EvtGen_Bd2DTauNu.root'}
#                   'Dd2K3Pi': 'p8_ee_Zcc_ecm91_EvtGen_Dd2K3Pi.root'}
#                   'Dd2TauNu' : 'p8_ee_Zcc_ecm91_EvtGen_Dd2TauNu.root'}
#                   'Dd2TauNuTAUHADNU' : 'p8_ee_Zcc_ecm91_EvtGen_Dd2TauNuTAUHADNU.root'}
#                   'Ds2EtapRho' : 'p8_ee_Zcc_ecm91_EvtGen_Ds2EtapRho.root'}
#                   'Lc2Sigma2Pi' : 'p8_ee_Zcc_ecm91_EvtGen_Lc2Sigma2Pi.root'}
                   'Lc2LMuNu' : 'p8_ee_Zcc_ecm91_EvtGen_Lc2LMuNu.root'}
#                   '' : ''}


    run(bkg_samples, 'bu', 'heavy flavor')

if __name__ == '__main__':
    main()

