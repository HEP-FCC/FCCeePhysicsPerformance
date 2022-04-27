from userConfig import loc
import matplotlib.pyplot as plt
import numpy as np
import awkward as ak
import matplotlib as mpl
from sklearn import metrics
from sklearn.metrics import roc_curve, auc

def errorbar_hist(P,var,P_name,title,units,low,high,bins):
    fig, ax = plt.subplots(figsize=(8,8))
    #Number of events, use this to determine bins and thus bin width
    n = np.sum(ak.num(P).tolist())
    bin_w = (high - low)/bins

    counts, bin_edges = np.histogram(ak.to_list(ak.flatten(P[var])), bins, range=(low,high))
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2.
    err = np.sqrt(counts)
    plt.errorbar(bin_centres, counts, yerr=err, fmt='o', color='k')
    plt.xlabel(f"{title} [{units}]",fontsize=30)
    plt.ylabel("Candidates / (%.4f %s)" % (bin_w, units), fontsize=30)
    plt.xlim(low,high)
    ax.tick_params(axis='both', which='major', labelsize=25)
    ymin, ymax = plt.ylim()
    plt.ylim(0.,ymax*1.1)
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/{P_name}_{var}.pdf")

def errorbar_plot(x_vals, y_vals, x_name, y_name, x_title, y_title, x_range, y_range, x_err=None, y_err=None):
    fig, ax = plt.subplots(figsize=(8,8))
    plt.errorbar(x_vals, y_vals, xerr=x_err, yerr=y_err, fmt='o', color='k')
    plt.xlabel(x_title,fontsize=30)
    plt.xlim(x_range[0],x_range[1])
    plt.ylabel(y_title,fontsize=30)
    plt.ylim(y_range[0],y_range[1])
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/{x_name}_vs_{y_name}.pdf")

def hist_plot(X,X_name,title,low,high,bins):
    fig, ax = plt.subplots(figsize=(8,8))
    plt.hist(X,bins=bins,range=(low,high),histtype='step',color='k')
    plt.xlabel(title,fontsize=30)
    plt.xlim(low,high)
    ax.tick_params(axis='both', which='major', labelsize=25)
    ymin, ymax = plt.ylim()
    plt.ylim(0.,ymax*1.1)
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/{X_name}.pdf")

def hist_plot_2d(X,X_name,X_title,Y,Y_name,Y_title,X_low,X_high,Y_low,Y_high,X_bins,Y_bins,log):
    fig, ax = plt.subplots(figsize=(8,8))
    if(log==True):
        norm_opt = mpl.colors.LogNorm()
    else:
        norm_opt = mpl.colors.Normalize()
    plt.hist2d(X.tolist(),Y.tolist(),bins=[X_bins,Y_bins],range=[[X_low, X_high], [Y_low, Y_high]], norm=norm_opt)
    plt.xlabel(X_title,fontsize=30)
    plt.xlim(X_low,X_high)
    plt.ylabel(Y_title,fontsize=30)
    plt.ylim(Y_low,Y_high)
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/{X_name}_vs_{Y_name}.pdf")


def plot_roc_curve(df, score_column, tpr_threshold=0.7, ax=None, color=None, linestyle='-', label=None):
  if ax is None:
    ax = plt.gca()
  if label is None:
    label = score_column
  fpr, tpr, thresholds = metrics.roc_curve(df['isSignal'], df[score_column], sample_weight=df['weight_total'])
  roc_auc = auc(fpr, tpr)
  mask = tpr >= tpr_threshold
  fpr, tpr = fpr[mask], tpr[mask]
  ax.plot(fpr, tpr, label=label+', auc={:.2f}'.format(roc_auc), color=color, linestyle=linestyle)
  #ax.semilogy(tpr, fpr, label=label, color=color, linestyle=linestyle)

