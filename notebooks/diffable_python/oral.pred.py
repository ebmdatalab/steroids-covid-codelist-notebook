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

# The following notebook contains [NHS Dictionary of Medicines and Devices](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) codes for oral prednisolone. The intention is that this list can be used to support identifiction of more severe forms of athma.

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''
WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
  bnf_code LIKE '0603020T0%' #bnf chemical prednisolone from endocrine corticosteroids

)

SELECT *
FROM measures.dmd_objs_with_form_route
WHERE bnf_code IN (SELECT * FROM bnf_codes) 
AND 
obj_type IN ('vmp', 'amp')
AND
form_route LIKE '%.oral%' #gets rid of suppositories
ORDER BY obj_type, bnf_code, snomed_id
'''


pred_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','pred_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pred_codelist
