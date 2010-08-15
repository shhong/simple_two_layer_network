COMMENT

Written by Sungho Hong, CNS unit, OIST, 2009.

ENDCOMMENT

NEURON {
	POINT_PROCESS CIClamp
	RANGE amp, i, n, tcorr, mu, gain
	ELECTRODE_CURRENT i
}

UNITS {
	(nA) = (nanoamp)
}

PARAMETER {
	amp (nA)
	tcorr = 5 (ms)
	mu = 0 (nA)
	gain = 1
}
ASSIGNED { i (nA) }

STATE { n }

INITIAL {
	i = 0
}

BREAKPOINT {
  SOLVE states METHOD cnexp
  i = n + mu
}

DERIVATIVE states {
  n' = -n/tcorr + gain*amp
}
