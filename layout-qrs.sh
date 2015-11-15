#!/bin/bash

KEY=6A9FB506

gs -sDEVICE=psmono \
   -dNOPAUSE -dBATCH -dSAFER \
   -sOutputFile=combined.ps \
$KEY.key.asca.eps \
$KEY.key.ascb.eps \
$KEY.key.ascc.eps \
$KEY.key.ascd.eps \
$KEY.key.asce.eps


