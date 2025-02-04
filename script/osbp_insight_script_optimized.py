# Convert initial data pull which comes from VCE SB Dashboard as .xlsx file to .csv file to prepare the data for data cleansing and analysis.  Once converted, move the .csv file to the processed data folder.  This script can be rerun with new or updated data from the VCE SB Dashboard.  

# This script can be rerun with new or updated data from the VCE SB Dashboard or data source. Potentially every Quarter.

# Import the OSBP Module
import osbp_optimized as sb 

# Convert the raw data folder location and the file pattern to search for the latest file in the raw data folder.  #This function will first check to see if the file is older than 30 days.  If < 30, skips the cleanse and transform process.  If > 30, it will convert the file to a csv and then cleanse and transform the data.  The final file will be saved in the interim data folder. https://x.com/i/grok/share/1qrwk5gLfh8orhxLslTG1fAdE
sb.convert_raw_data_from_excel_to_csv()

# Clean and transform the raw csv file and save it in the .  This will become the main file, named 'Data source.csv' to process and rovide a general cleanse of the data and create a dataframe based on it.
sb.clean_and_transform_data_for_contract_profiles()
# df.to_csv(output_file, index=False)

# Start processing data to meet different requirements based on the cleansed data source file.
# Insights Target1 are Full and Opens soliciations that were ultimately awarded to SBs, SBSAs with potential for socio set asides.
# sb.insight_unrestricted_awarded_to_sb()

# Insights Target2 are SBSAs with potential for socio set asides.
# sb.insight_sbsa_with_potential_for_socio_set_asides()

# # Insights Target3 are 8(a) awards, both competitive and sole source, where the incumbent 8(a) has a exit date that occurs before the contract expiratino date.
# sb.insight_8a_with_exit_before_expiration()

# Industry Insights.  Process data to provide insights on the industry.
# sb.insight_test2(df)as