from src.dconfig import get_file_path, pd, np, re

def check_size_standard(df_row, contract_no) -> str:
    """
    Check if the NAICS code value is present in the Size Standard listing (size_standard_list.xlsx).

    Args:
    df_row: The row of the contract being processed.
    contract_no (str): The contract number being processed.

    Returns:
    str: Value from from the 'Size standards in millions of dollars' column.  If 'Size standards in millions of dollars' is not present, return value from 'Size standards in number of employees' column.  If the NAICS value is not present, return "No".
    """
    
     # Get the NAICS value from the df_row from the "NAICS" column
    naics = df_row['NAICS']
    
    # makre sure naics is a string and only the first six digits are used
    naics = str(naics)[:6]

    # Read the Size Standard listing
    size_standard_df = pd.read_csv(get_file_path('size_standards', 'size_standards_list'))
        
    # Make sure the "Size standards in millions of dollars" column is string type
    size_standard_df['Size standards in millions of dollars'] = size_standard_df['Size standards in millions of dollars'].astype(str)
    
    # Make sure the "Size standards in number of employees" column is string type
    size_standard_df['Size standards in number of employees'] = size_standard_df['Size standards in number of employees'].astype(str)
    
    # Check if naics is in the size_standard_df['NAICS Codes'] column. Search the 'Size standards in millions of dollars' column for a value. If a value exists return that value. If no value found move over one column and return its value.  Otherwise, return naics not found message
    if naics in size_standard_df['NAICS Codes'].values:
        if size_standard_df.loc[size_standard_df['NAICS Codes'] == naics, 'Size standards in millions of dollars'].values[0] != 'nan':
            return str(size_standard_df.loc[size_standard_df['NAICS Codes'] == naics, 'Size standards in millions of dollars'].values[0]).strip() + "M"
        else:
            return str(size_standard_df.loc[size_standard_df['NAICS Codes'] == naics, 'Size standards in number of employees'].values[0]).strip() + " Employees"
    else:
        return f'{naics} not found'  
     
def check_wosb_naics(df_row, contract_no) -> str:
    """
    Check if the NAICS code value is present in the Underrepresented WOSB NAICS listing (wosb_naics_list.xlsx).

    Args
    df_row: The row of the contract being processed.    
    Contract_no (str): The contract number being processed in create_contract_profiles() function.

    Returns:
    str: "WOSB" or "EDWOSB" from the 'Set-Aside' column if the NAICS value is present, "No" otherwise.
    """
    
    # Select the NAICS value from the DataFrame based on the current contract number being processed
    naics = df_row['NAICS']
    
    # makre sure naics is a string and only the first six digits are used
    naics = str(naics)[:6]
        
    # Read the WOSB NAICS listing
    wosb_naics_df = pd.read_csv(get_file_path('wosb_naics', 'wosb_naics_list'))
    
    # Ensure the NAICS column is of the same type as naics and only six characters are used
    wosb_naics_df['NAICS Code'] = wosb_naics_df['NAICS Code'].astype(type(naics)).str[:6]

    # Check if naics is in the wosb_naics_df['NAICS Code'] column. If yes, return the value in the 'Set-aside' column. If no, return "No"
    if naics in wosb_naics_df['NAICS Code'].values:
        return wosb_naics_df.loc[wosb_naics_df['NAICS Code'] == naics, 'Set-aside'].values[0]
    else:
        return "No"

def check_if_awardee_sb(df_row, contract_no) -> str:
    """
    Check if the awardee is a small business based on the 'Size Status' column.

    Args:
    df_row: The row of the contract being processed.
    contract_no (str): The contract number being processed.

    Returns:
    str: "SB" if the awardee is a small business, "No" otherwise.
    """
    
    # Select the 'Size Status' value from the dataframe row based on the current contract number being processed
    size_status = df_row['Size Status']
    
    # Check if the 'Size Status' value is "SB". If yes, return "Yes". If no, return "No"
    if size_status == "SB":
        return "Yes"
    else:
        return "No"
    
def check_awardee_socioeconomic_status(df_row, contract_no) -> str:
    """
    Check if the awardee is a socio-economic status based on the 'Size Status' column.

    Args:
    df_row: The row of the contract being processed.
    contract_no (str): The contract number being processed.

    Returns:
    str: All socio categories they are identified as based on the "WOSB", "EDWOSB", "VOSB", "SDVOSB", "8(a)", "HUBZone", or "No" based on the socio-economic status.  If multiple categories are identified, they will be separated by a comma.
    """
    
    # Create a list to store the identified socioeconomic categories
    socioeconomic_categories = []
    
    # Define a dictionary mapping column names to their corresponding categories "key = column : value = category"
    socioeconomic_columns = {
        'SDB Concern Actions': 'SDB',
        'Service Disabled Veterans Actions': 'SDVOSB',
        'Women Owned Actions': 'WOSB',
        'HUB Zone Actions': 'HUBZone'
    }

    # Iterate through the dictionary and check each column
    for column_name, socio_category in socioeconomic_columns.items():
        if df_row[column_name] == 1:
            socioeconomic_categories.append(socio_category)
    
    if socioeconomic_categories:
        return ', '.join(socioeconomic_categories)
    else:
        return "None"
 
