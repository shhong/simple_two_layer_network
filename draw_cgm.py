#!/usr/bin/env python

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.axislines import SubplotZero
from numpy import loadtxt, linspace

def main(path):
  from os.path import join
  cgm = loadtxt(join(path, 'highvar1', 'cgm.txt'))
  t = linspace(-200,200, cgm.size)

  f1 = plt.figure(figsize=[6,3])
  ax = SubplotZero(f1, 111)
  f1.add_subplot(ax)

  for direction in ["right", "top"]:
    ax.axis[direction].set_visible(False)
  ax.axis["yzero"].set_visible(True)
  ax.axis["yzero"].toggle(all=False)

  ax.hold(True)

  ax.plot(t[101:-100], cgm[101:-100]*1e6, 'b')
  cgm = loadtxt(join(path, 'lowvar1', 'cgm.txt'))
  ax.plot(t[101:-100], cgm[101:-100]*1e6, 'r')

  ax.axis["left"].set_label(r'Covarinace (Hz$^2$)')
  ax.axis["bottom"].set_label("Time lag (ms)")

  from matplotlib.font_manager import fontManager, FontProperties  
  font= FontProperties(size='medium');
  l = plt.legend(('High var', 'Low var'), loc=1, prop=font)
  
  f1.subplots_adjust(top=0.95, bottom=0.15, left=0.1, right=0.95)
  plt.savefig(join(path, 'cgm.png'), dpi=200)
if __name__ == '__main__':
  import sys
  path = sys.argv[1]
  main(path)
#  plt.show()