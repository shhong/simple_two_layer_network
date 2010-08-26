#!/usr/bin/env python
import raster
import logging
logging.basicConfig(filename='calc_cgm2.log', filemode='w', level=logging.DEBUG)

def main(path, n):
  from cxcov import xcov3
  d = raster.SimulatedData(path)
  #  d.params['tstop'] = 1250
  psth = d.spike_time.psth(tstop=d.params['tstop'])
  y = psth.get_spike_trains()
  cgm, j = 0.0, 0
  for i in range(n):
    logging.info(str(i))
    for t in y[i+1:]:
      cgm = cgm + xcov3(y[i], t, L=200)
      j = j + 1
  from os.path import join
  from numpy import savetxt
  savetxt(join(path, 'cgm.txt'), cgm/float(j))

if __name__ == '__main__':
  import sys
  main(sys.argv[1], int(sys.argv[2]))