def check_if_nmr_waiver_available(df_row, contract_no) -> str:
    """
    Check if an NMR waiver exists based on the NAICS code from the current contract being processed.

    Args:
    df_row: The row of the contract being processed.
    contract_no (str): The contract number being processed.

    Returns:
    str: "Yes" if an NMR waiver exists, "No" otherwise.
    """
    
    # Select the NAICS value from the DataFrame based on the current contract number being processed
    naics = df_row['NAICS']
        
    # makre sure naics is a string and only the first six digits are used
    naics = str(naics)[:6]
    
    # Read the nmr_waiver_list (needs to be saved as CSV UTF-8)
    nmr_waiver_list_df = pd.read_csv(get_file_path('nmr_class_waivers', 'nmr_waiver_list'))
    
    # Ensure the NAICS column is of the same type as naics and only six characters are used
    nmr_waiver_list_df['NAICS CODE'] = nmr_waiver_list_df['NAICS CODE'].astype(type(naics)).str[:6]
    
    # Check if naics is in the nmr_waiver_list_df['NAICS Code'] column.
    if naics in nmr_waiver_list_df['NAICS CODE'].values:
        return "Yes"
    else:
        return "No"
    
def check_acc_ri_awards(df_row, contract_no) -> str:
    """
    Get the number of awards made by ACC-RI to small businesses based on the NAICS code from the current contract being processed.

    Args:
    df_row: The row of the contract being processed.
    contract_no (str): The contract number being processed.

    Returns:
    int: The number of awards made.
    """
     # Select the NAICS value from the DataFrame based on the current contract number being processed
    naics = df_row['NAICS']
    
    # makre sure naics is a string and only the first six characters are used
    naics = str(naics)[:6]
    
    # Use the processed acc_ri_processed_data.csv file to get the modifications
    acc_ri_awards_df = pd.read_csv(get_file_path('processed_data', 'acc_ri_processed_data'))
    
    # Filter df to only show Contract Action Types that are not "MODIFICATION", "SATOC", and "MATOC"
    acc_ri_awards_df = acc_ri_awards_df[~acc_ri_awards_df['Contract Action Type'].str.upper().isin(["MODIFICATION", "MATOC", "SATOC"])]
   
    # Ensure the NAICS column is of the same type as naics and only six characters are used
    acc_ri_awards_df['NAICS'] = acc_ri_awards_df['NAICS'].astype(type(naics)).str[:6] 
    
    acc_ri_awards_df = acc_ri_awards_df.loc[(acc_ri_awards_df['NAICS'] == naics) & (acc_ri_awards_df['Size Status'] == "SB")]

    # If dataframe is empty return "0", else return the number of rows remaining after filter to get the award count
    if acc_ri_awards_df.empty:
        return str(0)
    else:
        return str(acc_ri_awards_df.shape[0])
    
def check_all_acc_awards(df_row, contract_no):
    """
    Get the number of awards made by the Army enterprise to small businesses based on the NAICS code from the current contract being processed.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.

    Returns:
    int: The number of awards made.
    """
    # Select the 'NAICS' value from the DataFrame based on the current contract number being processed
    naics = df.loc[df['Contract No'] == contract_no, 'NAICS'].values[0]
    
    # makre sure naics is a string and only the first six digits are used
    naics = str(naics)[:6]
    # print(contract_no)
    # print(naics)
    # print("")
    
    # Only read the 'NAICS', 'Size Status', and ' columns into df the data source file that will be used to determine award count.
    acc_awards_df = pd.read_csv(data_folders['cleansed_all_army_data_source_file'], usecols=['NAICS', 'Size Status', 'Contract Action Type'])
    # acc_awards_df = pd.read_csv(data_folders['cleansed_all_army_data_source_file'])
  
    # Remove unique_values "Modification", "MATOC", "SATOC" from the 'Contract Action Type' column
    acc_awards_df = acc_awards_df[~acc_awards_df['Contract Action Type'].str.upper().isin(["MODIFICATION", "MATOC", "SATOC"])]
    
    # # Rename column "Small Business Actions" to "Size Status"
    # acc_awards_df = acc_awards_df.rename(columns={"Small Business Actions": "Size Status"})
    
    # # Within Size Status column, replace "0" with "OTSB" and ">0" with "SB"
    # acc_awards_df['Size Status'] = acc_awards_df['Size Status'].replace({0: 'OTSB', 1: 'SB'})
                      
    # Ensure the NAICS column is of the same type as naics and only six digits are used
    acc_awards_df['NAICS'] = acc_awards_df['NAICS'].astype(str).str[:6].astype(type(naics))
    # acc_awards_df['NAICS'] = acc_awards_df['NAICS'].astype(type(naics))
        
    # Ensure the Size Status column is of the same type as "SB" and only six digits are used
    acc_awards_df['Size Status'] = acc_awards_df['Size Status'].astype(str).str.strip()
    
    # print("Dataframe before filter:", acc_awards_df)
    # print("")
    # Filter the acc_awards_df based on the naics identified from the contract being processed
    acc_awards_df = acc_awards_df.loc[(acc_awards_df['NAICS'] == naics) & (acc_awards_df['Size Status'] == "SB")]
    # print("Dataframe after filter:", acc_awards_df)
    # print("")
    
    # If dataframe is empty return "0", else return the number of rows remaining after filter to get the award count
    if acc_awards_df.empty:
        return str(0)
    else:
        return str(acc_awards_df.shape[0])
    
