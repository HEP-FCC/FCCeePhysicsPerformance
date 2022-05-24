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
  
  file = uproot.open(root_file_name)
  tree = file['events']

  #Load event-level vars
  print("Converting to awkward array")
  if len(file) == 0:
    return pd.DataFrame()
  df = tree.arrays(library="pd", how="zip", filter_name=branches)
  
  return df

def Z0(S, B):
  if B<=0:
    return -100
  return sqrt(2*((S+B)*log(1+S/B)-S))

def Zmu(S, B):
  if B<=0:
    return -100
  return sqrt(2*(S-B*log(1+S/B)))

def Z(S, B):
  if B<=0:
    return -100
  return S/sqrt(S+B)

def Significance(df_s,df_b, func=Z0, score_range=(0, 1), nbins=50):
  S0 = np.sum(df_s.loc[df_s.index,'weight'])
  B0 = np.sum(df_b.loc[df_b.index,'weight']) 
  print('initial: S0={:.2f}, B0={:.2f}'.format(S0, B0))
  print('inclusive Z: {:.2f}'.format(func(S0, B0)))

  wid = (score_range[1]-score_range[0])/nbins
  arr_x = np.round(np.array([score_range[0]+i*wid for i in range(nbins)]), decimals=2)
  arr_Z=np.zeros([nbins])

  for i in tqdm(range(nbins)):
    xi = score_range[0]+i*wid
    Si = np.sum(df_s.loc[df_s.query('BDT>='+str(xi)).index,'weight'])
    Bi = np.sum(df_b.loc[df_b.query('BDT>='+str(xi)).index,'weight'])
    Zi = func(Si, Bi)
    if Bi<=11: continue
    if Zi<0: continue
    arr_Z[i]=Zi
          
  df_Z = pd.DataFrame(data=arr_Z, index=arr_x, columns=["Z"])
  
  return df_Z

def thres_opt(df, func=Z0, n_spliter=2, score_range=(0, 1), nbins=50, precut='test==True',b_scale=1.):
  df_s = df.query(precut+' & isSignal==1')
  df_b = df.query(precut+' & isSignal==0')
  S0 = len(df_s.index)
  B0 = b_scale*len(df_b.index)
  print('initial: S0={:.2f}, B0={:.2f}'.format(S0, B0))
  print('inclusive Z: {:.2f}'.format(func(S0, B0)))

  wid = (score_range[1]-score_range[0])/nbins
  arr_x = np.round(np.array([score_range[0]+i*wid for i in range(nbins)]), decimals=2)
  arr_Ztot=np.zeros([nbins, nbins])

  for i in tqdm(range(nbins)):
    xi = score_range[0]+i*wid
    Si = len(df_s.query('score>='+str(xi)).index)
    Bi = b_scale*len(df_b.query('score>='+str(xi)).index)
    Zi = func(Si, Bi)
    if Bi<=11: continue
    if Zi<0: continue

    for j in range(i):
      xj = score_range[0]+j*wid
      Sj = len(df_s.query('score>='+str(xj)+' & score<'+str(xi)).index)
      Bj = b_scale*len(df_b.query('score>='+str(xj)+' & score<'+str(xi)).index)
      Zj = func(Sj, Bj)
      if Bj<=11: continue
      if Zj<0: continue
      Ztot = sqrt(Zi**2+Zj**2)
      arr_Ztot[i][j] = Ztot

  df_Z = pd.DataFrame(data=arr_Ztot, index=arr_x, columns=arr_x)

  return df_Z

def plot_roc_curve(df, score_column, tpr_threshold=0.7, ax=None, color=None, linestyle='-', label=None):
    if ax is None:
        ax = plt.gca()
    if label is None:
        label = score_column
    fpr, tpr, thresholds = metrics.roc_curve(df['isSignal'], df[score_column] )
    roc_auc = auc(fpr, tpr)
    mask = tpr >= tpr_threshold
    fpr, tpr = fpr[mask], tpr[mask]
    ax.plot(fpr, tpr, label=label+', auc={:.2f}'.format(roc_auc), color=color, linestyle=linestyle)
    #ax.semilogy(tpr, fpr, label=label, color=color, linestyle=linestyle)
#__________________________________________________________
def dir_exist(mydir):
    import os.path
    if os.path.exists(mydir): return True
    else: return False


#__________________________________________________________
def create_dir(mydir):
    if not dir_exist(mydir):
        import os
        os.system('mkdir -p {}'.format(mydir))
