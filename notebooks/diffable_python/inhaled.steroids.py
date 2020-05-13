# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# This list of AMPs is derived from the denominator of [OpenPrescribing high dose inhaled corticosteroid measure](https://github.com/ebmdatalab/openprescribing/blob/master/openprescribing/measure_definitions/icsdose.json) definition.
#
# [All inhaled steroids](#all)
# [Single ingredient inhaled steroids](single#

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
    (bnf_code LIKE  "0302000C0%" OR # Beclometasone Dipropionate,
    bnf_code LIKE "0302000K0%"  OR # Budesonide,
    bnf_code LIKE "0302000N0%" OR # Fluticasone Propionate (Inh),
    bnf_code LIKE "0302000R0%" OR # Mometasone Furoate,
    bnf_code LIKE "0302000U0%" OR # Ciclesonide,
    bnf_code LIKE "0302000V0%" OR # Fluticasone Furoate ,
    bnf_code LIKE "0301011AB%") # BeclometDiprop/Formoterol/Glycopyrronium
    AND
    (bnf_code NOT LIKE "0302000N0%AV" OR # Fluticasone Prop_Inh Soln 500mcg/2ml Ud,
    bnf_code NOT LIKE "0302000N0%AW") # Fluticasone Prop_Inh Soln 2mg/2ml Ud 
    )

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

inhaledsteroids_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','inhaledsteroid_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
inhaledsteroids_codelist
# -