def check_financial_risk(df_row, contract_no) -> str:
    """
    Check the financial risk to industry based on the distribution of SB dollars against the identified NAICS.
    Percentiles will be 50% for Low, 75% for Medium, and 90% and above for High. 

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.

    Returns:
    str: "High", "Medium", "Low", or "No" based on the financial risk.
    """
    
    # Read into df the data source file that will be used to develop the percentiles from the SB Dollars column 
    # Use the below for testing the logic.  It's a smaller data sample.
    # cleansed_file_df = pd.read_csv(data_folders['cleansed_data_source_file'])
    cleansed_file_df = pd.read_csv(data_folders['cleansed_all_army_data_source_file'], usecols=['NAICS', 'Size Status', 'SB Dollars'])
    
    # Define the NAICS values from the DataFrame argument (NOT THE FULL RAW CLEANSED FILE) based on the current contract number being processed.  This will be used to sort the cleansed_file_df to get the percentiles.
    naics = df.loc[df['Contract No'] == contract_no, 'NAICS'].values[0]
    
    # # Print the unique values in the 'NAICS' column to verify the expected value is present
    # print("Unique NAICS values in the DataFrame:", df['NAICS'].unique())
    # print("")
    # print(contract_no)
    # print(naics)
    # print("")

    # Make sure the 'SB Dollars' column is numeric from the DataFrame argument (NOT THE FULL RAW CLEANSED FILE).  This value will be used to compare against the percentiles from the cleansed_file_df.
    # Ensure 'SB Dollars' column is string before removing currency formatting
    df['SB Dollars'] = df['SB Dollars'].astype(str)

    # Remove currency formatting from the SB Dollars column
    df['SB Dollars'] = df['SB Dollars'].str.replace('$', '').str.replace(',', '')

    # Convert the SB Dollars column to numeric
    df['SB Dollars'] = pd.to_numeric(df['SB Dollars'], errors='coerce')

    # Make sure the 'SB Dollars' column is numeric from the DataFrame argument (NOT THE FULL RAW CLEANSED FILE). This value will be used to compare against the percentiles from the cleansed_file_df.
    sb_dollars = df.loc[df['Contract No'] == contract_no, 'SB Dollars'].values[0]
    # print('SB Dollars before conversion: ', sb_dollars)
    
    # sb_dollars = pd.to_numeric(df.loc[df['Contract No'] == contract_no, 'SB Dollars'].values[0], errors='coerce')
    # print('SB Dollars after conversion: ', sb_dollars)
    # print("")

    # Filter the cleased_file_df based on the naics identified from the contract being processed and print the filtered result to check if it matches the expected rows
    filtered_df = cleansed_file_df.loc[(cleansed_file_df['NAICS'] == naics) & (cleansed_file_df['Size Status'] == "SB")]
    # print("Filtered DataFrame based on NAICS:", filtered_df)

    # Check if the 'SB Dollars' column contains the expected values from the full raw cleansed file (latest_cleansed_file_df)
    if not filtered_df.empty:
        # Print the 'SB Dollars' column before conversion
        # print("SB Dollars column before conversion:", filtered_df['SB Dollars'])
        
        # Convert 'SB Dollars' column to numeric values
        filtered_df.loc[:, 'SB Dollars'] = pd.to_numeric(filtered_df['SB Dollars'], errors='coerce')
        
        # Print the 'SB Dollars' column after conversion
        # print("SB Dollars column after conversion:", filtered_df['SB Dollars'])
        
        sb_dollars_values = filtered_df['SB Dollars'].values
        # print("SB Dollars Values:", sb_dollars_values)
        
        # Calculate the percentiles
        p50 = np.percentile(sb_dollars_values, 50)
        p75 = np.percentile(sb_dollars_values, 75)
        p90 = np.percentile(sb_dollars_values, 90)
        
        # print(f"50th Percentile (Low Risk): ${p50}")
        # print(f"75th Percentile (Medium Risk): ${p75}")
        # print(f"90th Percentile (High Risk): ${p90}")
        
        # Determine the risk level for the current contract's SB Dollars
        if sb_dollars <= p50:
            risk_level = "Low Risk"
        elif sb_dollars <= p75:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"
        
        return risk_level

def check_targeted_naics(df_row, contract_no) -> str:
    """
    Check if the NAICS code value is one of the Targeted Econcomic Sector (first two digits of NAICS) identified.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.

    Returns:
    str:  If NAICS is present, return "Yes". Otherwise, return "No".
    """
    
    # Get the NAICS value from the df_row from the "NAICS" column
    naics = df_row['NAICS']
    
    # makre sure naics is a string and only the first two digits are used
    naics = str(naics)[:2]
    
    # Define the targeted NAICS values.  Based on OSBP or Contracting goals.
    targeted_naics = ['33', '51', '54']
    
    # Check if the 'NAICS' value is in the targeted_naics list. If yes, return "Yes". If no, return "No"
    if naics in targeted_naics:
        return "Yes"
    else:
        return "No"

