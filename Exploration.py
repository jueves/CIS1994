#!/usr/bin/env python
# coding: utf-8

# # Data exploration

# ## Preprocess data

# In[1]:


run preprocess.py


# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()


# ## Functions

# In[3]:


def print_num_responses(var):
    n_responses = len(var) - sum(var.isna())
    print(str(n_responses) + " responses out of " + str(len(var)) + " interviewed people.")


# ## Explore

# In[4]:


get_metadata()


# In[5]:


data.region.value_counts(dropna=False)


# ### Population

# In[6]:


data.population.describe()


# In[7]:


data.population.isna().sum()


# ### Smoking

# In[8]:


fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.boxplot(data["cigarettes"].dropna())
ax1.set_title("Cigarettes per day")
ax2.boxplot(data["cigars"].dropna())
ax2.set_title("Cigars per week")
plt.show()


# In[9]:


print("Cigarettes NAs: " + str(sum(data.cigarettes.isna()/len(data))))
print("Cigars NAs: " + str(sum(data.cigars.isna()/len(data))))


# ### Drinking locations

# In[10]:


loc1 = pd.DataFrame({"location" : data.drink_loc1, "preference" : 1})
loc2 = pd.DataFrame({"location" : data.drink_loc2, "preference" : 2})
locs = pd.concat([loc1, loc2])


# In[11]:


sns.countplot(data=locs, y="location", hue="preference")


# ### political_espectrum

# In[12]:


data.political_espectrum.hist()
print_num_responses(data.political_espectrum)


# ### age

# In[13]:


data.age.hist()
print_num_responses(data.age)


# ### income

# In[14]:


print(data.population.describe(percentiles=[0.5, 0.8, 0.9, 0.95]))
data.population.hist()
print_num_responses(data.population)


# ### occupation

# In[15]:


sns.countplot(data=data, y="occupation")
print_num_responses(data.occupation)


# ### socioeconomic_condition

# Socioeconomic Condition is calculated by INE from occupation, activity and laboral status. See [INE glosary](
# https://www.ine.es/censo_accesible/es/glosario.html) for more information.
# 
# INE also uses the variables "Average Socioeconomic Condition" and "Reference person in household socioeconomic condition", althought this pool only labeled the variable as "Socioeconomic condition".

# In[16]:


sns.countplot(data=data, y="socioeconomic_condition")
print_num_responses(data.socioeconomic_condition)


# In[17]:


subdata = data.query("socioeconomic_condition == 'Students'")
sns.countplot(data=subdata, y="occupation").set(title="Students occupations")
print_num_responses(subdata.occupation)


# In[18]:


subdata = data.query("socioeconomic_condition == 'Non payed housekeeping'")
sns.countplot(data=subdata, y="occupation").set(title="Non payed housekeepers occupations")
print_num_responses(subdata.occupation)


# ### sex

# In[19]:


data.sex.value_counts(dropna=False)


# ### education_level

# In[20]:


sns.countplot(data=data, y="education_level")
print_num_responses(data.education_level)


# ### sector

# In[21]:


sns.countplot(data=data, y="sector")
print_num_responses(data.sector)


# ### status

# In[22]:


sns.countplot(data=data, y="status")
print_num_responses(data.status)


# ### UBEs

# In[23]:


data.UBE.hist()


# In[24]:


np.log1p(data.UBE).hist()


# In[25]:


np.log(data.query("UBE > 0").UBE).hist()


# In[26]:


np.exp(2)


# ### Factor plot sex, age, UBE

# Age vs UBE vs sex is the most revealing.

# In[27]:


sns.catplot(x="UBE", y="age", hue="sex", data=data)


# For income, we filter outliers of more than 100 UBEs in the 3 measured days.

# In[28]:


sns.catplot(x="income", y="UBE", hue="sex", data=data.query("UBE < 100"))


# Do people who earn more drink less? Or are they just a smaller group? Keep in mind that points get overlaped in these plots.

# In[29]:


sns.catplot(x="UBE", y="age", hue="income", data=data)

