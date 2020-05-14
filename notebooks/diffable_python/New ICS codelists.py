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

# # Inhaled Corticosteroid codelists

# ## All Inhaled Corticosteroids

# This list of AMPs is derived from the denominator of [OpenPrescribing high dose inhaled corticosteroid measure](https://github.com/ebmdatalab/openprescribing/blob/master/openprescribing/measure_definitions/icsdose.json) definition.
#
# [All inhaled steroids](#all)

from ebmdatalab import bq
import os
import pandas as pd

# +
#define high and med/low dose ICS inhaler variable for SQL search

high_dose_sql = """
CASE WHEN bnf_code LIKE '0302000C0%AC' THEN 'high' # Beclomet Diprop_Inha 250mcg (200D) (brands and generic)
WHEN bnf_code LIKE '0302000C0%AU' THEN 'high' # Beclomet Diprop_Inha B/A 250mcg (200 D) (brands and generic)
WHEN bnf_code LIKE '0302000C0%BK' THEN 'high' # Beclomet Diprop_Pdr For Inh 250mcg(100 D (brands and generic)
WHEN bnf_code LIKE '0302000C0%BW' THEN 'high' # Beclomet Diprop_Inha 250mcg (200 D) CFF (brands and generic)
WHEN bnf_code LIKE '0302000C0%BZ' THEN 'high' # Beclomet/Formoterol_Inh 200/6 (120D) CFF (brands and generic)
WHEN bnf_code LIKE '0302000C0%CA' THEN 'high' # Beclomet/Formoterol_Inh 200/6 (120D) Dry (brands and generic)
WHEN bnf_code LIKE '0302000K0%AH' THEN 'high' # Budesonide_Pdr For Inh 400mcg (50 D) (brands and generic)
WHEN bnf_code LIKE '0302000K0%AY' THEN 'high' # Budesonide_Pdr For Inh 400mcg (100 D) (brands and generic)
WHEN bnf_code LIKE '0302000K0%AU' THEN 'high' # Budesonide/Formoterol_InhaB/A 400/12(60D (brands and generic)
WHEN bnf_code LIKE '0302000N0%AF' THEN 'high' # Fluticasone Prop_Pdr Inh 250mcg Disk Ref (brands and generic)
WHEN bnf_code LIKE '0302000N0%AP' THEN 'high' # Fluticasone Prop_Pdr Inh 500mcg Disk+Dev (brands and generic)
WHEN bnf_code LIKE '0302000N0%AU' THEN 'high' # Fluticasone Prop_Pdr For Inh 500mcg(60D) (brands and generic)
WHEN bnf_code LIKE '0302000N0%AZ' THEN 'high' # Fluticasone/Salmeterol_Inh 500/50mcg 60D (brands and generic)
WHEN bnf_code LIKE '0302000N0%BC' THEN 'high' # ...
WHEN bnf_code LIKE '0302000N0%BD' THEN 'high' # ...
WHEN bnf_code LIKE '0302000N0%BG' THEN 'high' # Fluticasone/Salmeterol_Inh 250/25mcg120D (brands and generic)
WHEN bnf_code LIKE '0302000N0%BK' THEN 'high' # Fluticasone/Formoterol_Inh 250/10mcg120D (brands and generic)
WHEN bnf_code LIKE '0302000U0%AB' THEN 'high' # Ciclesonide_Inh 160mcg (120 D) CFF (brands and generic)
WHEN bnf_code LIKE '0302000V0%AA' THEN 'high' # Fluticasone/Vilanterol_Inha 184/22mcg30D (brands and generic)"
ELSE 'med_low'
END AS strength
"""

# +
#Single SQL for all different types of inhalers