def check_top_naics(df_row, contract_no) -> str:
    """
    Check if the NAICS code value is one of the Top 25 NAICS identified by the amount of SB Actions or SB Dollars.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.

    Returns:
    str:  If NAICS is present, return "Yes". Otherwise, return "No".
    """
    
    cleansed_file_df = pd.read_csv(data_folders['cleansed_data_source_file'], usecols=['NAICS', 'Size Status', 'SB Dollars'])
    
    # Select the 'NAICS' value from the DataFrame based on the current contract number being processed
    naics = df.loc[df['Contract No'] == contract_no, 'NAICS'].values[0]
    
    # makre sure naics is a string and only the first six digits are used
    naics = str(naics)[:6]
    
  
    # Get the count for top 30% of NAICS based on SB Dollars or SB actions
    top_naics_count = 25
    
    
    # Make sure the 'SB Dollars' column is numeric from the DataFrame argument (NOT THE FULL RAW CLEANSED FILE).  This value will be used to compare against the percentiles from the cleansed_file_df.
    # Ensure 'SB Dollars' column is string before removing currency formatting
    cleansed_file_df['SB Dollars'] = cleansed_file_df['SB Dollars'].astype(str)

    # Remove currency formatting from the SB Dollars column
    cleansed_file_df['SB Dollars'] = cleansed_file_df['SB Dollars'].str.replace('$', '').str.replace(',', '')

    # Convert the SB Dollars column to numeric
    cleansed_file_df['SB Dollars'] = pd.to_numeric(cleansed_file_df['SB Dollars'], errors='coerce')
    
    # Ensure the 'NAICS' column is of the same type as naics and only six digits are used
    cleansed_file_df['NAICS'] = cleansed_file_df['NAICS'].astype(str).str[:6].astype(type(naics))
    
    # Filter the cleased_file_df based on the naics identified from the contract being processed and print the filtered result to check if it matches the expected rows
    # filtered_df = cleansed_file_df.loc[(cleansed_file_df['NAICS'] == naics) & (cleansed_file_df['Size Status'] == "SB")]
    filtered_df = cleansed_file_df.loc[(cleansed_file_df['Size Status'] == "SB")]
    # print("Filtered DataFrame based on NAICS and Size Status:", filtered_df)
    # print("")
    
    # Define the targeted NAICS values based on the top 30% of unique NAICS based on total SB Dollars
    filtered_df = filtered_df.groupby('NAICS').agg({'SB Dollars': 'sum'}).reset_index()
    filtered_df = filtered_df.sort_values(by=['SB Dollars'], ascending=False)
    top_naics_by_dollars = filtered_df['NAICS'].head(top_naics_count).tolist()
    # print("Top NAICS by SB Dollars:", top_naics_by_dollars)
    # print("")
    
    # Define the targeted NAICS values based on the top 30% of unique NAICS based on total SB Actions (determined by "Size Status" column).
    filtered_df = cleansed_file_df.loc[(cleansed_file_df['Size Status'] == "SB")]
    filtered_df = filtered_df.groupby('NAICS').agg({'Size Status': 'count'}).reset_index()
    filtered_df = filtered_df.sort_values(by=['Size Status'], ascending=False)
    top_naics_by_actions = filtered_df['NAICS'].head(top_naics_count).tolist()
    # print("Top NAICS by SB Actions:", top_naics_by_actions)
    # print("")
    
    # top_naics = ['541611', '541512', '541330']
    
    # Check if the 'NAICS' value is in either top_naics_by_actions or top_naics_by_actions. If yes in either one, return "Yes". If not in either, return "No"
    if naics in top_naics_by_dollars or naics in top_naics_by_actions:
        return "Yes"
    else:
        return "No"    
    
    # if naics in top_naics:
    #     return "Yes"
    # else:
    #     return "No"

