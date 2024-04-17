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
                treated_df = df.loc[:, ['sample_id', 'sample_name', 'latitude', 'longitude', 'ipen']]
                treated_df.rename(columns={'sample_id':'field_sample_id'}, inplace=True)
                data_cleaned = {k: v if pd.notna(v) else "" for k, v in treated_df.items()}
                for index, row in data_cleaned.iterrows():
                     if row["field_sample_id"] != "":
                        data = {'field_sample_id': row["field_sample_id"],
                                'sample_name': row["sample_name"],
                                'latitude': row["latitude"],
                                'longitude': row["longitude"]}
                        response = session.post(url=collection_url, headers=headers, json=data)
                        print(response.status_code)
                        if response.status_code != 200:
                                collection_url_patch = collection_url + row["field_sample_id"]
                                response = session.patch(url=collection_url_patch, headers=headers, json=data)
                                print(response.status_code)
                        else:
                                print("grec?!")
                     else:
                           print("grec!!")   

