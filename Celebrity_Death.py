# -*-coding:utf-8-*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

####################
# Does the number of celebrities death is highest in 2016 ?
# Is there something interesting in the number of deaths by month?
# Does most of the celebrity die during their young age or old age ?
# What would be the main causes of death?
# What would be the main causes of death for each age category?
####################
death = pd.read_csv("../DataSet/celebrity_deaths_2016.csv")
print death.head()

##########################################
# Does the number of celebrities death is highest in 2016 ?
death_by_year = death.groupby('death_year')['name'].count()
plt.figure()
death_by_year.plot(kind='bar')  # 柱状图
plt.title('Number of deaths every year')
plt.show()

##########################################
# Is there something interesting in the number of deaths by month?
death_by_month = death.groupby('death_month')['name'].count().sort_values()
plt.figure()
death_by_month.plot(kind='line')  # 折线图
plt.title('Number of deaths every month')
plt.show()

##########################################
# Does most of the celebrity die during their young age or old age ?
fig = plt.figure()
ax = fig.add_subplot(111)
ax.boxplot(death['age'])  # 箱线图
plt.show()

##########################################
# What would be the main causes of death?
def group_deathcause(cause):
    mod_cause = ''
    cause = str(cause)
    if 'cancer' in cause:
        mod_cause = 'cancer'
    elif 'heart' in cause or 'cardiac' in cause:
        mod_cause = 'heart disease'
    else:
        mod_cause = cause
    return mod_cause


death['cause_of_death'].fillna('', inplace=True)
death['cause_of_death'] = death.apply(lambda row: group_deathcause(row['cause_of_death']), axis=1)
death_cause = death.groupby('cause_of_death')['name'].count().sort_values(ascending=False)
comp = death_cause.ix[1:20]
y = death_cause.ix[21:1].sum()
comp['others'] = y
plt.figure()
plt.pie(comp, labels=comp.index, autopct='%1.1f%%', startangle=310)  # 饼图
plt.tight_layout()
plt.axis('equal')
plt.title('composition of known cause of death', y=1.08, fontweight='bold')
plt.show()

# -------------------
death['cause_of_death'].fillna('unknown', inplace=True)
death_cause = death.groupby('cause_of_death')['name'].count().sort_values(ascending=False)
print death_cause.head(20)


##########################################
# What would be the main causes of death for each age category?
def age_categorizer(age):
    category = ""
    if (age < 18):
        category = "child"
    elif (age < 30):
        category = "young"
    elif (age < 60):
        category = "adult"
    else:
        category = "old"
    return category


death["age_category"] = death.apply(lambda row: age_categorizer(row["age"]), axis=1)
age_category_rep = death.groupby(["age_category", "cause_of_death"])["name"].count().sort_values(ascending=False)
f = plt.figure(figsize=(8, 15))
the_grid = GridSpec(4, 1)
for cat in [("child", 0, 0), ("young", 1, 0), ("adult", 2, 0), ("old", 3, 0)]:
    x = age_category_rep[cat[0]][1:10]
    y = age_category_rep[cat[0]][11:].sum()
    plt.subplot(the_grid[cat[1], cat[2]], aspect=1)
    x["others"] = y
    plt.pie(x, labels=x.index, autopct='%1.1f%%', startangle=10)
    plt.axis('equal')
    plt.title(cat[0], y=1.08, fontweight="bold")
    plt.tight_layout()
f.suptitle("Composition of known cause of death for every category", y=1.03)
plt.show()
