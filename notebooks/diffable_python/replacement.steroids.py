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

# [PHE criteria for shielded patients](https://www.gov.uk/government/publications/covid-19-guidance-on-social-distancing-and-for-vulnerable-people/guidance-on-social-distancing-for-everyone-in-the-uk-and-protecting-older-people-and-vulnerable-adults) specifies people with weakened immune systems and goes on to give an example of "_steroid tablets_". This is very unspecific as you can have injections, enemeas, inhaled which can all act on the imune system. The [BNF has a useful summary](https://bnf.nice.org.uk/treatment-summary/corticosteroids-general-use.html) of steroids including area of action, differnt types, uses and side-effects. In this list we will include "replacement like" steroids. 
#

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
    bnf_code LIKE '060302%'       OR    #BNF  glucocorticoid
    bnf_code LIKE '060301%'       OR    #BNF replacement therapy - fludrocortisone
    bnf_code LIKE '100102%'       OR      #BNF paragraph on corticosteroinds in rheumatic disease
    bnf_code LIKE '010502%'             #BNF paragraph on corticosteroinds in bowel disorders
  )

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp_full
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

replacement_steroids_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','replacement_steroids_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
replacement_steroids_codelist.count()
# +
sql = '''
SELECT obj_type, snomed_id, bnf_code, dmd_name, form_route
FROM ebmdatalab.measures_v2.dmd_objs_with_form_route
WHERE 
    (bnf_code LIKE '060302%'       OR    #BNF  glucocorticoid
    bnf_code LIKE '060301%'       OR    #BNF replacement therapy - fludrocortisone
    bnf_code LIKE '100102%'       OR      #BNF paragraph on corticosteroinds in rheumatic disease
    bnf_code LIKE '010502%' )            #BNF paragraph on corticosteroinds in bowel disorders
AND
(obj_type = "vmp" OR obj_type = "amp")


ORDER BY obj_type, bnf_code'''

test2 = bq.cached_read(sql, csv_path=os.path.join('..','data','test2.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
test2.count()
