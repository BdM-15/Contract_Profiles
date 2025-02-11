#Data processing functions used for processing the data for the contract profile project.
from ..utils.gen_utils import does_folder_exist, get_file_name
from ..dconfig import pd, os, datetime, data_folders, files, get_file_path, common_settings

# This function will find the latest file and convert the raw data file from .xlsx to .csv and move it to the interim data folder.  It will also log the conversion details in a log file.
def generate_csv_from_excel(raw_file: str, interim_data_folder: str) -> str:
    """
    Convert a raw data file from .xlsx to .csv and move it to the interim data folder.
        
    Args:
    None

    Returns:
    str: The path to the converted file in the interim data folder.
    """

    # Extract the base name, replace with inerim and update the extension with .csv
    csv_file_name = get_file_name(raw_file).replace('raw', 'interim') + '.csv'
    interim_data_file = os.path.join(interim_data_folder, csv_file_name)
    
    # Read the latest raw data file 
    df = pd.read_excel(raw_file)
    
    # Convert the latest raw data file to a CSV file and save it to the cleansed data folder
    df.to_csv(interim_data_file, index=False)
        
    # Print the conversion details to the console
    today_date = datetime.datetime.now().strftime('%Y-%m-%d') 
    print(f"{raw_file} was successfully converted to {interim_data_file} on {today_date}.")

    # Log the conversion details
    log_file = os.path.join(data_folders['raw_data'], 'OSBP-RI_data_conversion_log.txt') 
    with open(log_file, 'a') as log:
        log.write(f"The raw data to for the OSBP Insights was converted on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nRaw data file: {raw_file}\nConverted file: {interim_data_file}\nConverted csv file location: {interim_data_folder}\n\n")
    print(f"Conversion details logged in {log_file}")
    
    return interim_data_file

def transform_acc_ri_data(interim_file, processed_folder: str):
    """
    Clean and transforme the data. Ensure the proper data types are used; rename any columns to align with desired result.  Also, save any formatting for the point in which it will be analyzed.  For example, don't add currency formatting at this point.  Just make sure numbers are numeric, dates are dates, and text is text.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be cleaned.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
     
    # Read the csv file
    df = pd.read_csv(interim_file)
    
    # Remove any rows and columns that are completely empty
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')

    # Remove any duplicate rows
    df = df.drop_duplicates()

    # # Reduce the memory usage of the DataFrame by converting columns with object dtype to category dtype
    # df = df.astype({col: 'category' for col in df.select_dtypes('object').columns})
    
    # Rename column "13GG Legal Business Name (UEI)" to "Awardee"
    df = df.rename(columns={"13GG Legal Business Name (UEI)": "Awardee"})
    
    # Rename column "10N Type Set Aside Description" to "Type Set Aside Description"
    df = df.rename(columns={"10N Type Set Aside Description": "Type Set Aside Description"})
    
    # Remove the . from the values in the 'Type Set Aside Description' column
    df['Type Set Aside Description'] = df['Type Set Aside Description'].str.replace('.', '')
    
    # If a blank value exsits in "10N Type Set Aside Description" replace it with "NO SET ASIDE USED."
    df['Type Set Aside Description'] = df['Type Set Aside Description'].fillna("NO SET ASIDE USED")
    
    # Rename column "6M Desription of Requirement" to "Requirements Description"
    df = df.rename(columns={"6M Description of Requirement": "Requirements Description"})
        
    # Rename column "Current Completion Date" to "Exipriation"
    df = df.rename(columns={"Current Completion Date": "Expiration"})
    
    # Rename column "Small Business Actions" to "Size Status"
    df = df.rename(columns={"Small Business Actions": "Size Status"})
    
    # # Within Size Status column, replace "0" with "OTSB" and "1" with "SB"
    # df['Size Status'] = df['Size Status'].replace({0: 'OTSB', 1: 'SB'})
    
    # Rename column "Small Business Dollars" to "SB Dollars"
    df = df.rename(columns={"Small Business Dollars": "SB Dollars"})
        
    # Ensure the NAICS code is a string and only first six digits are used
    df['NAICS'] = df['NAICS'].astype(str).str[:6]
    
    # Convert the 'Expiration' column to datetime to match format with today_date and make it only 10 characters long
    df['Expiration'] = df['Expiration'].str[:10]
    df['Expiration'] = pd.to_datetime(df['Expiration'], errors='coerce')
    
    # Convert the "Award Date" column to datetime to match format with today_date
    df['Award Date'] = pd.to_datetime(df['Award Date'], errors='coerce')

    # For each row, calulate the number of months remaining to complete the contract and input the number of months remaining in the 'Months Remaining' column
    df['Months Remaining'] = (df['Expiration'] - pd.Timestamp.today()).dt.days // 30

    # Add a new column next to the 'Current Completion' column and insert the 'Months Remaining' column
    df.insert(df.columns.get_loc('Expiration') + 1, 'Months Remaining', df.pop('Months Remaining'))
    
    # Save the cleaned data copy to the cleansed data folder using the destination_folder argument
    df.to_csv(get_file_path('processed_data', 'acc_ri_processed_data'), index=False)
    
def transform_army_data(interim_file, processed_folder: str):
    """
    Clean and transforme the data. Ensure the proper data types are used; rename any columns to align with desired result.  Also, save any formatting for the point in which it will be analyzed.  For example, don't add currency formatting at this point.  Just make sure numbers are numeric, dates are dates, and text is text.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be cleaned.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
  
    # Read the csv file
    df = pd.read_csv(interim_file)
    
    # Remove any rows and columns that are completely empty
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')

    # Remove any duplicate rows
    df = df.drop_duplicates()
    
    # Rename column "Small Business Actions" to "Size Status"
    df = df.rename(columns={"Small Business Actions": "Size Status"})
    
    # Within Size Status column, replace any values > 0 with 1
    df['Size Status'] = df['Size Status'].apply(lambda x: 1 if x > 0 else 0)
    # df['Size Status'] = df['Size Status'].replace({0: 'OTSB', 1: 'SB'})
    
    # Rename column "Small Business Dollars" to "SB Dollars"
    df = df.rename(columns={"Small Business Dollars": "SB Dollars"})
    
    #Remove rows where "Size Status" is 1 and SB Dollars is 0
    # df = df[~((df['Size Status'] == 1) & (df['SB Dollars'] == 0))]
    
    #Remove rows where "Size Status" is 0 and SB Dollars is < 10000 (less than $10,000 = Micro Purchase)
    df = df[~((df['Size Status'] == 0) & (df['SB Dollars'] < 10000))]
        
    # Ensure the NAICS code is a string and only first six digits are used
    df['NAICS'] = df['NAICS'].astype(str).str[:6]
    
    #Remove all rows where the "Contract Action Type" is "MODIFICATION", "SATOC", and "MATOC"
    df = df[~df['Contract Action Type'].str.upper().isin(["MODIFICATION", "SATOC", "MATOC"])]
    
    # Save the cleaned data copy to the cleansed data folder using the destination_folder argument
    df.to_csv(get_file_path('processed_data', 'army_processed_data'), index=False)

