# Contain all the common folders and files that are used for the contract profile project.

import pandas as pd
import numpy as np
import os, glob, datetime, re


# Establish the base folder path for the project
base_folder = r'C:\GitHub\Contract_Profiles'

# Folders and file paths for the project
data_folders = {
    'raw_data' : os.path.join(base_folder, 'data', 'raw'),
    'interim_data' : os.path.join(base_folder, 'data', 'interim'),
    'processed_data' : os.path.join(base_folder, 'data', 'processed'),
    'references_data' : os.path.join(base_folder, 'references'),
    'nmr_class_waivers' : os.path.join(base_folder, 'references', 'nmr_class_waivers'),
    'size_standards' : os.path.join(base_folder, 'references', 'size_standards'),
    'wosb_naics' : os.path.join(base_folder, 'references', 'wosb_naics'),
    'forecasts' : os.path.join(base_folder, 'references', 'forecasts'),
    'reports' : os.path.join(base_folder, 'reports'),
    'contract_profiles' : os.path.join(base_folder, 'reports', 'contract_profiles'),
    'insight_unrestricted_sb_awards' : os.path.join(base_folder,'data', 'processed', 'insight_unrestricted_sb_awards'),
    'insight_sbsa' : os.path.join(base_folder,'data', 'processed', 'insight_sbsa'),
    'insight_8a_exit' : os.path.join(base_folder, 'data', 'processed', 'insight_8a_exit'),
    'insight_unrestricted_otsb_awards' : os.path.join(base_folder, 'data', 'processed', 'insight_unrestricted_otsb_awards'),
}

files = {
    'acc_ri_raw_data' : 'acc_ri_raw_data.xlsx',
    'army_raw_data' : 'army_raw_data.xlsx',
    'acc_ri_interim_data' : 'acc_ri_interim_data.csv',
    'army_interim_data' : 'army_interim_data.csv',
    'acc_ri_processed_data' : 'acc_ri_processed_data.csv',
    'army_processed_data' : 'army_processed_data.csv',
    'nmr_waiver_list' : 'nmr_waiver_list.csv',
    'size_standards_list' : 'size_standards_list.csv',
    'wosb_naics_list' : 'wosb_naics_list.csv',
    'osbp_forecast' : 'Data source.csv',
    'amc_forecast' : 'Data source.csv',
    'profile_template' : 'template_profile.docx',
    'insight1' : 'insight_unrestricted_sb_awards.csv',
    'insight2' : 'insight_sbsa.csv',
    'insight3' : 'insight_8a_exit.csv',
    'insight4' : 'insight_unrestricted_otsb_awards.csv',
}

# Function to contstruct paths to specific files
def get_file_path(folder, file):
    return os.path.join(data_folders[folder], files[file])
    
#Example usage:
# army_raw_data_file = get_file_path('raw_data', 'acc_ri_raw_data_file')

# Create a dictionary of Contract Profile Data Elements to populate the Contract Profile Data Elements table in the Contract Profile Word Document.
contract_profile_data_elements = {
    "1A" : "Contract No",
    "1A2" : "Order No",
    "1B" : "Modification No",
    "2A" : "Award Date",
    "2B" : "Effective Date",
    "2D" : "Expiration",
    "6A" : "Contract Type",
    "6M" : "Requirements Description",
    "8G" : "NAICS",
    "8N" : "Bundling",
    "9G" : "Place of Performance",
    "10C" : "Limited Competition",
    "10D" : "Number of Offerors",
    "10N" : "Type Set Aside Description",
    "11B" : "SubK Plan",
    "12A" : "GWAC", #Includes Agency IDIQs
    "13GG" : "Awardee",
    "CAT" : "Contract Action Type",
    "CPAR" : "CPARS Rating",
    "ESRS" : "SubK Achievement",
    "SB$" : "SB Dollars",
    "STS" : "Size Status", #originally "Small Business Actions" (0 = OTSB and 1 = SB)
    "FC" : "Forecast No", # Identify the forecast solicitation/PANCOC number
    "PCF" : "PCF Cabinet", #Provide link to PCF Cabinet
    # "FCL" : "Forecast Link", #Provide link to Forecast PCF Cabinet
}

sb_profile_analysis_elements = {
    "IT" : "IT Buy", 
    "ITSS" : "IT Services SONA",
    "SComp" : "Strong Competition",
    "SStd" : "Size Standard",
    "TNAICS:" : "Top NAICS",
    "TgtNAICS" : "Target NAICS",
    "WElg" : "WOSB Eligible",
    # "SoSSElg" : "Socio SS Eligible",
    "SNAICS" : "Strong NAICS",
    "WNAICS" : "Weak NAICS",
    "RIAwd" : "ACC RI Awards", #Awards that went to small under the identified NAICS
    "AAwd" : "All ACC Awards", #All awards made by ACC across the enterprise
    "SkR" : "Subcontract MQRs Realistic",
    "AwdSB" : "Awardee SB",
    "AwdSoc" : "Awardee Socio",
    "Mult" : "Multiple Products or Services",
    "NMRW" : "NMR Waiver Available", #Does an NMR waiver exist based on NAICS
    "NMRP" : "NMR Potential", #Potential for NMR based on requirements
    "FinC" : "Financial Risk", #Financial risk to industry based on distribution of SB awards under identified NAICS
    # "Rmks" : "Remarks"
}

sb_categories = {   
    "sb" : "SB",
    "d"  : "SDB",
    "w"  : "WOSB",
    "ew" : "EDWOSB",
    "v" : "VOSB",
    "sv" : "SDVOSB",
    "8a" : "8(a)",
    "hz" : "HUBZone",
}
# common settings
common_settings = {
    'max_rows' : 5, # For testing purposes
    'max_months_remaining' : 24, # Maximum number of months remaining on a contract
    'min_months_remaining' : 6, # Minimum number of months remaining on a contract
    'targeted_naics' : ['33', '51', '54'], # Target NAICS for the project based on customer and DoD/Army objectives
    'top_naics_count' : 25, # Number of top NAICS to consider for analysis
    'strong_naics_percentage' : .30, # Percentage of awards to be considered strong NAICS
}
