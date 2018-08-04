## -------------------------- Basic Imports -------------------------- ##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
style.use('fivethirtyeight')
## ------------------------------------------------------------------- ##

## --- Extracting all the DataFrames on the webpage for Indicators --- ##
dfs = pd.read_html('WWDI.html')
# For Testing Purposes
[print(df.head()) for df in dfs] 
df = dfs[1]
print(df.head())
## ------------------------------------------------------------------- ##

## Saving all the Indicators and their Descriptions from the DataFrame ##
indicators = [code for code in df['CODE'].tolist()]
indicators_index = [i for i in df['INDICATOR'].tolist()]
temp_df = pd.DataFrame(np.column_stack((np.asarray(indicators_index), np.asarray(indicators))))
print(temp_df.head())
## ------------------------------------------------------------------- ##


## ---Getting Country Codes for all the asian countries ---- ##
# (Too many countries clutter the graph)
df_temp = pd.read_html('Country_Codes2.html')
df = df_temp[0] # For Testing Purposes
print(df.sample()) #For testing purposes
a_c_codes = [df['alpha-3'][i] for i in range(len(df['country-code'])) if df['region'][i] == 'Asia' ]
## --------------------------------------------------------- ##

## -------------------Defining Quandl ---------------------- ##
import quandl
## --------------------------------------------------------- ##

## --Selecting a Random parameter from the indicators list-- ##
parameter = 'IT_NET_BBND_P2'
print("Visualizing Data for the Parameter = {0} : {1}".format(indicators_index[indicators.index(parameter)], parameter))
## --------------------------------------------------------- ##

## ------------------------Testing-------------------------## 
df_temp1 = quandl.get("WWDI/ARM_" + parameter)
df_temp1.rename(columns={'Value': 'ARM'}, inplace=True)
print(df_temp1.head())

df_temp2 = quandl.get("WWDI/IND_" + parameter)
df_temp2.rename(columns={'Value': 'IND'}, inplace=True)
print(df_temp2.head())

df_temp3 = quandl.get("WWDI/JPN_" + parameter)
df_temp3.rename(columns={'Value': 'JPN'}, inplace=True)
print(df_temp3.head())
## ---------------------------------------------------------##

## -------------------- Building Main-Data-Set ----------------- ##