def transform_data(interim_file, processed_folder: str):
    """Process each file from script based on their respective data cleansing requirements."""
    
    if "army" in interim_file:
        transform_army_data(interim_file, processed_folder)
    elif "acc_ri" in interim_file:
        transform_acc_ri_data(interim_file, processed_folder)
  
def insight_unrestricted_sb_awards(baseline_file, insight_folder_name) -> None:
    """
    Process the data to sort for the targeted contracts.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.

    Returns:
    None
    """
    
    # Define the cleansed data source file to create a DataFrame (df)
    df = pd.read_csv(baseline_file)
    
    #Remove all rows where the "Contract Action Type" is "MODIFICATION", "SATOC", and "MATOC"
    df = df[~df['Contract Action Type'].str.upper().isin(["MODIFICATION", "SATOC", "MATOC"])]
    
    #  # Within Size Status column, replace "0" with "OTSB" and "1" with "SB"
    # df['Size Status'] = df['Size Status'].replace({0: 'OTSB', 1: 'SB'})
   
    # Remove any rows that are not "NO SET ASIDE USED" or blank in the "10N Type Set Aside Description" column
    df = df[df['Type Set Aside Description'].isin(["NO SET ASIDE USED", ""])]
    
    # Remove any rows with Months reaminining less than 6 months and more than 18 months
    df = df[(df['Months Remaining'] >= common_settings['min_months_remaining']) & (df['Months Remaining'] <= common_settings['max_months_remaining'])]
    
    # Remove any rows with 0 in the "Size Status"
    df = df[df['Size Status'] != 0]
    
    # Sort "Months Remaining" in ascending order
    df = df.sort_values(by='Months Remaining', ascending=True)
    
    # Save the insight list based on the file name listed in the files dictionary in confjg
    output_file = get_file_path('insight_unrestricted_sb_awards', 'insight1')
    df.to_csv(output_file, index=False)

