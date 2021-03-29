import ROOT 
import os, sys
import root_pandas as rp
import pandas as pd 
import glob as glob 
from array import array
import seaborn as sn
import matplotlib.pyplot as plt

from matplotlib import rc, rcParams
rc('text', usetex=True)
rc('axes', linewidth=2)
rc('font', weight='bold')
rc('font', size=20)
#rc('xticks')
rcParams['text.latex.preamble'] = [r'\usepackage{sfmath}']
plt.tight_layout()
# 2D plots for mbc and dE
input_type = 'signal'#gen_MC_noksfinder'
if input_type == 'data':
    input_file = 'phase3DataReco/cands_total_data_proc11bucket9to15_sigbox.root'
elif input_type == 'gen_MC':
    input_file = 'phase3DataReco/total_3KsMC13aBG1.Reco.TAGnoConstraint.KFit.root'
elif input_type == 'gen_MC_noksfinder':
    input_file = '/home/wankun/workdir/data/gen0120/cands_nocut_total_gen0120.root'
elif input_type == 'signal':
     input_file = 'good3KsMC13aBG1.Reco.TAGIP.KFit.root'
vars = ['Mbc', 'deltaE', 'isSignal']
df = rp.read_root(input_file,'B0_3Ks',vars)
df_sig = df[df['isSignal']==1].drop(axis=1,labels='isSignal').head(10000)
df_bkg = df[df['isSignal']==0].drop(axis=1,labels='isSignal').head(10000)
print(f"sig:{len(df_sig)}; bkg:{len(df_bkg)}")

plt.figure(figsize=(15,10))
plt.scatter(x=df_sig['Mbc'], y=df_sig['deltaE'],s=0.1)
plt.xlabel('$M_{bc}$ (GeV/$c^2$)',fontsize =25,fontweight='bold')
plt.ylabel('$\Delta E$ (GeV)',fontsize =25,fontweight='bold')
plt.tick_params('both',labelsize=30, size=15)

plt.xlim(5.2, 5.29)
plt.ylim(-0.2, 0.2)
plt.savefig('hist_sig_MC_Mbc_dE.png')
plt.close()

# generic stacked histogram for Mbc and dE 

cut_type = 'nocut'
posfix = ''
if cut_type == 'oldksfinder':
# ksfinder used old
    qqbar = 'cands_total_mc13aTDCPSkimQQbarReco.TAGnoConstraint.Rave.root'
    charged = 'cands_total_mc13aTDCPSkimChargedReco.TAGnoConstraint.Rave.root'
    mixed = 'cands_total_mc13aTDCPSkimMixedReco.TAGnoConstraint.Rave.root'
    posfix = 'oldksfinder'

if cut_type == 'ksfinder':
# ksfinder used new
    qqbar = '/home/wankun/workdir/data/gen0120/cands_ksfinder_total_qqbar0120.root'
    charged = '/home/wankun/workdir/data/gen0120/cands_ksfinder_total_charged0120.root'
    mixed = '/home/wankun/workdir/data/gen0120/cands_ksfinder_total_mixed0120.root'
    posfix = 'ksfinder'

if cut_type == 'noksfinder':
# cosVe used 
    qqbar = '/home/wankun/workdir/data/gen0120/cands_noksfinder_total_qqbar0120.root'
    charged = '/home/wankun/workdir/data/gen0120/cands_noksfinder_total_charged0120.root'
    mixed = '/home/wankun/workdir/data/gen0120/cands_noksfinder_total_mixed0120.root'
    posfix = 'noksfinder'

if cut_type == 'nocut':
# no cut used
    qqbar = '/home/wankun/workdir/data/gen0120/cands_nocut_total_qqbar0120.root'
    charged = '/home/wankun/workdir/data/gen0120/cands_nocut_total_charged0120.root'
    mixed = '/home/wankun/workdir/data/gen0120/cands_nocut_total_mixed0120.root'
    posfix = 'nocut'


df_qqbar =rp.read_root(qqbar,'B0_3Ks',vars)
df_charged = rp.read_root(charged,'B0_3Ks',vars)
df_mixed = rp.read_root(mixed,'B0_3Ks',vars)

df_charged_head = df_charged.head(int(0.5*len(df_charged)))
df_charged_tail = df_charged.tail(int(0.5*len(df_charged)))
df_mixed_sig = df_mixed[df_mixed.isSignal==1]
df_mixed_scf_head = df_mixed[df_mixed.isSignal==0].head(int(0.2*len(df_mixed[df_mixed.isSignal==0])))
df_mixed_scf_tail = df_mixed[df_mixed.isSignal==0].tail(int(0.8*len(df_mixed[df_mixed.isSignal==0])))

df_qqbar = df_qqbar.append([df_mixed_scf_tail,df_charged_tail])
nbins = 15
nevents = len(df_charged_head)+len(df_mixed_scf_head)

weight = (1,1,1,1)
plt.hist(
    [df_qqbar.Mbc,df_charged_head.Mbc,df_mixed_scf_head.Mbc,df_mixed_sig.Mbc], 
    stacked=True,
    bins=nbins,
    histtype='bar',
    range=(5.20,5.29),
    #weights=weight,
    color=['blue','green','black','red'],
    label=['qqbar','charged','scf','signal']
)
plt.legend(loc=2,fontsize=12)
plt.xlabel(r'Mbc/GeV',fontsize=18)
plt.ylabel(r'event ',fontsize=14)
plt.savefig('hist_stacked_generic_mbc_'+posfix+'.png')
plt.close()

nbins=20
plt.hist(
    [df_qqbar.deltaE,df_charged_head.deltaE,df_mixed_scf_head.deltaE,df_mixed_sig.deltaE], 
    stacked=True,
    bins=nbins,
    histtype='bar',
    range=(-0.2,0.2),
    #weights=[nevents/(0.09/nbins)]*4,
    color=['blue','green','black','red'],
    label=['qqbar','charged','scf','signal']
)
plt.legend(loc=3,fontsize=12)
plt.xlabel(r'$\Delta E/GeV$',fontsize=18)
plt.ylabel(r'event ',fontsize=14)
plt.savefig('hist_stacked_generic_dE_'+posfix+'.png')
plt.close()

print(nevents)