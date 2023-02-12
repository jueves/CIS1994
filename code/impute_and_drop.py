import utils

data = utils.load_my_data(True)

# Values to impute on missing data per variable
imputing_dic = {
    "cigarettes":0,
    "cigars":0,
    "occupation":"No answer",
    "drink_loc1":"No answer",
    "drink_loc2":"No answer",
    "sex":"No answer",
    "sector":"Unknown"
}



def impute_missing(data):
    '''
    Imputes values to missing data on certain columns and drops rows
    that still have missing data.
    '''

    # Create new categories if they don't exist
    for key, value in imputing_dic.items():
        if isinstance(value, str) and not value in data[key].cat.categories:
            data[key] = data[key].cat.add_categories(value)
            
    # Compute imputing values
    imputing_dic["age"] = data.age.median()
    imputing_dic["population"] = data.population.median()

    data = data.fillna(imputing_dic)

    return(data)

def drop_data(data, max_nas=0.2):
    '''
    Drops all columns with more than column_threshold of NAs
    From resulting dataset, drops all rows with any NAs
    '''
    data = data.dropna(axis=1, thresh=len(data)*(1-max_nas))
    data = data.dropna()
    
    return(data)
