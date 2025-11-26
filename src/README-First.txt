# Downloading the dataset and starter app

The original script to download the dataset to use for this exercise is:
```
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
```

The script has been modified for the following:
1. Download the csv and save it in the right folder path (../data/00_Datasets/00_Raw/CSVs/)
2. If the csv file already exists, overwrite it.

```
wget -O ../data/00_Datasets/00_Raw/CSVs/spacex_launch_dash.csv \
  "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
```

The following command will download the source file for the dash app:
```
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/t4-Vy4iOU19i8y6E3Px_ww/spacex-dash-app.py"
```

# Running the app

To run the app, type the following in a terminal window:
```
python spacex-dash-app.py 
```

Note: You must be in the same folder as the Python file to run the app.
