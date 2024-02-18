# Download and Merge DSM of Egypt and Convert It to COG Using GDAL and Python

## Overview

This guide provides instructions on how to download and merge the Digital Surface Model (DSM) of Egypt and then convert it into Cloud Optimized GeoTIFF (COG) format using GDAL and Python.

## Prerequisites

- Register and obtain your secret key from [OpenTopography](https://opentopography.org/).
- Git
- Python 3.8+

## Steps

1. **Clone the Repository and Set Up the Virtual Environment**

   Clone the repository and create a virtual environment. Install the required packages from `requirements.txt`.

   ```bash
   git clone https://github.com/Youssef-Harby/dsm2cog.git
   cd dsm2cog
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the Script**
   Execute the main script to start the process.

   ```bash
   python main.py
   ```
   *dont't forget to fill your secret key in main.py here: https://github.com/Youssef-Harby/dsm2cog/blob/main/main.py#L9-L10*

3. **Navigate to the DSM Data Directory**

   Change into the directory containing the DSM data for Egypt.

   ```bash
   cd dsm_data_egypt
   ```

4. **Create a List of TIFF Files**

   Generate a text file listing all TIFF files in the directory.

   ```bash
   ls -1 *.tif > tiff_list.txt
   ```

5. **Merge TIFF Files Using gdal_merge.py**

   Use gdal_merge.py to combine all the raster data into a single TIFF file.

   ```bash
   gdal_merge.py -o mosaic.tif --optfile tiff_list.txt
   ```

6. **Convert to Cloud Optimized GeoTIFF (COG)**

   Convert the merged TIFF file to Cloud Optimized GeoTIFF format with LZW compression.

   ```bash
   gdal_translate mosaic.tif output_cog.tif -of COG -co COMPRESS=LZW
   ```