def get_dataset(parameter, country_codes, limit=None):
    main_df = pd.DataFrame()
    # if limit:k = limit
    # else : k = len(country_codes)
    for i in country_codes:
        # if k == 0: break
        # else: k-=1
        try:
            df_temp = quandl.get("WWDI/" + i + "_" + parameter)
        except:
            continue
        df_temp.rename(columns={'Value': i}, inplace=True)
        print(i)
        if main_df.empty:
            main_df = df_temp
        else:
            main_df = main_df.join(df_temp)

    ## Saving the DataFrame
    import pickle
    pickle_out = open("main_df.pickle", 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    return main_df


# Parameter - Any value from the 'indicators' variable
# Country Codes - List of Countries
# Limit - Limit for the number of Countries (default = all countries)
main_df = get_dataset(parameter, country_codes=a_c_codes, limit=len(a_c_codes))
## ------------------------------------------------------------- ##

## Retrieving the Data-Frame
main_df = pd.read_pickle('main_df.pickle')

## Basic Plotting ##
main_df.plot()
plt.legend().remove()
plt.show()

## Retrieving the Percent Change from the last value
def pct_chng_last(df, country_codes) :
    main_df2 = df
    main_df2.fillna(method='ffill')
    pct_chg_df = pd.DataFrame()
    for i in country_codes:
        if i in main_df2.columns.values:
            pct_chg_df[i] = main_df2[i].pct_change()

    pct_chg_df.fillna(0, inplace = True)
    pct_chg_df.replace(np.inf, 1, inplace = True)
    
    ## Saving the DataFrame
    pickle_out = open("pct_change_last.pickle", 'wb')
    pickle.dump(pct_chg_df, pickle_out)
    pickle_out.close()

    pct_chg_df.plot() # Plotting the Percent Change or Growth Rate in Values
    plt.legend().remove() # Does not clutter the graph
    plt.show()

    return pct_chg_df

# df (DataFrame) - For which percent change has to be calculated
# country_codes (list) - Country Codes for which percent change has to be calculated
df_pct_chg_last = pct_chng_last(main_df, country_codes = a_c_codes)

## Retrieving the Growth or % Change from the first value
def pct_chng_start(df, country_codes):
    main_df3 = pd.DataFrame()
    main_df3 = df
    main_df3.replace(0, np.NaN, inplace=True)
    main_df3.fillna(method='bfill', inplace=True)

    pct_chng_start_df = pd.DataFrame()
    for i in country_codes:
        if i in main_df3.columns.values:
            pct_chng_start_df[i] = (
                main_df3[i] - main_df3[i][0]) / main_df3[i][0] * 100
#     print(pct_chng_start_df)
    pickle_out = open("pct_change_start.pickle", 'wb')
    pickle.dump(pct_chng_start_df, pickle_out)
    pickle_out.close()

    pct_chng_start_df.plot()  # Plotting the Percent Change or Growth Rate in Values
    plt.legend().remove()  # Does not clutter the graph
    plt.show()
    return pct_chng_start_df

# Will Not Work for Starting Values of 0 for any dataset
pct_chng_start_df = pct_chng_start(main_df, a_c_codes)

## Getting Correlations between Growth Rates of different countries
growth_correlations = pct_chng_start_df.corr()
print(growth_correlations)
# Obtaining Correlation Stats for INDIA
print(growth_correlations.describe()['IND'])

## Resampling and plotting the graph    
main_df = pd.read_pickle('main_df.pickle')
ind_data = main_df['IND']
resampled_ind_data = ind_data.resample('2A').mean()

# Comparing Resampled with Unsampled Data
fig = plt.figure()
ax1 = plt.subplot2grid((1,1), (0,0))
ind_data.plot(ax = ax1, c='red', label = 'Original Data')
resampled_ind_data.plot(ax = ax1, c='blue', label = 'Resampled Mean Data')
plt.legend(loc = 2)
plt.show()

# Plotting the Deviation with comparision of sampled and unsampled data
fig = plt.figure()
ax1 = plt.subplot2grid((2, 1), (0, 0))
ax2 = plt.subplot2grid((2, 1), (1, 0), sharex=ax1)

main_df['IND_MEAN'] = main_df["IND"].rolling(2).mean() # Rolling Mean for every 3 DataPoints
main_df['IND_STD'] = main_df["IND"].rolling(2).std() #Rolling Standard Deviation 

main_df['IND'].plot(ax = ax1, label = "Original Data")
main_df['IND_MEAN'].plot(ax = ax1, label = 'MEAN Data')
main_df['IND_STD'].plot(ax = ax2, label = 'Standard Deviation')
plt.legend(loc = 4)
plt.show()

del main_df['IND_MEAN']
del main_df['IND_STD']

## Comparing Correlations between (India and China) and (India and Japan)
IND_data = main_df['IND']
CHN_data = main_df['CHN']
JPN_data = main_df['JPN']

IND_JPN_corr = main_df['IND'].rolling(5).corr(JPN_data)
IND_CHN_corr = main_df['IND'].rolling(5).corr(CHN_data)

fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0, 0))
ax2 = plt.subplot2grid((2,1), (1, 0), sharex = ax1)

IND_data.plot(label = 'INDIA', ax = ax1)
CHN_data.plot(label = 'CHINA', ax=ax1)
JPN_data.plot(label = 'JAPAN', ax=ax1)
ax1.legend(loc = 4)

IND_JPN_corr.plot(ax = ax2, label = 'INDIA-JAPAN')
IND_CHN_corr.plot(ax = ax2, label = 'INDIA-CHINA')
ax2.legend(loc = 4)

plt.show()




