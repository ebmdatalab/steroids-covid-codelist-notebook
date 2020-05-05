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
#
# - [All ICS inhalers](#ai)
# - [low and medium dose ICS inhalers](#lm)

#import libraries
from ebmdatalab import bq
import os
import pandas as pd

# ## All ICS Inhalers <a id='ai'></a>

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

#import csv from other notebook dealing with high dose
dose_high_ics = pd.read_csv('../data/highdose_inhaledsteroid_codelist.csv')
dose_high_ics.info()

## here we merge and create an indicator to see which ones are in both
combine = pd.merge(all_inhaler_ics,dose_high_ics, how='outer', indicator=True)
combine

# ## Low and medium dose ICS <a id='lm'></a>

#ones that = left only are low medium dose
low_med_ics = combine.loc[(combine['_merge'] == "left_only")]
low_med_ics.info()

low_med_ics.sort_values(["type", "nm"], inplace=True)
low_med_ics.drop('_merge', 1, inplace=True)

low_med_ics

low_med_ics.to_csv(os.path.join('..','data','low_med_ics.csv'))
