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

# This list of AMPs is derived from the numerator of [OpenPrescribing high dose inhaled corticosteroid measure](https://github.com/ebmdatalab/openprescribing/blob/master/openprescribing/measure_definitions/icsdose.json) definition.

from ebmdatalab import bq
import os

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
   bnf_code LIKE "0302000C0%AC" OR # Beclomet Diprop_Inha 250mcg (200D) (brands and generic)",
   bnf_code LIKE "0302000C0%AU" OR # Beclomet Diprop_Inha B/A 250mcg (200 D) (brands and generic)",
   bnf_code LIKE "0302000C0%BK" OR # Beclomet Diprop_Pdr For Inh 250mcg(100 D (brands and generic)",
   bnf_code LIKE "0302000C0%BW" OR # Beclomet Diprop_Inha 250mcg (200 D) CFF (brands and generic)",
   bnf_code LIKE "0302000C0%BZ" OR # Beclomet/Formoterol_Inh 200/6 (120D) CFF (brands and generic)",
   bnf_code LIKE "0302000C0%CA" OR # Beclomet/Formoterol_Inh 200/6 (120D) Dry (brands and generic)",
   bnf_code LIKE "0302000K0%AH" OR # Budesonide_Pdr For Inh 400mcg (50 D) (brands and generic)",
   bnf_code LIKE "0302000K0%AY" OR # Budesonide_Pdr For Inh 400mcg (100 D) (brands and generic)",
   bnf_code LIKE "0302000K0%AU" OR # Budesonide/Formoterol_InhaB/A 400/12(60D (brands and generic)",
   bnf_code LIKE "0302000N0%AF" OR # Fluticasone Prop_Pdr Inh 250mcg Disk Ref (brands and generic)",
   bnf_code LIKE "0302000N0%AP" OR # Fluticasone Prop_Pdr Inh 500mcg Disk+Dev (brands and generic)",
   bnf_code LIKE "0302000N0%AU" OR # Fluticasone Prop_Pdr For Inh 500mcg(60D) (brands and generic)",
   bnf_code LIKE "0302000N0%AZ" OR # Fluticasone/Salmeterol_Inh 500/50mcg 60D (brands and generic)",
   bnf_code LIKE "0302000N0%BC" OR # ...",
   bnf_code LIKE "0302000N0%BD" OR # ...",
   bnf_code LIKE "0302000N0%BG" OR # Fluticasone/Salmeterol_Inh 250/25mcg120D (brands and generic)",
   bnf_code LIKE "0302000N0%BK" OR # Fluticasone/Formoterol_Inh 250/10mcg120D (brands and generic)",
   bnf_code LIKE "0302000U0%AB" OR # Ciclesonide_Inh 160mcg (120 D) CFF (brands and generic)",
   bnf_code LIKE "0302000V0%AA"    # Fluticasone/Vilanterol_Inha 184/22mcg30D (brands and generic)"
  )

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

highdose_inhaledsteroids_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','highdose_inhaledsteroid_codelist.csv'))
highdose_inhaledsteroids_codelist
# -


