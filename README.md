# iNaturalist_uploader
Takes pictures from a QFieldCloud server instance (self-hosted or commercial) and modifies the metadata to have an automatic iNaturalist import. It takes the sample sampling code and coordinates in the gpkg file of interest and adds it in the pictures metadata. Then, once uploaded to iNaturalist, it adds the sampling code as a tag and the coordinates to the observation.

Prerequistie to make this code work:
- Pictures have to contain the scientific name of the species, the sampling code and the point of view (if you take multiple pictures of a single plant, it can be either a descripition of the point of view or a number, in order to have unique pictures names) separated by a space or an underscore. This can be done automatically with QField application when taking a picture
- gpkg have to have the columns x_coord that stores the x coordinate and the y_coord that stores the y coordinate. The CRS (Coordinates Reference System) is not important, the code detects it and converts it to EPSG:4326, that is the CRS used in iNaturalist
- gpkg have to have the column spl_code that stores the sampling code (that has to be unique in order to have unique pictures names)


To run this code: 
1. clone the repository to your computer, by using this link: https://github.com/digital-botanical-gardens-initiative/iNaturalist_uploader.git
2. Create a .env file in the folder and add these variables on it, modified to your needs: 

    #QFieldCloud server instance's API link
    Instance=https://your/qfieldcloud/url/api/v1

    #QFieldCloud username
    Username=yourinstanceusername

    #QFieldcloud password
    Password=yourinstancepassword

    #path to the folder where GPGK will be downloaded
    in_gpkg_path=/path/to/the/gpkg/folder

    #path to the folder where raw JPG will be downloaded
    in_jpg_path=/path/to/the/in/jpg/folder

    #path to the folder where raw csv will be stored
    in_csv_path=/path/to/the/in/csv/folder

    #path to the folder where treated csv will be stored
    out_csv_path=/path/to/the/out/folder

    #path to the folder where treated JPG will be stored
    out_jpg_path=/path/to/the/out/folder
3. Run the DBGI_scripts_runner.py script, that runs all the other scipts and perform the pictures metadata edition.

That's all. With that you should obtain modified pictures that contain the coordinates where the plant have been collected and the sampling code. If you want to verify, you can use the command exiftool /path/to/your/modified/picture.jpg. It will display the picture metadata.
