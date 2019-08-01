#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: abenaafful
"""

import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

species = pd.read_csv(r'/Users/abenaafful/Desktop/Data/biodiversity/species_info.csv')
print(species.head())

#How many different species are indentified?
species_count = species.scientific_name.nunique()

#The different values of catergory
species_type = species.category.nunique()

#The different values of conservation_status
conservation_statuses = species.conservation_status.nunique()

#The next section analyzes the Conservation Status
conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()
print(conservation_counts)

#To count the species that didn't come through because it was categorized as 'Nan'
species.fillna('No Intervention', inplace = True)
conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()

#Visualizing the conservation status
protection_counts = conservation_counts_fixed.sort_values(by='scientific_name')

plt.figure(figsize=(10,4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)), protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show

#Investingating Endangered Species
species['is_protected'] = species.conservation_status != 'No Intervention'

category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()
print(category_counts.head())

category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()
print(category_pivot)

category_pivot.columns = ['category', 'not_protected', 'protected']
category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)
print(category_pivot)

#Chi-Squared Test for Significance
contingency = [[30, 146], [75, 413]]
pval = chi2_contingency(contingency)[1] #p-value

contingency_reptile_mammal = [[30, 146], [5, 73]]
pval_reptile_mammal = chi2_contingency(contingency_reptile_mammal)[1]
