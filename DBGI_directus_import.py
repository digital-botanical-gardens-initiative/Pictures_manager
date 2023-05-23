# import packages
import psycopg2
import os
from dotenv import load_dotenv

#Get the path to the output of inaturalist
CSV_PATH = '/home/dbgi/output/csv/jbn/audrey_le_cabec.csv'

#create SQL query 
sql = f'''
/* Create a temporary table with the columns found in the csv file 
and copy the values from the csv file
*/

CREATE TEMP TABLE tmp_x (
        sample_name TEXT,
        sample_id TEXT,
        picture_panel TEXT,
        picture_general TEXT,
        picture_detail TEXT,
        picture_cut TEXT,
        picture_panel_label TEXT,
        x_coord NUMERIC,
        y_coord NUMERIC,
        geometry TEXT,
        longitude NUMERIC,
        latitude NUMERIC
); -- but see below


COPY tmp_x FROM '{CSV_PATH}' delimiter ',' csv header;

--Insert the values from the temporary table in the pyinat table where the ids do not already exist

INSERT INTO qfield
SELECT * FROM tmp_x
WHERE sample_id NOT IN (SELECT sample_id FROM qfield);

--Update the values of the columns where the ids already exist and match

UPDATE pyinat
SET     quality_grade = tmp_x.quality_grade ,
        sample_name = tmp_x.sample_name ,
        picture_panel = tmp_x.picture_panel ,
        picture_general = tmp_x.picture_general ,
        picture_detail = tmp_x.picture_detail ,
        picture_cut = tmp_x.picture_cut ,
        picture_panel_label = tmp_x.picture_panel_label ,
        x_coord = tmp_x.x_coord ,
        y_coord = tmp_x.y_coord ,
        geometry = tmp_x.geometry ,
        longitude = tmp_x.longitude ,
        latitude = tmp_x.latitude
FROM tmp_x  
WHERE qfield.sample_id = tmp_x.sample_id 
        ;

--Drop the temporary table
DROP TABLE tmp_x; -- else it is dropped at end of session automatically

'''

# import env variable
load_dotenv()

usr=os.getenv('DB_USR')
pwd=os.getenv('DIRECTUS_PWD')
vpn_provider=os.getenv('VPN_PROVIDER')
vpn_user=os.getenv('VPN_USER')
vpn_pwd=os.getenv('VPN_pwd')
vpn_server=os.getenv('VPN_SERVER')


#Add the VPN connection
from pyvpn import VPN

vpn = VPN()

vpn.configure({
    'vpn_provider': vpn_provider,
    'username': vpn_user,
    'password': vpn_pwd,
    'server': vpn_server,
})

vpn.connect()

# establish connections

conn1 = psycopg2.connect(
	database="directus_dbgi",
        user=usr,
        password=pwd,
        host='127.0.0.1',
        port= '5432'
        )

#conn1.autocommit = True

# execute query
cursor = conn1.cursor()
cursor.execute(sql)

# commit and close connection
conn1.commit()
conn1.close()

vpn.diconnect()