def check_strong_naics(df_row, contract_no) -> str:
    """
    Check if the NAICS code value is one of the Top 30% of unique NAICS identified by the amount of SB Actions or SB Dollars.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.

    Returns:
    str:  If NAICS is present, return "Yes". Otherwise, return "No".
    """
    
    cleansed_file_df = pd.read_csv(data_folders['cleansed_data_source_file'], usecols=['NAICS', 'Size Status', 'SB Dollars'])
    
    # Select the 'NAICS' value from the DataFrame based on the current contract number being processed
    naics = df.loc[df['Contract No'] == contract_no, 'NAICS'].values[0]
    
    # makre sure naics is a string and only the first six digits are used
    naics = str(naics)[:6]
    
    # Idnentify the number of uniqe values in the 'NAICS' column by count !!MAY HAVE TO ALSO KEEP IT THE LAST 3 YEARS OF DATA!!
    naics_count = cleansed_file_df['NAICS'].nunique()
    # print("Number of unique NAICS values:", naics_count)
    # print("")
    
    # Get the count for top 30% of NAICS based on SB Dollars or SB actions
    strong_naics_count = int(naics_count * .3)
    # print("Top 30% of NAICS count:", strong_naics_count)
    # print("")
    
    # Make sure the 'SB Dollars' column is numeric from the DataFrame argument (NOT THE FULL RAW CLEANSED FILE).  This value will be used to compare against the percentiles from the cleansed_file_df.
    # Ensure 'SB Dollars' column is string before removing currency formatting
    cleansed_file_df['SB Dollars'] = cleansed_file_df['SB Dollars'].astype(str)

    # Remove currency formatting from the SB Dollars column
    cleansed_file_df['SB Dollars'] = cleansed_file_df['SB Dollars'].str.replace('$', '').str.replace(',', '')

    # Convert the SB Dollars column to numeric
    cleansed_file_df['SB Dollars'] = pd.to_numeric(cleansed_file_df['SB Dollars'], errors='coerce')
    
    # Ensure the 'NAICS' column is of the same type as naics and only six digits are used
    cleansed_file_df['NAICS'] = cleansed_file_df['NAICS'].astype(str).str[:6].astype(type(naics))
    
    # Filter the cleased_file_df based on the naics identified from the contract being processed and print the filtered result to check if it matches the expected rows
    # filtered_df = cleansed_file_df.loc[(cleansed_file_df['NAICS'] == naics) & (cleansed_file_df['Size Status'] == "SB")]
    filtered_df = cleansed_file_df.loc[(cleansed_file_df['Size Status'] == "SB")]
    # print("Filtered DataFrame based on NAICS and Size Status:", filtered_df)
    # print("")
    
    # Define the targeted NAICS values based on the top 30% of unique NAICS based on total SB Dollars
    filtered_df = filtered_df.groupby('NAICS').agg({'SB Dollars': 'sum'}).reset_index()
    filtered_df = filtered_df.sort_values(by=['SB Dollars'], ascending=False)
    strong_naics_by_dollars = filtered_df['NAICS'].head(strong_naics_count).tolist()
    # print("Top NAICS by SB Dollars:", strong_naics_by_dollars)
    # print("")
    
    # Define the targeted NAICS values based on the top 30% of unique NAICS based on total SB Actions (determined by "Size Status" column).
    filtered_df = cleansed_file_df.loc[(cleansed_file_df['Size Status'] == "SB")]
    filtered_df = filtered_df.groupby('NAICS').agg({'Size Status': 'count'}).reset_index()
    filtered_df = filtered_df.sort_values(by=['Size Status'], ascending=False)
    strong_naics_by_actions = filtered_df['NAICS'].head(strong_naics_count).tolist()
    # print("Top NAICS by SB Actions:", strong_naics_by_actions)
    # print("")
    
    # top_naics = ['541611', '541512', '541330']
    
    # Check if the 'NAICS' value is in either top_naics_by_actions or top_naics_by_actions. If yes in either one, return "Yes". If not in either, return "No"
    if naics in strong_naics_by_dollars or naics in strong_naics_by_actions:
        return "Yes"
    else:
        return "No"    
    
    # if naics in top_naics:
    #     return "Yes"
    # else:
    #     return "No"

# def check_weak_naics(df, contract_no) -> str:
    """
    Check if the NAICS code value is one of the Weak NAICS in ACC-RI by 10th percentile of SB Dollars or SB Actions.
    
    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.
    
    returns:
    str:  If NAICS is present in the 10th percentile, return "Yes". Otherwise, return "No".
    """
    # Read into df the data source file that will be used to develop the percentiles from the  Dollars column
    df = pd.read_csv(data_folders['cleansed_data_source_file'], usecols=['Contract No', 'NAICS', 'Size Status'])
        
    # Select the 'NAICS' value from the DataFrame based on the current contract number being processed
    naics = df.loc[df['Contract No'] == contract_no, 'NAICS'].values[0]
    
    # makre sure naics is a string and only the first six digits are used
    naics = str(naics)[:6]
    
    # Filter the DataFrame for rows where 'Size Status' is "SB"
    filtered_df = df[df['Size Status'] == "SB"]

    # Group by 'NAICS' and count the occurrences
    naics_count_df = filtered_df.groupby('NAICS').size().reset_index(name='count')
    
    # Calculate the 10th percentile of the 'count' column
    tenth_percentile = np.percentile(naics_count_df['count'], 10)
    
    # Filter the 'NAICS' values that fall within the 10th percentile
    weak_naics = naics_count_df[naics_count_df['count'] <= tenth_percentile]['NAICS'].values
    # print("Weak NAICS:", weak_naics)
    # print("")
    
    if naics in weak_naics:
        return "Yes"
    else:
        return "No"

