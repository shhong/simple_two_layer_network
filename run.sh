#!/bin/bash

ln -s $1/spiketime .
./generate_runhoc.py $1/config.js run.hoc
nrngui run.hoc
mv HHLS_*.dat $1
mv ML_*.dat $1
mv run.hoc $1
rm spiketime

