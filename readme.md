# Pandas Tutorial

This repository makes use of most of the basic functions of pandas library.
Nothing Fancy.
#### What does it do?

  - Can analyse 1082 indicators for almost all of the countries in existance.
For eg

```sh
In [21]: temp_df.sample(10)
Out[21]:
                                                     0                     1
964  Tariff rate, applied, weighted mean, manufactu...  TM_TAX_MANF_WM_AR_ZS
816                Primary education, duration (years)           SE_PRM_DURS
68        Average precipitation in depth (mm per year)        AG_LND_PRCP_MM
634  Mortality rate, adult, male (per 1,000 male ad...        SP_DYN_AMRT_MA
584     Manufacturing, value added (constant 2000 US$)        NV_IND_MANF_KD
840            Pump price for gasoline (US$ per liter)        EP_PMP_SGAS_CD
254   Employees, services, male (% of male employment)     SL_SRV_EMPL_MA_ZS
920  Secondary education, vocational pupils (% female)  SE_SEC_ENRL_VO_FE_ZS
733  Nitrous oxide emissions in industrial and ener...     EN_ATM_NOXE_EI_ZS
100      Chemicals (% of value added in manufacturing)     NV_MNF_CHEM_ZS_UN
```
```sh
In [22]: len(indicators)
Out[22]: 1082
```
  - To narrow down the datatset and the declutter the graph, only asian countries have been analysed for the parameter(indicators).
```sh
In [23]: df_temp = pd.read_html('Country_Codes2.html')
    ...: df = df_temp[0]
    ...: a_c_codes = [df['alpha-3'][i] for i in range(len(df['country-code'])) if df['region'][i] == 'Asia' ]
    ...: print(len(a_c_codes))
Out[23] : 51
```
  - Built the DataFrame from the paramters for various countries and Pickle it for further use to save time
  - Calculate Percentage Change in the data from the previous value.
  - Calculate Percentage Change in the data from the starting (initial) value.
  - Plot both of the above DataFrames. 
  - Pickle both the DataFrames for quick access.
  - Plot the correlations between different countries
 ```sh
 In [24]: growth_correlations.describe()['IND']
Out[24]:
count    48.000000
mean      0.900618
std       0.079899
min       0.710692
25%       0.868522
50%       0.928836
75%       0.957534
max       1.000000
Name: IND, dtype: float64
```
```sh
In [25]: growth_correlations['IND'].head()
Out[25]:
AFG    0.726658
ARM    0.953290
AZE    0.932335
BHR    0.956719
BGD    0.767517
Name: IND, dtype: float64
```
  - Resample the data for every 2 years.
  - Observe the Standard Deviation between rolling values of every 2 years wrt to the original data.
 ![alt text](https://github.com/revantg/basic_pandas/raw/master/Figure_1.png "Standard Deviation")
- Compared Correlation of India-Japan and India-China for the selected Parameter
 ![alt text](https://github.com/revantg/basic_pandas/raw/master/Figure_2.png "Plotting and Comparing Correlations")
Markdown is a lightweight markup language based on the formatting conventions that people naturally use in email.  As [John Gruber] writes on the [Markdown site][df1]


### Dependencies


* [Pandas] - Bummer !
* [Numpy] - For using arrays in Python
* [Quandl] - For building Data-Sets
* [Pickle] - For quick reuse of the DataFrame later
* [Matplotlib] - For plotting the graphs


**Thanks for your Time, Consider it giving a star?**
