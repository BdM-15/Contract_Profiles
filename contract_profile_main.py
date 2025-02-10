# Convert initial data pull which comes from VCE SB Dashboard as .xlsx file to .csv file to prepare the data for data cleansing and analysis.  Once converted, move the .csv file to the processed data folder.  This script can be rerun with new or updated data from the VCE SB Dashboard.  

# This script can be rerun with new or updated data from the VCE SB Dashboard or data source. Potentially every Quarter.

# Import the OSBP Module
from src.dconfig import pd, data_folders, files, get_file_path
from src.data_processing import generate_csv_from_excel, transform_data, generate_insights
 
# Convert the raw data folder location and the file pattern to search for the latest file in the raw data folder.  #This function will first check to see if the file is older than 30 days.  If < 30, skips the cleanse and transform process.  If > 30, it will convert the file to a csv and then cleanse and transform the data.  The final file will be saved in the interim data folder. https://x.com/i/grok/share/1qrwk5gLfh8orhxLslTG1fAdE

# Define the raw data files to be processed
raw_data_files = [
    get_file_path('raw_data', 'army_raw_data'), 
    get_file_path('raw_data', 'acc_ri_raw_data')
]

# Loop through each raw data file and process it
for raw_data_file in raw_data_files:
    generate_csv_from_excel(raw_data_file, data_folders['interim_data'])

# Define the interim data file(s) to be cleansed and processed (transformed)
interim_data_files = [
    get_file_path('interim_data', 'army_interim_data'),
    get_file_path('interim_data', 'acc_ri_interim_data')
]

# Loop through each interim data file and process it
for interim_data_file in interim_data_files:
    transform_data(interim_data_file, data_folders['processed_data'])

# Start processing data to meet different requirements based on the cleansed data source file.
# Insights Target1 are Full and Opens soliciations that were ultimately awarded to SBs, SBSAs with potential for socio set asides.
baseline_data = get_file_path('processed_data', 'acc_ri_processed_data')
generate_insights(baseline_data, data_folders['processed_data'])

# Insights Target2 are SBSAs with potential for socio set asides.
# sb.insight_sbsa_with_potential_for_socio_set_asides()

# # Insights Target3 are 8(a) awards, both competitive and sole source, where the incumbent 8(a) has a exit date that occurs before the contract expiratino date.
# sb.insight_8a_with_exit_before_expiration()

# Industry Insights.  Process data to provide insights on the industry.
# sb.insight_test2(df)as