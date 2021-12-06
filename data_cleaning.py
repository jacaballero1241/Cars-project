import pandas as pd 
import re
import numpy as np
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_excel(r'C:\Users\Usuario\Desktop\cars_ds_final_2021.xlsx')
df = df.iloc[:, : 100]
df.Displacement = df.Displacement.str.extract('(\d+)').astype(float)
df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].str.replace(',','').str.extract('(\d+)').astype(float)
df['Fuel_Tank_Capacity'] = df['Fuel_Tank_Capacity'].str.extract('(\d+)').astype(float)
df['Height'] = df['Height'].str.replace('.','').str.extract('(\d+)').astype(float)
df['Length'] = df['Length'].str.replace('.','').str.extract('(\d+)').astype(float)
df['Width'] = df['Width'].str.replace('.','').str.extract('(\d+)').astype(float)
df['Kerb_Weight'] = df['Kerb_Weight'].str.replace('.','').str.extract('(\d+)').astype(float)
df['Ground_Clearance'] = df['Ground_Clearance'].str.replace('.','').str.extract('(\d+)').astype(float)
l=[]
for row in df['City_Mileage'].astype(str): 
    l.append(re.findall("([0-9]+[,.]+[0-9]+)",row))
df['City_Mileage'] = pd.DataFrame(l)[0]
l=[]
for i in df['City_Mileage']:
    if i == None:
        l.append(0)
    else:
        l.append(float(i.replace(',','.')))
df['City_Mileage'] = l
df = pd.concat([df,pd.get_dummies(df.Make)], axis=1)
for column in df.columns:
    if len(df[column].value_counts())<2:
        df.drop(columns=[column],inplace=True)
df.Seating_Capacity=df.Seating_Capacity.astype(float)
for column in df.loc[:, df.dtypes == object]:
    print(column,len(df[column].value_counts()))
df = pd.concat([df,pd.get_dummies(df.Drivetrain, prefix='Drivetrain')], axis=1)
df = pd.concat([df,pd.get_dummies(df.Emission_Norm, prefix='Emission_Norm')], axis=1)
df = pd.concat([df,pd.get_dummies(df.Engine_Location, prefix='Engine_Location')], axis=1)
df = pd.concat([df,pd.get_dummies(df.Fuel_Type, prefix='Fuel_Type')], axis=1)
df = pd.concat([df,pd.get_dummies(df.Body_Type, prefix='Body_Type')], axis=1)
df = pd.concat([df,pd.get_dummies(df.Gears, prefix='Gears')], axis=1)
df = pd.concat([df,pd.get_dummies(df.Front_Brakes, prefix='Front_Brakes')], axis=1)
df = pd.concat([df,pd.get_dummies(df.Rear_Brakes, prefix='Rear_Brakes')], axis=1)
df = df.loc[:, df.dtypes != object]
#df.to_csv(r'C:\Users\Usuario\Desktop\cars_ds_final_2021_tidy.csv')
