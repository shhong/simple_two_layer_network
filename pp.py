#!/usr/bin/env python

def findfiles(d):
  import os
  allfiles = os.listdir(d)
  highvar = [x for x in allfiles if x.startswith('highvar') and x.endswith('.dat')][0]
  lowvar = [x for x in allfiles if x.startswith('lowvar') and x.endswith('.dat')][0]
  return tuple(os.path.join(d, m) for m in [highvar, lowvar])

def main(x):
  from numpy import loadtxt, arange
  from matplotlib.pyplot import figure, subplot, show, savefig, title
  highvarfile, lowvarfile = findfiles(x)
  highvar, lowvar = loadtxt(highvarfile), loadtxt(lowvarfile)
  hst = [i for i in arange(1,highvar.size) if highvar[i]>=-10 and highvar[i-1]<-10]
  lst = [i for i in arange(1,lowvar.size) if lowvar[i]>=-10 and lowvar[i-1]<-10 ]
  t = arange(highvar.size)*0.2
  p = subplot(2,1,1)
  p.plot(t,highvar)
  title('%g Hz and %g Hz' % (len(hst)/5.0, len(lst)/5.0))
  p = subplot(2,1,2)
  p.plot(t,lowvar,'r')
  savefig(x.strip('/')+'.pdf')

if __name__ == '__main__':
  import sys
  main(sys.argv[1])