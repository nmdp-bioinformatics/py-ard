#!/bin/bash
INDIR=/vol/bio/wmda_simulator/graph/PlanA
OUTDIR=/vol/bio/wmda_simulator/graph/PlanA/flatgl
for pop in AAFA_CARB AAFA_NAMER FILII_NAMER MENAFC_NAMER
  do
  for popcat in donor patient
  do
    INFILE=${INDIR}/${pop}_GraphVal_PlanA_${popcat}.in
    OUTFILE=${OUTDIR}/${pop}_GraphVal_PlanA_${popcat}.flat.gl
    python flatten_glstring.py -i ${INFILE} -o ${OUTFILE} 
  done
done 


