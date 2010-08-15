TITLE M-current

COMMENT

Written by Sungho Hong
Computational Neuroscience Unit
Okinawa Institute of Science and Technology
shhong@oist.jp

ENDCOMMENT

NEURON {
  SUFFIX im
  USEION k READ ek WRITE ik
  RANGE gkbar, ik, tauz, betaz, gammaz
  GLOBAL zinf
}

UNITS {
	(mV) = (millivolt)
	(mA) = (milliamp)
	(S)  = (siemens)
}

PARAMETER {
    v (mV)
    gkbar = 2e-3 (S/cm2)

  tauz  = 200 (ms)
  betaz  = -35 (mV)
  gammaz = 2 (mV)    

  ek (mV)
}

ASSIGNED {
	ik (mA/cm2)
  gk (S/cm2)  
	zinf
}

STATE {
	z   FROM 0 TO 1
}

INITIAL {
	rates(v)
	z = zinf
}

BREAKPOINT {
	SOLVE states METHOD cnexp
  gk  = gkbar * z      
	ik  = gk * (v - ek)
}

DERIVATIVE states {
	rates(v)
	z' = (zinf-z)/tauz
}

PROCEDURE rates( v (mV) ) {

	TABLE zinf FROM -100 TO 100 WITH 200

	zinf = 1/(1 + exp((betaz-v)/gammaz))
}
