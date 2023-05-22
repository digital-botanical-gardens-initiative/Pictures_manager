# Pictures manager script
Takes pictures from a QFieldCloud server instance (self-hosted or commercial) and modifies the metadata to have an automatic iNaturalist import. It takes the sample sampling code and coordinates in the gpkg file of interest and adds it in the pictures metadata. Then, once uploaded to iNaturalist, it adds the sampling code as a tag and the coordinates to the observation.

Prerequiste to make this code work:
- Pictures have to contain the scientific name of the species, the sampling code and the point of view (if you take multiple pictures of a single plant, it can be either a descripition of the point of view or a number, in order to have unique pictures names) separated by a space or an underscore. This can be done automatically with QField application when taking a picture
- gpkg have to have the columns x_coord that stores the x coordinate and the y_coord that stores the y coordinate. The CRS (Coordinates Reference System) is not important, the code detects it and converts it to EPSG:4326, that is the CRS used in iNaturalist
- gpkg have to have the column sample_id that stores the sampling code (that has to be unique in order to have unique pictures names)
- To have a Nextcloud instance on the same machine (if not the case, delete DBGI_Nextcloud_import.py and remove it from DBGI_scripts_runner.py)


To run this code: 
1. clone the repository to your computer, by using this link: https://github.com/digital-botanical-gardens-initiative/iNaturalist_uploader.git
2. Copy .env.example to .env and change the variables to suit your needs.
3. Control that all used libraries are installed on your computer.
4. Install exiftool on your Command Line Interface (bash, powershell, ...). Informations about exiftool: https://exiftool.org/
5. Run the DBGI_scripts_runner.py script, that runs all the other scripts and perform the pictures metadata edition.

That's all. With that you should obtain modified pictures that contain the coordinates where the plant have been collected and the sampling code. If you want to verify, you can got to the pictures output directory and use the command <exiftool /name_of_a_picture.jpg> on your CLI. It will display the picture metadata.
