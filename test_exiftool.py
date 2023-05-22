from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def modify_coordinates(image_path, latitude, longitude):
    image = Image.open(image_path)
    exif_data = image._getexif()

    if exif_data is not None:
        # Get the ID of the EXIF GPS tag
        exif_gps_tag = None
        for tag, value in TAGS.items():
            if value == 'GPSInfo':
                exif_gps_tag = tag
                break

        # Check if GPSInfo exists in the EXIF data
        if exif_gps_tag is not None and exif_gps_tag in exif_data:
            # Get the GPSInfo dictionary
            gps_info = exif_data[exif_gps_tag]
        else:
            # Create a new GPSInfo dictionary
            gps_info = {}

        # Modify the latitude and longitude values
        gps_info[2] = ((latitude[0], 1), (latitude[1], 1), (latitude[2] * 100, 100))
        gps_info[4] = ((longitude[0], 1), (longitude[1], 1), (longitude[2] * 100, 100))

        # Update the modified GPSInfo in the EXIF data
        exif_data[exif_gps_tag] = gps_info

        # Update the EXIF data in the image
        image.save(image_path, exif=image.info['exif'])

        print('Coordinates modified successfully.')
    else:
        print('No EXIF data found in the image.')

# Usage example
modify_coordinates("C:\\Users\\edoua\\Desktop\\test3.jpg", (40, 12, 4320), (-74, 55, 3540))