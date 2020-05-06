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

# [PHE criteria for shielded patients](https://www.gov.uk/government/publications/covid-19-guidance-on-social-distancing-and-for-vulnerable-people/guidance-on-social-distancing-for-everyone-in-the-uk-and-protecting-older-people-and-vulnerable-adults) specifies people with weakened immune systems and goes on to give an example of "_steroid tablets_". This is very unspecific as you can have injections, enemeas, inhaled which can all act on the imune system. The [BNF has a useful summary](https://bnf.nice.org.uk/treatment-summary/corticosteroids-general-use.html) of steroids including area of action, differnt types, uses and side-effects. This is a complete list of steroids in BNF (I think as steroids in all over the place).
#

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE
    (bnf_code LIKE '060302%'         OR    #BNF  glucocorticoid
    bnf_code LIKE '060301%'          OR    #BNF replacement therapy - fludrocortisone
    bnf_code LIKE '100102%'          OR    #BNF paragraph on corticosteroinds in rheumatic disease
    bnf_code LIKE '110401%'          OR    #BNF eye cortocosteroids
    bnf_code LIKE '1201010U0%'       OR    #BNF ear cortocosteroids prednisolone
    bnf_code LIKE '1201010E0%'       OR    #BNF ear cortocosteroids betamethasone
    bnf_code LIKE '120101050%'       OR    #BNF ear cortocosteroids dexamethasone
    bnf_code LIKE '120101040%'       OR    #BNF ear cortocosteroids dexamethasone
    bnf_code LIKE '1201010F0%'       OR    #BNF ear cortocosteroids flumethasone
    bnf_code LIKE '1201010Q0%'       OR    #BNF ear cortocosteroids hydrocortisone
    bnf_code LIKE '1201010G0%'       OR    #BNF ear cortocosteroids hydrocortisone acetate
    bnf_code LIKE '1201010Z0%'       OR    #BNF ear cortocosteroids triamcinolclone
    bnf_code LIKE '1201010AE%'       OR    #BNF dexamtheasome/cipro combo
    bnf_code LIKE '1201020Q0%'       OR    #BNF dexamtheasome/cipro combo
    bnf_code LIKE '1202010V0%'       OR    #BNF dexamtheasome isonicontinate nasal
    bnf_code LIKE '1203010M0%'       OR    #BNF hydrocortisone sodium succ
    bnf_code LIKE '1306010AA%'       OR    #BNF clind/hydrocort
    bnf_code LIKE '1304000V0%'       OR    #BNF hydrocortisone
    bnf_code LIKE '1304000X0%'       OR    #BNF hydrocortisone acetate
    bnf_code LIKE '1304000W0%'       OR    #BNF hydrocortisone butyrate
    bnf_code LIKE '010502%'          OR    #BNF paragraph on corticosteroinds in bowel disorders
    bnf_code LIKE '010702%'          OR    #BNF paragraph on local preparations with corticosteroinds haemorrhoidal
    bnf_code LIKE '03040%'           OR    #topical cortic'steroids
    bnf_code LIKE '03020%'           OR    #BNF respiratory steroids
    bnf_code LIKE "0301011AB%")         # BeclometDiprop/Formoterol/Glycopyrronium compund triple therapy
  )

SELECT "vmp" AS type, id, vmp.bnf_code, nm, form_route
FROM dmd.vmp_full as vmp
INNER JOIN
measures.dmd_objs_with_form_route as dmd
ON
vmp.id = dmd.snomed_id
WHERE vmp.bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, amp.bnf_code, descr, form_route
FROM dmd.amp
INNER JOIN
measures.dmd_objs_with_form_route as dmd
ON
amp.id = dmd.snomed_id
WHERE amp.bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

complete_steroids_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','complete_steroids_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
complete_steroids_codelist
# -

