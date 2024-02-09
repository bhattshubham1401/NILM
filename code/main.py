import pandas as pd
import numpy as np

def NILM():
    """ data ingestion """

    lst = ['wm',"ac","f",'tv']
    path = "d:/NILM/Data_files/Parquet/Appliances12_06_04_08/"
    print("data read done")
    """ data ingestion done """

    """ data transformation """
    complete_data_lst = [] # empty list to store final data set of all appliances
    for i in range(len(lst)):
        df = pd.read_parquet(f"{path}{lst[i]}.parquet")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.drop_duplicates(inplace=True)  
        df.set_index(['timestamp'],inplace=True ,drop=True)
        df.drop(df[(df['frequency']>51) | (df['frequency']<49)].index, inplace=True)
        df.drop(df[(df['PF']>1) | (df['PF']<0)].index, inplace=True)
        # df.drop(df[(df['current']>20) |(df['current']<0.07)].index, inplace=True)
        df.drop(df[df['voltage']<140].index, inplace=True)
        
        # power is active power derived from voltage current and pf
        df['power'] = (df['voltage'] * df['current'] * df['PF']).round(2)
        
        if lst[i]=="f":
            df_appliance = df[['power',"voltage",'current']].resample(rule="1s").asfreq()
            df_appliance = df_appliance.rename(columns={'power': f'{lst[i]}_A', 'voltage': f'{lst[i]}_V', 'current': f'{lst[i]}_C'})
        else:
            df_sample_lst = [] # empty list for storing resampled data at 1sec frequency of each hour
            unique_dates = pd.Series(df.index.date).unique()
            for date1 in unique_dates: # dates when applince is on                             
                df_date = df[df.index.to_series().dt.date == date1] # dataframe of that perticular date
                hours = df_date.index.hour.unique() # hours when appliance is on
                for h in hours:
                    date2 = f"{date1} {h:02d}"
                    df_hour = df_date.loc[date2] # dataframe of that perticular hour at which appliance was on 
                    df_resampled_hour = df_hour[['power',"voltage",'current']].resample(rule="1s").asfreq()
                    df_sample_lst.append(df_resampled_hour) # adding each hour data in lst
            df_appliance = pd.concat(df_sample_lst) # concating all hours data into single data frame with missing values within signature
            df_appliance = df_appliance.rename(columns={'power': f'{lst[i]}_A', 'voltage': f'{lst[i]}_V', 'current': f'{lst[i]}_C'})
            # df_appliance = create_features(df_appliance)
        complete_data_lst.append(df_appliance) # all applince data in list
    print("transormation done")
    return complete_data_lst