TITLE Morris-Lecar spiking dynamics

COMMENT

Written by Sungho Hong
Computational Neuroscience Unit
Okinawa Institute of Science and Technology
shhong@oist.jp

ENDCOMMENT

NEURON {
  SUFFIX ml
  USEION k READ ek WRITE ik
  USEION na READ ena WRITE ina
  NONSPECIFIC_CURRENT il
  RANGE gnabar, gkbar, gleak, el, ina, ik, il
  RANGE phi, betam, gammam, betaw, gammaw
  GLOBAL minf, winf, tauw
}

UNITS {
	(mV) = (millivolt)
	(mA) = (milliamp)
	(S)  = (siemens)
}

PARAMETER {
	v (mV)
    
	gnabar = 20e-3 (S/cm2)
	gkbar  = 20e-3 (S/cm2)
    gleak  = 2e-3  (S/cm2)
  
  ek (mV)
  ena (mV)
  el = -70 (mV)
  
  phi = 0.15
	
	betam  = -1.2 (mV)
  gammam = 18 (mV)
  
  betaw  = 0 (mV)
  gammaw = 10 (mV)
}

ASSIGNED {
  ina (mA/cm2)
	ik (mA/cm2)
  il (mA/cm2)
  gk (S/cm2)  
  gna (S/cm2) 
	minf
	winf
	tauw (ms)
}

STATE {
	m   FROM 0 TO 1
  w   FROM 0 TO 1
}

INITIAL {
	rates(v)
	m = minf
	w = winf
}

BREAKPOINT {
	SOLVE states METHOD cnexp
  gna = gnabar * m
  gk  = gkbar * w      
	ik  = gk * (v - ek)
  ina = gna * (v - ena)
  il  = gleak * (v - el)
}

DERIVATIVE states {
	rates(v)
	m = minf
	w' = phi*(winf-w)/tauw
}

PROCEDURE rates( v (mV) ) {

  TABLE minf, winf, tauw FROM -100 TO 100 WITH 200

  minf = 0.5*(1 + tanh((v-betam)/gammam))
  winf = 0.5*(1 + tanh((v-betaw)/gammaw))
  tauw = 1/(cosh((v-betaw)/(2*gammaw)))
}
