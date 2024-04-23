import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()

# import env variable
directus_email = os.getenv('directus_email')
directus_password = os.getenv('directus_password')

# Define the Directus table url
base_url = 'http://directus.dbgi.org'

# Define the login endpoint URL
login_url = base_url + '/auth/login'

# Create a session object for making requests
session = requests.Session()

# Send a POST request to the login endpoint
response = session.post(login_url, json={'email': directus_email, 'password': directus_password})
data = response.json()['data']
directus_access_token = data['access_token']
collection_url = base_url + '/items/Qfield_Data/'
session.headers.update({'Authorization': f'Bearer {directus_access_token}'})

#Add headers
headers = {
                'Content-Type': 'application/json'
    }

out_csv_path = os.getenv('out_csv_path')

# Iterate over all CSV files in the input folder and its subdirectories
for root, dirs, files in os.walk(out_csv_path):
    for filename in files:
        if filename.endswith('.csv') and filename != "SBL_20004_2022_EPSG:4326.csv":
                constructed_path = root + "/" + filename
                df = pd.read_csv(constructed_path)
                treated_df = df.loc[:, ['sample_id', 'sample_name', 'latitude', 'longitude', 'ipen', 'no_name_on_list', 'name_proposition', 'herbivory_(percent)', 'comment_eco', 'soil_type', 'weather', 'temperature_(°C)', 'comment_env']]
                treated_df.rename(columns={'sample_id':'field_sample_id'}, inplace=True)
                treated_df.fillna('', inplace=True)
                for index, row in treated_df.iterrows():
                     if row["field_sample_id"] != '':
                        if row["no_name_on_list"] == "":
                              field_sample_name = row["sample_name"]
                        else:
                              field_sample_name = row["name_proposition"]
                              print(row["no_name_on_list"])
                              print(field_sample_name)
                        data = {'field_sample_id_pk': row["field_sample_id"],
                                'field_sample_id_fk': row["field_sample_id"],
                                'field_sample_name': field_sample_name,
                                'latitude': row["latitude"],
                                'longitude': row["longitude"],
                                'ipen': row["ipen"],
                                'herbivory_percent': row["herbivory_(percent)"],
                                'comment_eco': row["comment_eco"],
                                'soil_type': row["soil_type"],
                                'weather': row["weather"],
                                'temperature_celsius': row["temperature_(°C)"],
                                'comment_env': row["comment_env"]}
                        
                        response = session.post(url=collection_url, headers=headers, json=data)
                        if response.status_code != 200:
                                collection_url_patch = collection_url + row["field_sample_id"]
                                response = session.patch(url=collection_url_patch, headers=headers, json=data)
                                if response.status_code != 200:
                                      print(row["field_sample_id"])
                     else:
                           print("no field sample id")   