sql = '''
WITH bnf_codes AS (
  SELECT 
    DISTINCT bnf_code 
  FROM 
    measures.dmd_objs_with_form_route 
  WHERE 
    (
      bnf_code LIKE '0302000C0%' OR #BNF Beclometasone dipropionate
      bnf_code LIKE '0301011AB%' OR #BNF BeclometDiprop/Formoterol/Glycopyrronium
      bnf_code LIKE '0302000K0%' OR #BNF budesonide
      bnf_code LIKE '0302000U0%' OR #BNF Ciclesonide
      bnf_code LIKE '0302000V0%' OR #BNF Fluticasone furoate
      bnf_code LIKE '0302000N0%' OR #BNF Fluticasone propionate
      bnf_code LIKE '0302000R0%'#BNF Mometasone Furoate
      ) 
    AND (
      form_route LIKE '%pressurizedinhalation.inhalation' 
      OR form_route LIKE 'powderinhalation.inhalation%'
    ) # this provides BNF codes for all inhalers (MDI and DPI) which contain corticosteroid
) 
SELECT 
  'vmp' AS type, 
  vmp.id AS id, #VMP from DM+D
  vmp.bnf_code AS bnf_code, 
  vmp.nm AS nm, #VMP name
  COUNT(ing) AS chem_count, #how many chemical substances in device
  {} #variable high_dose_sql, from code in above cell: describes inhalers as either "high" dose or "med/low"
FROM 
  dmd.vmp AS vmp 
  INNER JOIN dmd.vpi AS vpi ON vmp.id = vpi.vmp 
WHERE 
  bnf_code IN (
    SELECT 
      * 
    FROM 
      bnf_codes
  ) 
GROUP BY 
  vmp.id, 
  vmp.bnf_code, 
  vmp.nm 
UNION ALL 
SELECT 
  "amp" AS type, 
  amp.id AS id, 
  amp.bnf_code AS bnf_code, 
  amp.descr AS nm, 
  COUNT(ing) AS chem_count, 
  {} 
FROM 
  dmd.amp as amp 
  INNER JOIN dmd.vpi as vpi ON amp.vmp = vpi.vmp 
WHERE 
  bnf_code IN (
    SELECT 
      * 
    FROM 
      bnf_codes
  ) 
GROUP BY 
  amp.id, 
  amp.bnf_code, 
  amp.descr
'''

sql = sql.format(high_dose_sql,high_dose_sql) #adds in high_dose_ics variable
all_ics = bq.cached_read(sql, csv_path=os.path.join('..','data','new_all_ics_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
all_ics.info()
# -

# ## Single Agent Inhaled Corticosteroids

# +
#to create a list of single agent ICS, we filter dataframe to where the number of chemical substances in the inhaler = 1
single_ics = all_ics.loc[all_ics['chem_count'] == 1]
single_ics = single_ics.drop(columns=["chem_count","strength"]) #drop the strength and chemical substance count from the table

single_ics
# -

# ## Combination Inhaled Corticosteroids

#Similar to above, to get combination products, we filter where there is more than one chemical substance in the inhaler
combi_ics = all_ics.loc[all_ics['chem_count'] >1]
combi_ics = combi_ics.drop(columns=["chem_count","strength"])
combi_ics

# ## High Dose Corticosteroids

# ### Single agent High Dose Corticosteroids

#to get high dose single products, we have to filter where there is only one chemical substance in the inhaler AND where strength is "high"
single_high_ics = all_ics.loc[((all_ics['chem_count'] == 1) & (all_ics['strength'] == "high"))]
single_high_ics = single_high_ics.drop(columns=["chem_count","strength"])
single_high_ics

# ### Combination High Dose Corticosteroids

# +
#to get high dose single products, we have to filter where there is more than one chemical substance in the inhaler AND where strength is "high"
combi_high_ics = all_ics.loc[((all_ics['chem_count'] > 1) & (all_ics['strength'] == "high"))]
combi_high_ics = combi_high_ics.drop(columns=["chem_count","strength"])

combi_high_ics
# -

# ## Low/Medium Dose Inhaled Corticosteroids

# ### Combination Low/Medium Dose Corticosteroids

#to get low and medium dose combination products, we have to filter where there is more than one chemical substance in the inhaler AND where strength is "med_low"
combi_med_low_ics = all_ics.loc[((all_ics['chem_count'] >1) & (all_ics['strength'] == "med_low"))]
combi_med_low_ics = combi_med_low_ics.drop(columns=["chem_count","strength"])
combi_med_low_ics

# ### Single agent Low/Medium Dose Corticosteroids

#to get low and medium dose single products, we have to filter where there is only chemical substance in the inhaler AND where strength is "med_low"
single_med_low_ics = all_ics.loc[((all_ics['chem_count'] == 1) & (all_ics['strength'] == "med_low"))]
single_med_low_ics = single_med_low_ics.drop(columns=["chem_count","strength"])
single_med_low_ics

# ### Create codelists

#Here we create all codelists as csvs
single_ics.to_csv(os.path.join('..','data','new_single_ics_codelist.csv'))
combi_ics.to_csv(os.path.join('..','data','new_combi_ics_codelist.csv'))
combi_high_ics.to_csv(os.path.join('..','data','new_combi_high_dose_ics_codelist.csv'))
single_high_ics.to_csv(os.path.join('..','data','new_single_high_dose_ics_codelist.csv'))
combi_med_low_ics.to_csv(os.path.join('..','data','new_combi_med_low_ics_codelist.csv'))
single_med_low_ics.to_csv(os.path.join('..','data','new_single_med_low_dose_ics_codelist.csv'))