def check_weak_naics(df_row, contract_no) -> str:
    """
    Check if the NAICS code value is one of the Top 30% of unique NAICS identified by the amount of SB Actions or SB Dollars.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.

    Returns:
    str:  If NAICS is present, return "Yes". Otherwise, return "No".
    """
    
    cleansed_file_df = pd.read_csv(data_folders['cleansed_data_source_file'], usecols=['NAICS', 'Size Status', 'SB Dollars'])
    
    # Select the 'NAICS' value from the DataFrame based on the current contract number being processed
    naics = df.loc[df['Contract No'] == contract_no, 'NAICS'].values[0]
    
    # makre sure naics is a string and only the first six digits are used
    naics = str(naics)[:6]
    
    # Idnentify the number of uniqe values in the 'NAICS' column by count !!MAY HAVE TO ALSO KEEP IT THE LAST 3 YEARS OF DATA!!
    naics_count = cleansed_file_df['NAICS'].nunique()
    # print("Number of unique NAICS values:", naics_count)
    # print("")
    
    # Get the count for top 30% of NAICS based on SB Dollars or SB actions
    weak_naics_count = int(naics_count * .3)
    # print("Top 30% of NAICS count:", strong_naics_count)
    # print("")
    
    # Make sure the 'SB Dollars' column is numeric from the DataFrame argument (NOT THE FULL RAW CLEANSED FILE).  This value will be used to compare against the percentiles from the cleansed_file_df.
    # Ensure 'SB Dollars' column is string before removing currency formatting
    cleansed_file_df['SB Dollars'] = cleansed_file_df['SB Dollars'].astype(str)

    # Remove currency formatting from the SB Dollars column
    cleansed_file_df['SB Dollars'] = cleansed_file_df['SB Dollars'].str.replace('$', '').str.replace(',', '')

    # Convert the SB Dollars column to numeric
    cleansed_file_df['SB Dollars'] = pd.to_numeric(cleansed_file_df['SB Dollars'], errors='coerce')
    
    # Ensure the 'NAICS' column is of the same type as naics and only six digits are used
    cleansed_file_df['NAICS'] = cleansed_file_df['NAICS'].astype(str).str[:6].astype(type(naics))
    
    # Filter the cleased_file_df based on the naics identified from the contract being processed and print the filtered result to check if it matches the expected rows
    # filtered_df = cleansed_file_df.loc[(cleansed_file_df['NAICS'] == naics) & (cleansed_file_df['Size Status'] == "SB")]
    filtered_df = cleansed_file_df.loc[(cleansed_file_df['Size Status'] == "SB")]
    # print("Filtered DataFrame based on NAICS and Size Status:", filtered_df)
    # print("")
    
    # Define the targeted NAICS values based on the top 30% of unique NAICS based on total SB Dollars
    filtered_df = filtered_df.groupby('NAICS').agg({'SB Dollars': 'sum'}).reset_index()
    filtered_df = filtered_df.sort_values(by=['SB Dollars'], ascending=True)
    weak_naics_by_dollars = filtered_df['NAICS'].head(weak_naics_count).tolist()
    # print("Top NAICS by SB Dollars:", strong_naics_by_dollars)
    # print("")
    
    # Define the targeted NAICS values based on the top 30% of unique NAICS based on total SB Actions (determined by "Size Status" column).
    filtered_df = cleansed_file_df.loc[(cleansed_file_df['Size Status'] == "SB")]
    filtered_df = filtered_df.groupby('NAICS').agg({'Size Status': 'count'}).reset_index()
    filtered_df = filtered_df.sort_values(by=['Size Status'], ascending=True)
    weak_naics_by_actions = filtered_df['NAICS'].head(weak_naics_count).tolist()
    # print("Top NAICS by SB Actions:", strong_naics_by_actions)
    # print("")
    
    # top_naics = ['541611', '541512', '541330']
    
    # Check if the 'NAICS' value is in either top_naics_by_actions or top_naics_by_actions. If yes in either one, return "Yes". If not in either, return "No"
    if naics in weak_naics_by_dollars or naics in weak_naics_by_actions:
        return "Yes"
    else:
        return "No"    
    
    # if naics in top_naics:
    #     return "Yes"
    # else:
    #     return "No"
       
# def check_forecast(df, contract_no) -> str:
    """
    Check if the contract is a forecasted action.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.

    Returns:
    str: "Yes" if the contract is a forecasted action, "No" otherwise.
    """
    forecast = df.loc[df['Contract No'] == contract_no, 'Forecast'].values[0]
    
    if forecast == 1:
        return "Yes"
    else:
        return "No"

def check_modification(df_row,contract_no) -> str:
    '''
    Check if the contract has a modification and get the most recent number identified sorted by the most recent award date.
    
    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.
    
    Returns:
    str: The most recent modification number.
    '''
    
    # Use the processed acc_ri_processed_data.csv file to get the modifications
    mod_df = pd.read_csv(get_file_path('processed_data', 'acc_ri_processed_data'))
    
    # Filter the df based on the contract_no identified from the contract being processed where Contract Action Type is "MODIFICATION"
    mod_df = mod_df.loc[(mod_df['Contract No'] == contract_no) & (mod_df['Contract Action Type'] == "MODIFICATION")]
    
    # Sort the modifications_df by 'Award Date' in descending order
    mod_df = mod_df.sort_values(by='Award Date', ascending=False)
    
    # Get the most recent 'Modification Number' from the modifications_df
    if mod_df.empty:
        return "No Modifications"
    else:
        return mod_df.iloc[0]['Modification No']
    
