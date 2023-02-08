# Modelization


```python
#%run preprocess.py
# Tarda 17.3seg
```


```python
import pickle
from sklearn.ensemble import RandomForestClassifier
```


```python
pickle_off = open("preprocessed_objs.pickle", "rb")
data, var_names = pickle.load(pickle_off)
pickle_off.close()
```

## Subset data
Select only those atributes whose metadata is considered complete.


```python
selected_vars = []
for key, value in var_names.items():
    if (value["description"] != "incomplete"):
        selected_vars.append(value["name"])
```


```python
subdata = data[selected_vars]
```

## Missing values imputation


```python
subdata.drop(columns=["day", "month", "year"])
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>region</th>
      <th>population</th>
      <th>cigarettes</th>
      <th>cigars</th>
      <th>drink_loc1</th>
      <th>drink_loc2</th>
      <th>political_espectrum</th>
      <th>age</th>
      <th>income</th>
      <th>occupation</th>
      <th>socioeconomic_condition</th>
      <th>sex</th>
      <th>education_level</th>
      <th>sector</th>
      <th>status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Andalusia</td>
      <td>30000.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>4.0</td>
      <td>17.0</td>
      <td>125000</td>
      <td>Skilled workers</td>
      <td>Students</td>
      <td>female</td>
      <td>High school</td>
      <td>Industry</td>
      <td>Skilled workers</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Andalusia</td>
      <td>30000.0</td>
      <td>15.0</td>
      <td>0.0</td>
      <td>Pubs and caffeterias</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>33.0</td>
      <td>125000</td>
      <td>Farmers</td>
      <td>Non-skilled workers</td>
      <td>male</td>
      <td>High school</td>
      <td>Industry</td>
      <td>Non-skilled workers</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Andalusia</td>
      <td>30000.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>68.0</td>
      <td>25000</td>
      <td>Skilled workers</td>
      <td>Retirees and pensioners</td>
      <td>female</td>
      <td>Elementary school</td>
      <td>Industry</td>
      <td>No information</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Andalusia</td>
      <td>30000.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>39.0</td>
      <td>125000</td>
      <td>Skilled workers</td>
      <td>Non payed housekeeping</td>
      <td>female</td>
      <td>Elementary school</td>
      <td>Construction</td>
      <td>Skilled workers</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Andalusia</td>
      <td>30000.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Home</td>
      <td>Pubs and caffeterias</td>
      <td>3.0</td>
      <td>41.0</td>
      <td>175000</td>
      <td>Profesionals</td>
      <td>Technicians and middle management</td>
      <td>male</td>
      <td>Bachelor's degree</td>
      <td>Servicies</td>
      <td>Upper/Upper-middle class</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>17611</th>
      <td>La Rioja</td>
      <td>6000.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>7.0</td>
      <td>67.0</td>
      <td>75000</td>
      <td>Skilled workers</td>
      <td>Non payed housekeeping</td>
      <td>female</td>
      <td>Elementary school</td>
      <td>Industry</td>
      <td>Skilled workers</td>
    </tr>
    <tr>
      <th>17612</th>
      <td>La Rioja</td>
      <td>6000.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>&lt;NA&gt;</td>
      <td>16.0</td>
      <td>NaN</td>
      <td>Business owners</td>
      <td>Students</td>
      <td>male</td>
      <td>High school</td>
      <td>Agriculture</td>
      <td>Old middle class</td>
    </tr>
    <tr>
      <th>17613</th>
      <td>La Rioja</td>
      <td>6000.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>8.0</td>
      <td>52.0</td>
      <td>125000</td>
      <td>Business owners</td>
      <td>Non payed housekeeping</td>
      <td>female</td>
      <td>Elementary school</td>
      <td>Agriculture</td>
      <td>Old middle class</td>
    </tr>
    <tr>
      <th>17614</th>
      <td>La Rioja</td>
      <td>6000.0</td>
      <td>30.0</td>
      <td>0.0</td>
      <td>Home</td>
      <td>Pubs and caffeterias</td>
      <td>&lt;NA&gt;</td>
      <td>26.0</td>
      <td>NaN</td>
      <td>Business owners</td>
      <td>Farmers</td>
      <td>male</td>
      <td>Vocational trainning</td>
      <td>Agriculture</td>
      <td>Old middle class</td>
    </tr>
    <tr>
      <th>17615</th>
      <td>La Rioja</td>
      <td>6000.0</td>
      <td>15.0</td>
      <td>0.0</td>
      <td>Home</td>
      <td>Pubs and caffeterias</td>
      <td>&lt;NA&gt;</td>
      <td>24.0</td>
      <td>175000</td>
      <td>Skilled workers</td>
      <td>Non-skilled workers</td>
      <td>male</td>
      <td>Vocational trainning</td>
      <td>Agriculture</td>
      <td>Skilled workers</td>
    </tr>
  </tbody>
</table>
<p>17616 rows × 15 columns</p>
</div>




```python
# Check that there is only one type of missing data
# Maybe this is not necesary

missing_types = []
for var_name in subdata.columns:
    missing_types.extend(list(subdata[var_name][subdata[var_name].isna()].unique()))
    
print(missing_types)
```

    [nan, nan, nan, nan, nan, <NA>, nan, nan, nan, nan, nan, nan]



```python
# How common are nans per variable?
for var_name in subdata.columns:
    prop_nas = sum(subdata[var_name].isna())/len(subdata)
    if prop_nas != 0.0:
        print(var_name + ": " + str(round(prop_nas, 3)))
```

    population: 0.001
    cigarettes: 0.649
    cigars: 0.652
    drink_loc1: 0.464
    drink_loc2: 0.799
    political_espectrum: 0.336
    age: 0.002
    income: 0.319
    occupation: 0.006
    sex: 0.001
    sector: 0.007


| name | prop | type | comment |
| ---- | ---- | ----- | ------- |
| population | 0.001 | num              | median in their region   |
| cigarettes | 0.656 | num              | 0                        |
| cigars | 0.979 | num                  | 0                        |
| political_espectrum | 0.336 | num     | 34% |
| age | 0.003 | num                     | median (or per similarities)                       |
| income | 0.319 | num                  | 32%                        |
| occupation | 0.045 | cat              | N.C.                      |
| drink_loc1 | 0.464 | cat              | N.C.                     |
| drink_loc2 | 0.799 | cat              | N.C.                   |
| sex | 0.001 | cat                     | New label: "No answer"                    |
| sector | 0.035 | cat                  | either N.S. or N.C., the most common                    |


```python

```

## One hot encoding


```python

```

## RandomForestClassifier


```python
RFC = RandomForestClassifier(n_estimators=5, max_depth=4, random_state=1)
```
