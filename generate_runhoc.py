#!/usr/bin/env python

from string import Template
import demjson

hoctemplate = """
load_file("nrngui.hoc")

tstop = $tstop
steps_per_ms = 5
Dt = 1/steps_per_ms
N = tstop*steps_per_ms
twait = 0

NCells = $NCells
syntau = $tau
correlation = $correlation

strdef MLoutputfilename, HHLSoutputfilename
sprint(MLoutputfilename, "ML_N%d_tau%d.dat", NCells, syntau)
sprint(HHLSoutputfilename, "HHLS_N%d_tau%d.dat", NCells, syntau)

load_file("hocs/morphology_mechanisms2.hoc")
load_file("hocs/$casename.hoc")

objref l2[2]
l2[0] = new L2ML(2.0)
l2[1] = new L2HHLS(2.0)

for j=0,1 {
  for i=0,NCells-1 {
    l2[j].synapses()
  }
}

// ML
nw = 0.1e-1 // 5ms
//nw = 0.6e-1 // 50ms

//HHLS
//nw = 0.1e-1 // 5ms
//nw = 0.1e-1 // 50ms

objref nclist[2], nc, syn
for j=0,1 {
  nclist[j] = new List()
  
  for i=0,NCells/2-1 {
      syn = l2[j].synlist.o(i)
      nc = l1[i].connect2target(syn)
      nc.weight = nw
      nclist.append(nc)
  }
  
  for i=NCells/2, NCells-1 {
      syn = l2[j].synlist.o(i)
//    syn.e = -90
      nc = l1[i].connect2target(syn)
      nc.weight = nw    
      nclist.append(nc)
  }
}

objref spikecount[NCells], nil, spiketime[NCells]
for i=0,NCells-1 {
    spikecount[i] = l1[i].connect2target(nil)
    spiketime[i] = new Vector()
    spikecount[i].record(spiketime[i])
}


xopen("l1_1_ml.ses")

objref epsp[2]

for j=0,1 {
  access l2[j].soma
  epsp[j] = new Vector(N)
  epsp[j].record(&v(0.5), Dt)
}

init()
run()

objref f
f = new File()

srate = 0
strdef spikefilename
for i=1,NCells-1 {
    spiketime[i].where(">=", twait)
    srate = srate + 1e3*spiketime[i].size/(tstop-twait)
    sprint(spikefilename, "spiketime/%d.bin",i+1)
    f.wopen(spikefilename)
    spiketime[i].fwrite(f)
    f.close()
}

printf("Spike rate = %g Hz\\n", srate/NCells)

f.wopen(MLoutputfilename)
epsp[0].printf(f, "%.12g\\n")
f.close()

f.wopen(HHLSoutputfilename)
epsp[1].printf(f, "%.12g\\n")
f.close()

quit()

"""

hoctemplate = Template(hoctemplate)
params = demjson.decode(open("config.js", "r").read())
print hoctemplate.safe_substitute(params)