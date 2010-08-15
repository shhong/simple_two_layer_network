#!/usr/bin/env python

import os

import logging
logging.basicConfig(filename='raster.log', filemode='w', level=logging.DEBUG)

class PSTH(object):
  def __init__(self, spiketimes, dt, tstop):
    from numpy import array
    self.spiketimes = [array(st).astype(int) for st in spiketimes]
    logging.info('Some spike times.')
    logging.info(str(self.spiketimes[0]))
    logging.info(str(self.spiketimes[10]))
    self.dt = dt
    self.tstop = tstop
    
  def plot_raster(self, axes):
    from numpy import ones
    for i, st in enumerate(self.spiketimes):
      axes.hold(True)
      axes.plot(st, ones(st.size) + i, '.k', ms=2.5)  
    axes.hold(False)
    for direction in ["right", "bottom", "top"]:
      axes.axis[direction].set_visible(False)
    axes.axis["left"].set_label("Neuron id")
    
  
  def get_spike_rate(self, smoothed=True, span=6):
    from numpy import hamming, convolve, zeros, ones
    x = zeros(int(self.tstop))
    for i, st in enumerate(self.spiketimes):
      x[st] = x[st] + 1
    self.spike_rate_raw = x/len(self.spiketimes)*1e3
    if smoothed==False:
      spike_rate = self.spike_rate_raw
    else:
      window = ones(span)
      nn = sum(window)
      spike_rate = convolve(window, self.spike_rate_raw, mode="same")/nn
    return spike_rate
    
  def plot_rate(self, axes, smoothed=True, span=6):
    spike_rate = self.get_spike_rate(smoothed=smoothed, span=span)
    axes.plot(spike_rate, 'b')
    axes.hold(True)
    spike_rate = self.get_spike_rate(smoothed=smoothed, span=3*span)
    axes.plot(spike_rate, 'r')    
    for direction in ["right", "top", "bottom"]:
      axes.axis[direction].set_visible(False)
    axes.axis["left"].set_label("Rate (Hz)")
    axes.axis["bottom"].set_label("Time (ms)")
    axes.set_ylim([0, 50])
#    axes.legend(("6ms", "18ms"), prop={'size':8}, loc=9)
  
  def hist_mean_rate(self, axes, bins=10):
    from numpy import array
    self.mean_rates = [st.size*1e3/self.tstop for st in self.spiketimes]
    axes.hist(self.mean_rates, bins=bins)
    for direction in ["top", "right"]:
      axes.axis[direction].set_visible(False)
    axes.axis["bottom"].set_label("Rate (Hz)")
    return array(self.mean_rates)
    
class SpikeTimeData(object):
  def __init__(self, root):
    super(SpikeTimeData, self).__init__()
    self.root = root
    self.ids = [self.to_id(x) for x in os.listdir(self.root) if x.endswith('.bin')]
    self.ids.sort()
    logging.info('File ids collected.')
    logging.info(str(self.ids))
  
  def to_id(self, x):
    return int(x.split('.')[0])
  
  def to_fname(self, x):
    fname = '.'.join([str(x),'bin'])
    return fname
    
  def to_full_path(self, x):
    fname = os.path.join(self.root, self.to_fname(x))
    return fname
  
  def psth(self, dt=1, tstop=5000):
    from numpy import fromfile
    logging.info("Loading spike times.")
    self.spiketimes = [fromfile(self.to_full_path(i)) for i in self.ids]
    self.psth = PSTH(self.spiketimes, dt, tstop)
    return self.psth
  


def main(path, name):
  from numpy import linspace, loadtxt
  d = SpikeTimeData(path) 
  psth = d.psth()
  
  from mpl_toolkits.axes_grid.axislines import SubplotZero
  import matplotlib.pyplot as plt
  
  f1 = plt.figure(figsize=[6,8])
  ax = SubplotZero(f1, 411)
  f1.add_subplot(ax)  
  psth.plot_raster(ax)
  
  ax = SubplotZero(f1, 412)
  f1.add_subplot(ax)
  psth.plot_rate(ax, smoothed=True)
  
  ax = SubplotZero(f1, 413)
  f1.add_subplot(ax)
  dat = loadtxt('ML_'+name+'_N400_tau5.dat')
  t = linspace(0, 5000, dat.size)
  ax.plot(t, dat, 'k')
  for direction in ["left", "right", "top", "bottom"]:
    ax.axis[direction].set_visible(False)
  logging.info(str(dir(ax.axis["bottom"])))
#  ax.axis["bottom"].major_ticklabels=[]
  ax.set_title("ML")

  ax = SubplotZero(f1, 414)
  f1.add_subplot(ax)
  dat = loadtxt('HHLS_'+name+'_N400_tau5.dat')
  t = linspace(0, 5000, dat.size)
  ax.plot(t, dat, 'k')
  for direction in ["left", "right", "top"]:
    ax.axis[direction].set_visible(False)
  ax.axis["bottom"].set_label("Time (ms)")
  ax.set_title("HHLS")
  
  f1.subplots_adjust(hspace=0.47, top=0.95, bottom=0.05)
  
  f2 = plt.figure(figsize=[4,4])
  ax = SubplotZero(f2, 111)
  f2.add_subplot(ax)
  mf = psth.hist_mean_rate(ax, bins=linspace(0,8,20))
  ax.set_title({"highvar": "High variance", "lowvar": "Low variance"}[name])
  print "Mean firing rate =", mf.mean(), "Hz", "(", mf.std(),")"
  plt.show()

if __name__ == '__main__':
  import sys
  main(sys.argv[1], sys.argv[2])
  