def check_forecast(df_row, contract_no) -> str:
        '''
        Check if the contract is a forecasted action and return the VCE-PCF Cabinet Name.
        
        Args:
        df (pd.DataFrame): The DataFrame containing the data to be processed.
        contract_no (str): The contract number being processed.
        
        Returns:
        str: The VCE-PCF Cabinet Name.
        '''
        # Define the forecast file which will be the cleansed data source file
        forecast_df = pd.read_csv(data_folders['forecast_file'], usecols=['VCE-PCF Cabinet Name', 'FOLLOWON CONTRACT'])
        
        # Search the "FOLLOWON CONTRACT" column in the forecast_df for the contract_no identified from the contract being processed
        forecast_df = forecast_df.loc[forecast_df['FOLLOWON CONTRACT'] == contract_no]
        if contract_no in forecast_df['FOLLOWON CONTRACT'].values:
            return str(forecast_df['VCE-PCF Cabinet Name'].values[0])
        else:
            return "No Forecast Identified"
        
def check_pcf_cabinet_link(df_row, contract_no) -> str:
    '''
    Check the file and determine if there is a link to the identified contract being processes.
    
    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.
    
    Returns:
    str: The hyperlink to the PCF Cabinet.
    '''
    # Define the file where hyperlinks are stored
    hyperlink_df = pd.read_csv(data_folders['hyperlinks_file'], usecols= ['PCF Access', 'Contract', 'Order'])
    
    #Define Order No from argument df
    order_no = df.loc[df['Contract No'] == contract_no, 'Order No'].values[0] 
        
    # Define the base URL for the PCF Cabinet
    base_url = "https://pcf.army.mil/pcf/login.htm?t=1460636157811&cabinetName="

    # Construct the full URL by appending the contract number to the base URL
    # hyperlink = f"{base_url}{contract_no}"

    # Check if order no is in the hyperlink_df['Order'] column. If a value exists, return the value from the PCF Access column from the hyperlink_df.  If no, check if contract_no is in the hyperlink_df['Contract"] column. If a value exists, return the value of PCF Access column from hyperlink_df.  Otherwise, return naics not found message.
    if order_no in hyperlink_df['Order'].values:
        return hyperlink_df.loc[hyperlink_df['Order'] == order_no, 'PCF Access'].values[0]
        # return f"{base_url}{order_no}"
    elif contract_no in hyperlink_df['Contract'].values:
        return hyperlink_df.loc[hyperlink_df['Contract'] == contract_no, 'PCF Access'].values[0]
        # return f"{base_url}{contract_no}"
    else:
        return f'No PCF cabinet link found'
    
  
    return hyperlink

def check_it_buy(df_row, contract_no) -> str:
    """
    Check the NAICS Description, PSC Description, OMB Level 1 and OMB Level 2 columns for certain combinations and keywords to determine if it is an IT buy.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.

    Returns:
    str: "Yes" if the NAICS description contains specific keywords, "No" otherwise.
    """
    # Define the IT Buy keywords
    it_buy_keywords = ['IT', 'INFORMATION TECHNOLOGY', 'TECHNOLOGY', 'SOFTWARE', 'HARDWARE', 'COMPUTER', 'NETWORK', 'CYBERSECURITY', 'CLOUD', 'DATA', 'ANALYTICS', 'AI', 'ARTIFICIAL INTELLIGENCE', 'MACHINE LEARNING', 'ML', 'IOT', 'INTERNET OF THINGS', 'BLOCKCHAIN', 'CRYPTO', 'CRYPTOCURRENCY', 'DIGITAL', 'ELECTRONIC', 'TELECOMMUNICATIONS', 'TELECOMM', 'TELECOM', 'TELEPHONE', 'TELEPHONY', 'TELEPHONIC', 'TELEPHONICS']
    
    # Use columns 'NAICS', 'NAICS Description', 'PSC Decription', 'OMB Level 1', and 'OMB Level 2' to check for IT Buy keywords from df argument
    naics_description = df.loc[df['Contract No'] == contract_no, 'NAICS Description'].values[0]
    psc_description = df.loc[df['Contract No'] == contract_no, 'PSC Description'].values[0]
    omb_level_1 = df.loc[df['Contract No'] == contract_no, 'OMB Level 1'].values[0]
    omb_level_2 = df.loc[df['Contract No'] == contract_no, 'OMB Level 2'].values[0]
    
    # # Check if any of the IT Buy keywords are present in the 'NAICS Description', 'PSC Description', 'OMB Level 1', or 'OMB Level 2' columns
    # if any(keyword in naics_description.upper() for keyword in it_buy_keywords) or any(keyword in psc_description.upper() for keyword in it_buy_keywords) or any(keyword in omb_level_1.upper() for keyword in it_buy_keywords) or any(keyword in omb_level_2.upper() for keyword in it_buy_keywords):
    #     return "Yes"
    # else:
    #     return "No"
    
    # Create a regex pattern to match whole words only
    pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in it_buy_keywords) + r')\b'
    
    # Check if any of the IT Buy keywords are present in the 'NAICS Description', 'PSC Description', 'OMB Level 1', or 'OMB Level 2' columns
    if (re.search(pattern, naics_description, re.IGNORECASE) or
        re.search(pattern, psc_description, re.IGNORECASE) or
        re.search(pattern, omb_level_1, re.IGNORECASE) or
        re.search(pattern, omb_level_2, re.IGNORECASE)):
        return "Yes"
    else:
        return "No"

