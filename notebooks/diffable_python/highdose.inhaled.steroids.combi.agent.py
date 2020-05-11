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

# This list of VMPs/AMPs is derived from the numerator of [OpenPrescribing high dose inhaled corticosteroid measure](https://github.com/ebmdatalab/openprescribing/blob/master/openprescribing/measure_definitions/icsdose.json) definition and inhalers reported with single agent devices removed.

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''WITH bnf_codes AS (
  SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
   (bnf_code LIKE "0302000C0%BZ" OR # Beclomet/Formoterol_Inh 200/6 (120D) CFF (brands and generic)",
   bnf_code LIKE "0302000C0%CA" OR # Beclomet/Formoterol_Inh 200/6 (120D) Dry (brands and generic)",
   bnf_code LIKE "0302000K0%AU" OR # Budesonide/Formoterol_InhaB/A 400/12(60D (brands and generic)",
   bnf_code LIKE "0302000N0%AZ" OR # Fluticasone/Salmeterol_Inh 500/50mcg 60D (brands and generic)",
   bnf_code LIKE "0302000N0%BG" OR # Fluticasone/Salmeterol_Inh 250/25mcg120D (brands and generic)",
   bnf_code LIKE "0302000N0%BK" OR # Fluticasone/Formoterol_Inh 250/10mcg120D (brands and generic)",
   bnf_code LIKE "0302000V0%AA")   # Fluticasone/Vilanterol_Inha 184/22mcg30D (brands and generic)"
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

highdose_inhaledsteroids_combiagent_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','highdose_inhaledsteroid_combiagent_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
highdose_inhaledsteroids_combiagent_codelist
# +


