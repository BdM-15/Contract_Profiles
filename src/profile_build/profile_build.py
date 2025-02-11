from ..dconfig import pd, os, datetime, data_folders, get_file_path, contract_profile_data_elements, sb_profile_analysis_elements, common_settings
from ..sb_analysis import *
from docx import Document
from ..utils.gen_utils import does_folder_exist, does_file_exist, get_file_name, set_cell_font
import shutil

def get_inisght_data(insight_file) -> pd.DataFrame:
    """Loads the data based on the specifically insight argument."""
    
    insight_df = pd.read_csv(insight_file)
        
    return insight_df

def get_document_path(completed_profiles_path, contract_no):
    """Generate a path for a new contract profile document based on the insight being processed."""
    
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    filename = f'{contract_no.replace("/", "_")}_{today_date}.docx'
    
    return os.path.join(completed_profiles_path, filename)

def copy_profile_template(template_file, contract_profile) -> Document:
    """Prepare a new document based on the template document."""
    # Copy the template to the new location
    shutil.copy(template_file, contract_profile)

    return contract_profile

def create_contract_details_table(formal_template, insight_dictionary) -> Document:
    """Create the Contract Details table using the data elements from the insight_dictionary argument.
    
    Args:
    formal_template (docx.Document): The document to which the table will be added.
    insight_dictionary (dict): The dictionary containing the data elements to be added to the table.
    
    Returns:
    Table: The table containing the Contract Details.
    """
    profile  = Document(formal_template)
    table = profile.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    
    if len(table.rows) > 1:
        table._tbl.remove(table.rows[0]._tr)
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].merge(hdr_cells[1]).merge(hdr_cells[2]).merge(hdr_cells[3])
    
    hdr_cells[0].text = 'Contract Details'
    hdr_cells[0].paragraphs[0].alignment = 1  # Center alignment
    
    set_cell_font(hdr_cells[0], font_size=11, bold=True)

    return table

def populate_contract_details_table(df, contract_no, formal_template, insight_dictionary) -> Document:
    """Populate the Contract Details table in the document for all rows."""
    table = create_contract_details_table(formal_template, insight_dictionary)
    
    values = list(insight_dictionary.values())
    for i in range(0, len(values), 2):
        row_cells = table.add_row().cells
        row_cells[0].text = values[i]
        row_cells[1].text = str(row[values[i]]) if values[i] in df.columns else 'Data Gap'
        if i + 1 < len(values):
            row_cells[2].text = values[i + 1]
            row_cells[3].text = str(row[values[i + 1]]) if values[i + 1] in df.columns else 'Data Gap'
        else:
            row_cells[2].text = ''
            row_cells[3].text = ''
        for cell in row_cells:
            set_cell_font(cell)
    
    #Add paragraph break to ensure the next table is not connected to the previous one
    formal_template.add_paragraph()
        
    return table

def create_sb_profile_analysis_table(formal_template) -> Document:
    """Create and return the Small Business Profile Analysis table."""
    table = formal_template.add_table(rows=1, cols=6)
    table.style = 'Table Grid'
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].merge(hdr_cells[1]).merge(hdr_cells[2]).merge(hdr_cells[3].merge(hdr_cells[4]).merge(hdr_cells[5]))
    
    hdr_cells[0].text = 'Small Business Profile Analysis'
    hdr_cells[0].paragraphs[0].alignment = 1  # Center alignment
    
    set_cell_font(hdr_cells[0], font_size=11, bold=True)
    
    return table