def check_socio_sole_source_eligible(df_row, contract_no) -> str:
    """
    Check if the contract is eligible for sole source award based on the dollar value.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    contract_no (str): The contract number being processed.

    Returns:
    str: "Yes" if the contract is eligible for sole source award based on the $4M threshold for SDVOSB and $4.5M for all others, "No" otherwise.
    """
    # Select the 'Socio-Economic Status' value from the DataFrame based on the current contract number being processed
    sdvosb_sole_source_threshold = 4000000
    all_others_sole_source_threshold = 4500000
    
    # create a list of all other sole source thresholds
    all_eligible_sole_source_categories = ['8(a)', 'HUBZone', 'WOSB', 'EDWOSB', 'SDVOSB']
    eligible_sole_sole_categories_above_sdvosb_threshold = ['8(a)', 'HUBZone', 'WOSB', 'EDWOSB']
    eligible_sole_source_categories_above_sdvosb_not_wosb_naics_list = ['8(a)', 'HUBZone']
    eligible_sole_sole_categories_not_on_wosb_naics_list = ['8(a)', 'HUBZone', 'SDVOSB']
    
    #Get dollar value from the 'SB Dollars' from df argument based on the contract_no being processed
    sb_dollars = df.loc[df['Contract No'] == contract_no, 'SB Dollars'].values[0]
    #Remove currency formatting from sb_dollars
    sb_dollars = sb_dollars.replace('$', '').replace(',', '')
    
    # Convert the 'SB Dollars' value to numeric
    sb_dollars = pd.to_numeric(sb_dollars, errors='coerce')    
        
    # # If the SB dollars less than sdvosb_sole_source_threshold AND the WOSB NAICS list is "Yes", return all_eligible_sole_source_categories as str
    # if sb_dollars > all_others_sole_source_threshold:
    #     return 'No'
    # elif sb_dollars >= sdvosb_sole_source_threshold and check_wosb_naics(df, contract_no) == "No":
    #     return ', '.join(eligible_sole_source_categories_above_sdvosb_not_wosb_naics_list)
    # elif sb_dollars <= sdvosb_sole_source_threshold and check_wosb_naics(df, contract_no) == "No":
    #     return ', '.join(eligible_sole_sole_categories_not_on_wosb_naics_list)
    # elif sb_dollars >= sdvosb_sole_source_threshold and check_wosb_naics(df, contract_no) != "No":
    #     return ', '.join(eligible_sole_sole_categories_above_sdvosb_threshold)
    # elif sb_dollars <= sdvosb_sole_source_threshold and check_wosb_naics(df, contract_no) != "No":
    #     return ', '.join(all_eligible_sole_source_categories)
    
sb_profile_analysis_functions = {
    # "IT Buy" : check_it_buy, # Check NAICS desription to determine if it is an IT buy, search for specific keywords and return yes or no
    # "Strong Competition" : check_strong_competition, # Get a sense of average number of offerors against this NAICS (use all army data source file)
    "Size Standard" : check_size_standard,
    # "Top NAICS" : check_top_naics, #Top 25 NIACS either by SB Dollars or SB Actions
    "Target NAICS" : check_targeted_naics, #NAICS identified by specific needs or objectives or rationales/logic
    "WOSB Eligible" : check_wosb_naics, # Check if the NAICS code value is present in the Underrepresented WOSB NAICS listing
    # "Strong NAICS" : check_strong_naics, #Top 30% of NAICS based on SB Dollars or SB Actions
    # "Weak NAICS" : check_weak_naics, #10th percentile of SB Dollars or SB Actions
    # "Socio SS Eligible" : check_socio_sole_source_eligible, # Check if the $ value is below the threshold ($4M SDVOSB, $4.5M all others)
    "Awardee SB" : check_if_awardee_sb,
    "Awardee Socio" : check_awardee_socioeconomic_status,
    "NMR Waiver Available" : check_if_nmr_waiver_available, #Does an NMR waiver exist based on NAICS
    "ACC RI Awards" : check_acc_ri_awards, #Awards that went to SB under the identified NAICS
    # "All ACC Awards" : check_all_acc_awards, #All awards made by ACC across the enterprise# "Financial Risk" : check_financial_risk, #Financial risk to industry based on distribution of SB awards under identified NAICS"
    "Modification No" : check_modification, #Check if the contract is a modification and get the most recent number
    # "PCF Cabinet" : check_pcf_cabinet_link, #Provide link to PCF Cabinet and return a str or hyperlink
    # "Forecast No" : check_forecast # Identify the forecast solicitation/PANCOC number
} 