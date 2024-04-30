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
        # Ignore old layer without sample_id
        if filename.endswith('.csv') and filename != "SBL_20004_2022_EPSG:4326.csv" and not filename.endswith("_obs_EPSG:4326.csv"):
                # Read each df
                constructed_path = root + "/" + filename
                df = pd.read_csv(constructed_path)
                # Homogeneize data for directus import
                treated_df = df.loc[:, ['sample_id', 'sample_name', 'latitude', 'longitude', 'ipen', 'no_name_on_list', 'name_proposition', 'herbivory_(percent)', 'comment_eco', 'soil_type', 'weather', 'temperature_(°C)', 'comment_env']]
                treated_df.rename(columns={'sample_id':'field_sample_id'}, inplace=True)
                # Remove possible whitespaces
                treated_df["field_sample_id"] = treated_df["field_sample_id"].str.strip()
                # Replace NAs by nothing, otherwise directus raises an error
                treated_df.fillna('', inplace=True)
                # Send each row individually to directus
                for index, row in treated_df.iterrows():
                     # Check that sample_id is not null
                     if row["field_sample_id"] != '':
                        # Store correct field_sample_name, depending if user entered it in sample_name or name_proposition
                        if row["no_name_on_list"] != 1 or row["no_name_on_list"] != 1.0:
                              field_sample_name = row["sample_name"]
                        else:
                              field_sample_name = row["name_proposition"]
                        # Create json for data import
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
                        
                        # Request
                        response = session.post(url=collection_url, headers=headers, json=data)

                        # Check if success, if not try modifying the data to update already existing observations
                        if response.status_code != 200:
                                # Modify url to target the correct observation
                                collection_url_patch = collection_url + row["field_sample_id"]
                                # Request
                                response = session.patch(url=collection_url_patch, headers=headers, json=data)
                                # If still not success response, print informations on the sample.
                                # Should be replaced by an other directus request to have a track of unsuccessful import elsewhere than in the log.
                                if response.status_code != 200:
                                      print(row["field_sample_id"])
                                      print(response.status_code)
                                      print(filename)
                     else:
                           print("no field sample id")

      

