TITLE fast AHP

COMMENT

Sungho Hong, CNS Unit, Okinawa Inst Sci Tech. Mar 2008
ENDCOMMENT
 
UNITS {
        (mA) = (milliamp)
        (mV) = (millivolt)
        (S) = (siemens)
}

? interface
NEURON {
        SUFFIX fahp
        USEION k READ ek WRITE ik
        RANGE gbar, g, ntau, vth
        GLOBAL trigger
}
 
PARAMETER {
        gbar = 15e-6 (S/cm2)	<0,1e9>
        ntau = 300 (ms)
        vth = -10 (mV)
}
 
STATE {
        n
}
 
ASSIGNED {
        v (mV)
        celsius (degC)
        ek (mV)

        g (S/cm2)
        ik (mA/cm2)
        
        trigger
}
  
? currents
BREAKPOINT {
        SOLVE states METHOD cnexp
        g = gbar*n
        ik = g*(v - ek)
        
}

INITIAL {
	rates(v)
	n = 0
	trigger = 0
}

? states
DERIVATIVE states {  
        rates(v)
        n' = -n/ntau
}
 
LOCAL q10

? rates
PROCEDURE rates(v(mV)) {
UNITSOFF
        q10 = 1  :no temperature dependence
        if (trigger==0 && v>=vth) {
            trigger = 1
        }
                
        if (v<vth && trigger==1) {
            trigger = 0
            n = n+1
        }
}

UNITSON
