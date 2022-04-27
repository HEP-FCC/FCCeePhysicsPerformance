import uproot
import glob
import pandas as pd
from tqdm import tqdm
import numpy as np
import awkward as ak
import ROOT
import seaborn as sns
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
from xgboost import plot_importance
from hyperopt import hp

from math import sqrt, log, fabs

def get_df(root_file_name, branches):
  tree_keys = []
  ftmp = ROOT.TFile(root_file_name, 'open')
  list_keys = ftmp.GetListOfKeys()
  for i in range(list_keys.GetSize()):
    key = list_keys[i].GetName()
    element = ftmp.Get(key)
    if type(element) is ROOT.TTree:
      tree_keys.append(key)       
  ftmp.Close()    
  
  f = uproot.lazy(root_file_name+":"+tree_keys[0])
  if len(f) == 0:
    return pd.DataFrame()
  df = ak.to_pandas(f[branches])
  
def Z0(S, B):
  if B<=0:
    return -100
  return sqrt(2*((S+B)*log(1+S/B)-S))

def Zmu(S, B):
  if B<=0:
    return -100
  return sqrt(2*(S-B*log(1+S/B)))

def Significance(S, B):
  if B<=0:
    return -100
  return S/sqrt(S+B)

def thres_opt(df, func=Z0, n_spliter=2, score_range=(0, 1), nbins=50, precut='test==True',b_scale=1/0.7):
  df_s = df.query(precut+' & isSignal==1')
  df_b = df.query(precut+' & isSignal==0')
  S0 = np.sum(df_s.loc[df_s.index,'weight_total'])
  B0 = b_scale*np.sum(df_b.loc[df_b.index,'weight_total'])
  print('initial: S0={:.2f}, B0={:.2f}'.format(S0, B0))
  print('inclusive Z: {:.2f}'.format(func(S0, B0)))

  wid = (score_range[1]-score_range[0])/nbins
  arr_x = np.round(np.array([score_range[0]+i*wid for i in range(nbins)]), decimals=2)
  arr_Ztot=np.zeros([nbins, nbins])

  for i in tqdm(range(nbins)):
    xi = score_range[0]+i*wid
    Si = np.sum(df_s.loc[df_s.query('score>='+str(xi)).index,'weight_total'])
    Bi = b_scale*np.sum(df_b.loc[df_b.query('score>='+str(xi)).index,'weight_total'])
    Zi = func(Si, Bi)
    if Bi<=11: continue
    if Zi<0: continue

    for j in range(i):
      xj = score_range[0]+j*wid
      Sj = np.sum(df_s.loc[df_s.query('score>='+str(xj)+' & score<'+str(xi)).index,'weight_total'])
      Bj = b_scale*np.sum(df_b.loc[df_b.query('score>='+str(xj)+' & score<'+str(xi)).index,'weight_total'])
      Zj = func(Sj, Bj)
      if Bj<=11: continue
      if Zj<0: continue
      Ztot = sqrt(Zi**2+Zj**2)
      arr_Ztot[i][j] = Ztot

  df_Z = pd.DataFrame(data=arr_Ztot, index=arr_x, columns=arr_x)

  return df_Z

