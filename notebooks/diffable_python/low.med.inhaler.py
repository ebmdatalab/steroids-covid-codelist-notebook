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

# This notebook identifies a list of all ICS inhalers that have not been categorised as high does i.e. low and Medium dose inhalers. This is a pragmatic approach to work out a steroid load for a patient without using does syntax.

from ebmdatalab import bq
import os
import pandas as pd

# +


sql = '''
WITH bnf_codes AS (  
  SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
  (bnf_code LIKE '0302000C0%' OR #BNF Beclometasone dipropionate
  bnf_code LIKE '0301011AB%'  OR #BNF BeclometDiprop/Formoterol/Glycopyrronium",
  bnf_code LIKE '0302000K0%'  OR #BNF budesonide
  bnf_code LIKE '0302000U0%'  OR #BNF Ciclesonide
  bnf_code LIKE '0302000V0%'  OR #BNF Fluticasone furoate 
  bnf_code LIKE '0302000N0%'  OR #BNF Fluticasone propionate 
  bnf_code LIKE '0302000R0%')   #BNF Mometasone Furoate
  AND
  (form_route LIKE '%pressurizedinhalation.inhalation' OR form_route LIKE 'powderinhalation.inhalation%')
   )
   
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

all_inhaler_ics = bq.cached_read(sql, csv_path=os.path.join('..','data','all_inhaler_ics.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
all_inhaler_ics.info()
# -

#import csv from other notebook dealing wi
dose_high_ics = pd.read_csv('../data/highdose_inhaledsteroid_codelist.csv')

low_med_ics = all_inhaler_ics[~all_inhaler_ics.isin(dose_high_ics)].dropna()
low_med_ics.info()

low_med_ics


