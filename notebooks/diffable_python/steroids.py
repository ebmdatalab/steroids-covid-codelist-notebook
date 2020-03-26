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

# WIP 
#
# [PHE criteria for shielded patients](https://www.gov.uk/government/publications/covid-19-guidance-on-social-distancing-and-for-vulnerable-people/guidance-on-social-distancing-for-everyone-in-the-uk-and-protecting-older-people-and-vulnerable-adults) specifies people with weakened immune systems and goes on to give an example of "_steroid tablets_". This is very unspecific as you can have injections, enemeas, inhaled which can all act on the imune system. The [BNF hsa a useful summary](https://bnf.nice.org.uk/treatment-summary/corticosteroids-general-use.html) of steroids including area of action, differnt types, uses and side-effects. In this list we will include
#
# -
# -
# -
# -



from ebmdatalab import bq
import os

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
    bnf_code LIKE '1001030C0%' OR ##hydroxychloroquine sulfate - BNF sect drugs used in rheumatic disease
    bnf_code LIKE '0504010F0%' OR ## chloroquine phosphate - BNF sect antiprotozoal drugs
    bnf_code LIKE '0504010Z0%'  OR ## chloroquine phosphate with proguanil - BNF sect antiprotozoal drugs
    bnf_code LIKE '0504010G0%' ## chloroquine sulfate - BNF sect antiprotozoal drugs 
  )

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

steroids_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','steroids_codelist.csv'))
steroids_codelist.head(10)