def populate_sb_profile_analysis_table(df, contract_no, formal_template) -> Document:
    """Populate the Small Business Profile Analysis table in the document and check for functions from the sb_analysis modules sb_profile_analysis_functions dictionary."""
    table = create_sb_profile_analysis_table(formal_template)
    
    values = list(sb_profile_analysis_elements.values())
    for i in range(0, len(values), 3):
        row_cells = table.add_row().cells
        row_cells[0].text = values[i]
        if values[i] in sb_profile_analysis_functions:
            row_cells[1].text = sb_profile_analysis_functions[values[i]](df, contract_no)
        else:
            row_cells[1].text = str(row[values[i]]) if values[i] in df.columns else ''
        if i + 1 < len(values):
            row_cells[2].text = values[i + 1]
            if values[i + 1] in sb_profile_analysis_functions:
                row_cells[3].text = sb_profile_analysis_functions[values[i + 1]](df, contract_no)
            else:
                row_cells[3].text = str(row[values[i + 1]]) if values[i + 1] in df.columns else ''
        else:
            row_cells[2].text = ''
            row_cells[3].text = ''
        if i + 2 < len(values):
            row_cells[4].text = values[i + 2]
            if values[i + 2] in sb_profile_analysis_functions:
                row_cells[5].text = sb_profile_analysis_functions[values[i + 2]](df, contract_no)
            else:
                row_cells[5].text = str(row[values[i + 2]]) if values[i + 2] in df.columns else ''
        else:
            row_cells[4].text = ''
            row_cells[5].text = ''
        for cell in row_cells:
            set_cell_font(cell)
    
    # Add a final row titled "Remarks" in the first cell and the remaining 3 cells are mergec and left blank
    row_cells = table.add_row().cells
    row_cells[0].text = 'Remarks'
    row_cells[1].merge(row_cells[2]).merge(row_cells[3].merge(row_cells[4]).merge(row_cells[5]))
    for cell in row_cells:
        set_cell_font(cell)
    #Add paragraph break to ensure the next table is not connected to the previous one
    formal_template.add_paragraph()
    
    return table

def generate_profiles(insight_file, completed_profiles_folder):
    """
    Populate the Contract Details tables based on the Contract Profile Data Elements dictionary.

    Args:
    df (pd.DataFrame): The DataFrame containing the data to be processed.
    template_path (str): The path to the template document.
    completed_folder (str): The path to the folder where completed documents will be saved.

    Returns:
    None
    """
    # Does the completed_profiles folder exist? If not, create it.
    does_folder_exist(completed_profiles_folder)
    
    # Create a folder within the copmleted_profiles_folder based on the name of the insight file being processed
    insight_name = get_file_name(insight_file)
    insight_profiles = os.path.join(completed_profiles_folder, insight_name)
    does_folder_exist(insight_profiles)
        
    # Load the insight data
    df = get_inisght_data(insight_file)

    # Get dictionary from dconfig based on the insight being processed
    sb_profile_analysis_functions = contract_profile_data_elements
        
    # Identify the profile template to be used
    template_file = get_file_path('reports', 'profile_template')
            
    # Identify the path for the specific contract profile based on the insight being processed
    profile_location = get_document_path(insight_profiles, df["Contract No"].replace('/', '_'))
    
    # Create a new document based on the template
    profile_document = copy_profile_template(template_file, profile_location)
    
    # Load the template document
    profile = Document(profile_document)

    # Create and populate the Contract Details table
    profile = create_contract_details_table(profile, contract_profile_data_elements)
    profile = populate_contract_details_table(df, df["Contract No"], profile, contract_profile_data_elements)
    
    # Create and populate the Small Business Profile Analysis table
    profile = create_sb_profile_analysis_table(profile, df, df["Contract No"])
    profile = populate_sb_profile_analysis_table(df, df["Contract No"], profile)
            
    # Save the populated document
    profile.save(insight_profiles)
    print(f"Populated contract details saved to: {insight_profiles}")

    # Create a log of completed contracts and check the amount of documents compared to the amount of rows in the DataFrame
    log_file = os.path.join(completed_profiles_folder, 'completed_profiles_log.txt')
    with open(log_file, 'a') as log:
        log.write(f"Completed profiles on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nCompleted contracts location: {insight_profiles}\n\n")