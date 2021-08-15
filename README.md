# rozvedcik
This repository stores various projects related to Rozvedcik Volleyball Tournament by Bára and Vojta.

## historical_results
Py project for calculating all relevant inputs for historical table, statistics and records.
#### Installation
1. consider the `historical_results` a root folder for the project
2. create virtual environment for this project 
3. run `pip install -r requirements.txt` or install the required packages manually
4. run `main.py`
#### Main inputs and outputs
- folder `data` contains general data and subfolders for each year
- historical records are printed on the console
- `mt` as product of `master_table()` stores merged data table with all players and their attributes
- `ht` as product of `historical_table()` stores adjusted data table with all players and their attributes in the format to be imported to the website
- `ht` is also stored as gitignored csv file

## web
Text and Excel files archive used as a backup for web.
- `historical_table` stores the current version of historical table and legend
- `tables` stores the point tables for each tournament and also their generators (Excel files)
- `texts` stores crucial texts from the webpage as nonbreakable spaces get lost when entering the edit mode of Elementor