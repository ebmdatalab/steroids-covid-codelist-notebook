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

# This list of VMPs/AMPs is derived from the numerator of [OpenPrescribing high dose inhaled corticosteroid measure](https://github.com/ebmdatalab/openprescribing/blob/master/openprescribing/measure_definitions/icsdose.json) definition and inhalers reported, with combination products removed.

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''WITH bnf_codes AS (
  SELECT DISTINCT bnf_code FROM measures.dmd_objs_with_form_route WHERE 
   (bnf_code LIKE "0302000C0%AC"OR # Beclomet Diprop_Inha 250mcg (200D) (brands and generic)",
   bnf_code LIKE "0302000C0%AU" OR # Beclomet Diprop_Inha B/A 250mcg (200 D) (brands and generic)",
   bnf_code LIKE "0302000C0%BK" OR # Beclomet Diprop_Pdr For Inh 250mcg(100 D (brands and generic)",
   bnf_code LIKE "0302000C0%BW" OR # Beclomet Diprop_Inha 250mcg (200 D) CFF (brands and generic)",
   bnf_code LIKE "0302000K0%AH" OR # Budesonide_Pdr For Inh 400mcg (50 D) (brands and generic)",
   bnf_code LIKE "0302000K0%AY" OR # Budesonide_Pdr For Inh 400mcg (100 D) (brands and generic)",
   bnf_code LIKE "0302000N0%AF" OR # Fluticasone Prop_Pdr Inh 250mcg Disk Ref (brands and generic)",
   bnf_code LIKE "0302000N0%AP" OR # Fluticasone Prop_Pdr Inh 500mcg Disk+Dev (brands and generic)",
   bnf_code LIKE "0302000N0%AU" OR # Fluticasone Prop_Pdr For Inh 500mcg(60D) (brands and generic)",
   bnf_code LIKE "0302000N0%BC" OR # Fluticasone 250micrograms/dose inhaler (brands and generic)",
   bnf_code LIKE "0302000N0%BD" OR # ...",
   bnf_code LIKE "0302000U0%AB)"    # Ciclesonide_Inh 160mcg (120 D) CFF (brands and generic)"
   AND
(form_route LIKE '%pressurizedinhalation.inhalation' OR form_route LIKE 'powderinhalation.inhalation%')
   ))
   
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''


highdose_inhaledsteroids_single_agent_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','highdose_inhaledsteroid_single_agent_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
highdose_inhaledsteroids_single_agent_codelist
# -