def insight_sbsa(baseline_file, insight_folder_name) -> None:
    """
    Process the data to sort for the targeted contracts.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.

    Returns:
    None
    """
    
    # Define the cleansed data source file to create a DataFrame (df)
    df = pd.read_csv(baseline_file)
    
    #Remove all rows where the "Contract Action Type" is "MODIFICATION", "SATOC", and "MATOC"
    df = df[~df['Contract Action Type'].str.upper().isin(["MODIFICATION", "SATOC", "MATOC"])]
    
    #  # Within Size Status column, replace "0" with "OTSB" and "1" with "SB"
    # df['Size Status'] = df['Size Status'].replace({0: 'OTSB', 1: 'SB'})
   
    # Remove any rows that contain "NO SET ASIDE USED" in the "Type Set Aside Description" column
    df = df[~df['Type Set Aside Description'].isin(["NO SET ASIDE USED"])]
    
    # Remove any rows with Months reaminining less than 6 months and more than 18 months
    df = df[(df['Months Remaining'] >= common_settings['min_months_remaining']) & (df['Months Remaining'] <= common_settings['max_months_remaining'])]
    
    # Remove any rows with 0 in the "Size Status"
    df = df[df['Size Status'] != 0]
    
    # Sort "Months Remaining" in ascending order
    df = df.sort_values(by='Months Remaining', ascending=True)
    
    # Save the insight list based on the file name listed in the files dictionary in confjg
    output_file = get_file_path('insight_sbsa', 'insight2')
    df.to_csv(output_file, index=False)
    
def insight_8a_exit(baseline_file, insight_folder_name) -> None:
    """
    Process the data to sort for the targeted contracts.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.

    Returns:
    None
    """
    # Define the cleansed data source file to create a DataFrame (df)
    df = pd.read_csv(baseline_file)
    
    #Remove all rows where the "Contract Action Type" is "MODIFICATION", "SATOC", and "MATOC"
    df = df[~df['Contract Action Type'].str.upper().isin(["MODIFICATION", "SATOC", "MATOC"])]
    
    #  # Within Size Status column, replace "0" with "OTSB" and "1" with "SB"
    # df['Size Status'] = df['Size Status'].replace({0: 'OTSB', 1: 'SB'})
   
    # Remove any rows that are not "8(A) SOLE SOURCE" OR "8A COMPETED" in the "Type Set Aside Description" column
    df = df[df['Type Set Aside Description'].str.upper().isin(["8(A) SOLE SOURCE", "8A COMPETED"])]
    
    # Remove any rows with Months reaminining less than 6 months and more than 18 months
    df = df[(df['Months Remaining'] >= common_settings['min_months_remaining']) & (df['Months Remaining'] <= common_settings['max_months_remaining'])]
    
    # Sort "Months Remaining" in ascending order
    df = df.sort_values(by='Months Remaining', ascending=True)
    
    # Save the insight list based on the file name listed in the files dictionary in confjg
    output_file = get_file_path('insight_8a_exit', 'insight3')
    df.to_csv(output_file, index=False)
    
def insight_unrestricted_otsb_awards(baseline_file, insight_folder_name) -> None:
    """
    Process the data to sort for the targeted contracts.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.

    Returns:
    None
    """
    
    # Define the cleansed data source file to create a DataFrame (df)
    df = pd.read_csv(baseline_file)
    
    # Remove any rows with 1 in the "Size Status"
    df = df[df['Size Status'] != 1]
    
    #Remove all rows where the "Contract Action Type" is "MODIFICATION", "SATOC", and "MATOC"
    df = df[~df['Contract Action Type'].str.upper().isin(["MODIFICATION", "SATOC", "MATOC"])]

    # Remove any rows with Months reaminining less than 6 months and more than 18 months
    df = df[(df['Months Remaining'] >= common_settings['min_months_remaining']) & (df['Months Remaining'] <= common_settings['max_months_remaining'])]
    
    # Sort "Months Remaining" in ascending order
    df = df.sort_values(by='Months Remaining', ascending=True)
    
    # Save the insight list based on the file name listed in the files dictionary in confjg
    output_file = get_file_path('insight_unrestricted_otsb_awards', 'insight4')
    df.to_csv(output_file, index=False)
    
def generate_insights(baseline_data, insight_folder):
    """
    Generate insights based on the insights identified in insight functions dictionary. Each insight is based on the baseline data provided.

    Args:
    processed_data_folder (str): The path to the folder containing the processed data.
    insight_folder (str): The path to the folder where the insights will be saved.

    Returns:
    None
    """
   # Define the mapping of insight keys to functions
    insight_functions = {
        'insight1': insight_unrestricted_sb_awards,
        'insight2': insight_sbsa,
        'insight3': insight_8a_exit,
        'insight4': insight_unrestricted_otsb_awards,
    }
    
    # Loop through each insight function and generate the insights using the baseline data for each insight
    for insight_key, insight_function in insight_functions.items():
        # Create a folder name based on the function name
        function_name = insight_function.__name__
        insight_folder_name = os.path.join(insight_folder, function_name)
        
        # Ensure the folder exists
        does_folder_exist(insight_folder_name)
        
        print(f"Running insight {insight_function.__name__}")
        insight_function(baseline_data, insight_folder_name)