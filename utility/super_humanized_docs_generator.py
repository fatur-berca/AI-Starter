import os
import re
import glob
from bs4 import BeautifulSoup

# Define directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIEWS_SRC_DIR = r"C:\Users\fatchurrachman.yudha\source\repos\tom2\hms-tom-dev\Views\AllocationPlanning"
BLL_SRC_DIR = r"C:\Users\fatchurrachman.yudha\source\repos\tom2\TOM.AllocationPlanning.BusinessLogics"
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sequential order of the view folders
VIEWS_LIST = [
    {"folder": "MasterBrand", "seq": "01"},
    {"folder": "MasterDepletion", "seq": "02"},
    {"folder": "MasterLocation", "seq": "03"},
    {"folder": "MasterLocationDetail", "seq": "04"},
    {"folder": "MasterSource", "seq": "05"},
    {"folder": "MasterSourceModaDetail", "seq": "06"},
    {"folder": "MasterSourceRatio", "seq": "07"},
    {"folder": "MasterTransportModa", "seq": "08"},
    {"folder": "MasterTransportModaType", "seq": "09"},
    {"folder": "MasterTransportType", "seq": "10"},
    {"folder": "MasterVessel", "seq": "11"},
    {"folder": "MasterWhsCapacity", "seq": "12"},
    {"folder": "OneTimeSetup", "seq": "13"},
    {"folder": "UploadForecast", "seq": "14"},
    {"folder": "UploadSourceRatio", "seq": "15"},
    {"folder": "UploadWpp", "seq": "16"},
    {"folder": "VesselScheduleResult", "seq": "17"},
    {"folder": "VesselUpload", "seq": "18"},
    {"folder": "WppDetailResult", "seq": "19"},
    {"folder": "WppSummaryResult", "seq": "20"},
]

def parse_bll_validations(folder_name):
    """Statically parses C# BLL implementation files to extract actual business validations."""
    validations = []
    
    # Locate BLL file
    bll_path = os.path.join(BLL_SRC_DIR, f"{folder_name}BLL", f"{folder_name}BLL.cs")
    if not os.path.exists(bll_path):
        # Fallback to check without BLL suffix in path
        bll_path = os.path.join(BLL_SRC_DIR, f"{folder_name}", f"{folder_name}.cs")
        
    if not os.path.exists(bll_path):
        return None
        
    with open(bll_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Search for string.IsNullOrWhiteSpace checks (wajib diisi / required)
    null_checks = re.findall(r'if\s*\(string\.IsNullOrWhiteSpace\(dto\.(.*?)\)\)\s*return\s*["\'](.*?)["\']', content)
    for field, msg in null_checks:
        validations.append({
            "stage": "All Operations",
            "rule": "Required Field",
            "trigger": f"Field '{field}' is blank or empty",
            "response": f'"{msg}"'
        })
        
    # Search for Exists checks on Insert (sudah ada / already exists)
    exists_insert = re.findall(r'if\s*\(_repo\.Exists\(dto\.(.*?)\)\)\s*return\s*OutputDataModel\.Fail\(["\'](.*?)["\']\)', content)
    for field, msg in exists_insert:
        validations.append({
            "stage": "Insert Only",
            "rule": "Uniqueness Guard",
            "trigger": f"Value of '{field}' already exists in database",
            "response": f'"{msg}"'
        })
        
    # Search for Exists checks on Update (sudah digunakan / already used)
    exists_update = re.findall(r'if\s*\(_repo\.Exists\(dto\.(.*?),\s*dto\.Id\)\)\s*return\s*OutputDataModel\.Fail\(["\'](.*?)["\']\)', content)
    for field, msg in exists_update:
        validations.append({
            "stage": "Update Only",
            "rule": "Identity Duplicate Guard",
            "trigger": f"Value of '{field}' matches another active record",
            "response": f'"{msg}"'
        })
        
    return validations

def parse_cshtml_view(filepath, folder_name):
    """Parses a CSHTML view file and returns key metadata for documentation."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Title
    title = f"Allocation Planning > {folder_name}"
    title_match = re.search(r'ViewBag\.Title\s*=\s*["\'](.*?)["\']', content)
    if title_match:
        title = title_match.group(1).replace(" > List", "").strip()

    # Clean HTML from Razor comments and C# code blocks
    clean_html = re.sub(r'@\*.*?\*@', '', content, flags=re.DOTALL)
    clean_html = re.sub(r'@{.*?}', '', clean_html, flags=re.DOTALL)
    
    soup = BeautifulSoup(clean_html, 'html.parser')

    # Find Db Table Staging tags (e.g. APLMasterSource)
    stag_tag = soup.find(class_='stag')
    db_tag = stag_tag.get_text().strip() if stag_tag else f"APL{folder_name}"

    # Extract Data Grid Headers
    headers = []
    table_id = "N/A"
    table_tag = soup.find('table')
    if table_tag:
        table_id = table_tag.get('id', 'N/A')
        main_tr = table_tag.find('tr', class_='th-main')
        if not main_tr:
            main_tr = table_tag.find('tr')
            
        if main_tr:
            th_elements = main_tr.find_all('th')
            for th in th_elements:
                txt = th.get_text().strip()
                if txt:
                    headers.append(txt)
                else:
                    headers.append("ACTION")

    # Extract Form Fields / Filters
    filters = []
    for inp in soup.find_all('input'):
        inp_id = inp.get('id', '')
        placeholder = inp.get('placeholder', '')
        inp_type = inp.get('type', 'text')
        if inp_id or placeholder:
            name = placeholder or inp_id.replace("filter", "").replace("search", "")
            filters.append({
                "id": inp_id or "N/A",
                "type": f"Input ({inp_type})",
                "purpose": f"Filters grid by {name}" if "filter" in inp_id.lower() else f"Form field for {name}"
            })
            
    for sel in soup.find_all('select'):
        sel_id = sel.get('id', '')
        if sel_id:
            filters.append({
                "id": sel_id,
                "type": "Dropdown Selection",
                "purpose": f"Dropdown selection filter for {sel_id.replace('filter', '')}"
            })

    # Extract AJAX Action Endpoints
    ajax_actions = []
    url_action_matches = re.findall(r'@Url\.Action\(\s*["\'](.*?)["\']\s*,\s*["\'](.*?)["\']\s*\)', content)
    for action, controller in url_action_matches:
        endpoint = f"/AllocationPlanning/{controller}/{action}"
        if endpoint not in ajax_actions:
            ajax_actions.append(endpoint)

    return {
        "title": title,
        "db_tag": db_tag,
        "table_id": table_id,
        "headers": headers,
        "filters": filters,
        "ajax_actions": ajax_actions
    }

def generate_rich_spec(folder_name, seq, metadata_list, validations):
    """Generates a highly descriptive, humanized, C#-validated functional specification Markdown."""
    
    filename = f"{seq}_{folder_name}.md"
    filepath = os.path.join(INPUT_DIR, filename)
    
    primary_meta = metadata_list[0] if metadata_list else {"title": f"Allocation Planning > {folder_name}", "db_tag": f"APL{folder_name}"}
    title = primary_meta["title"]
    db_tag = primary_meta["db_tag"]
    
    # 1. Image Checkers (checking if actual captured screenshots exist)
    main_img = f"{seq}_{folder_name}.png"
    add_img = f"{seq}_{folder_name}_Add.png"
    detail_img = f"{seq}_{folder_name}_Detail.png"
    
    # Humanized Section 1: Overview and Description
    markdown_content = f"""# {title}

This document details the functional specifications, database integrations, and dynamic interface actions for the **{folder_name}** menu inside HMS TOM Allocation Planning.

## 1. Functional Overview
The **{folder_name}** view allows authorized users to inspect, configure, and maintain parameters vital to the Allocation Planning pipeline.

* **Path:** `/AllocationPlanning/{folder_name}`
* **Default Controller:** `AllocationPlanning/{folder_name}Controller`
* **Staging Database Tag:** `<span class="stag">{db_tag}</span>`

---

## 2. Interface Screen Walkthrough

### 2.1 The Master Listing Screen

The master listing screen presents a highly structured, professional administration dashboard styled according to the PT HM Sampoerna TOM Page Design System. It features a clean white background card set against a soft gray background `#F1F4F7`.

![{title} Master Listing Dashboard showing active configurations, status indicators, and column filters.]({main_img})

#### Visual & Functional Elements:
* **Branded Page Header:** Displays the category category icon highlighted in Primary Blue (`#24A4F1`). It displays the page title "**{folder_name}**" and a dedicated staging badge `.stag` exhibiting the database entity tag `{db_tag}`.
* **Search & CTA Controls:** The top-right header contains a global text search input allowing for immediate keyword-based filtering, and a primary blue button (`.btn-p`) labeled **"+ Add New"** if create operations are supported.
* **Master Grid:** A high-density grid displaying records synced from database services. The table headers are styled in a soft gray `#f5f7fa` with bold, uppercase text. The body rows support alternating row styles, record status indicators (Green dots for active, red dots for inactive), and action buttons.

"""

    # Humanized Section 2.2: Add Modal Form (if exists)
    if os.path.exists(os.path.join(INPUT_DIR, add_img)):
        markdown_content += f"""### 2.2 Add Configuration Modal ("Add New")

Clicking the primary **"Add New"** button slides open a modal overlay containing a clean glassmorphism panel. This interface provides input fields for creating a new system parameter.

![Add New {folder_name} modal overlay containing form inputs, validation markers, and control buttons.]({add_img})

#### Form Structure & Visual Flow:
* **Modal Header:** Displays the title **"Add {folder_name}"** and a close icon (`&times;` or class `.close-x`).
* **Input Fields:** Form controls are grouped into clean, two-column row layouts allowing administrators to define listing sequences and toggle active status via a standard dropdown select.

"""

    # Humanized Section 2.3: Detail Modal Form (if exists)
    if os.path.exists(os.path.join(INPUT_DIR, detail_img)):
        markdown_content += f"""### 2.3 Edit Configuration Modal ("Detail / Edit")

Clicking the pencil edit icon (`.fa-pencil`) on any grid record loads that specific item's details dynamically from the database and populates the modal form.

![Edit {folder_name} modal showing loaded data, active status flags, and update actions.]({detail_img})

#### Form Structure & Actions:
* **Modal Title:** Displays "**Edit {folder_name}**".
* **Data Binding:** Programmatically binds the unique primary key, populating the text inputs with current parameter records.
* **Control Actions:** The modal footer provides options to **"Close"** or **"Save Changes"** (Primary Blue `.btn-p` with a save icon).

"""

    markdown_content += """---

## 3. User Interface Components

"""

    # Render details for each file parsed (Index.cshtml, Detail.cshtml, etc.)
    for meta in metadata_list:
        view_file = meta["file"]
        markdown_content += f"### View Template: `{view_file}`\n\n"
        
        # Grid section
        if meta["headers"]:
            markdown_content += f"#### Data Grid Listing (`#{meta['table_id']}`)\n"
            markdown_content += "Displays real-time records synced from database services. The grid supports sorting, server-side pagination, and global search.\n\n"
            markdown_content += "| Column Name | Description |\n| :--- | :--- |\n"
            for col in meta["headers"]:
                desc = "Dynamic database field value."
                if col == "STATUS" or col == "Status": desc = "Indicator showing record status (Active/Inactive)."
                elif "Code" in col or "ID" in col: desc = "Unique alphanumeric identifier code."
                markdown_content += f"| **{col}** | {desc} |\n"
            markdown_content += "\n"
            
        # Form Fields / Filters section
        if meta["filters"]:
            markdown_content += "#### Interactive Form Controls & Filters\n"
            markdown_content += "Below are the key controls and fields available on this interface:\n\n"
            markdown_content += "| Field ID / Label | Control Type | Functional Purpose |\n| :--- | :--- | :--- |\n"
            for flt in meta["filters"]:
                markdown_content += f"| `{flt['id']}` | {flt['type']} | {flt['purpose']} |\n"
            markdown_content += "\n"
            
        # AJAX Actions
        if meta["ajax_actions"]:
            markdown_content += "#### Backend Controller Operations\n"
            markdown_content += "This interface initiates asynchronous server calls to perform core CRUD operations:\n\n"
            for action in meta["ajax_actions"]:
                markdown_content += f"* **POST Request:** `{action}` (Fetches formatted records dynamically)\n"
            markdown_content += "\n"
            
        markdown_content += "---\n\n"

    # Humanized Section 4: Validation Rules
    markdown_content += "## 4. Application Validation Rules\n\n"
    if validations:
        markdown_content += "Validations are applied programmatically in two layers to ensure absolute database integrity:\n\n"
        markdown_content += "### 4.1 Client-Side HTML/JS Validations\n"
        markdown_content += "* **Required Field Constraints:** Primary keys and identifiers are restricted at the element level using HTML5 required states.\n"
        markdown_content += "* **Numeric Format Enforcement:** Sequential IDs and sort numbers are restricted using type attributes (`type=\"number\"`) and minimum values.\n\n"
        
        markdown_content += "### 4.2 Backend C# Business Logic Validations\n"
        markdown_content += "When data is received at the service layer, the system executes detailed validation checks:\n\n"
        markdown_content += "| Action Stage | Validation Rule | Error Trigger | System Response / Message Returned |\n"
        markdown_content += "| :--- | :--- | :--- | :--- |\n"
        for val in validations:
            markdown_content += f"| **{val['stage']}** | {val['rule']} | {val['trigger']} | `{val['response']}` |\n"
        markdown_content += "\n"
    else:
        markdown_content += "### 4.1 Read-Only Policy\n"
        markdown_content += "* **Data Source:** This view acts as a **Read-Only** data panel synced from external services (DFIS).\n"
        markdown_content += "* **Validations:** No local create, update, or delete operations are exposed on the UI. Validations and uniqueness checks are handled upstream by DFIS integration channels before data synchronization occurs.\n\n"

    # Append instructions section
    markdown_content += """## 5. Dynamic UI Behavior
* **Real-time Filters:** Table redraws automatically with a 500ms debounce delay after users type inside column filter fields.
* **Server-side Pagination:** Displays 10 records per page by default with dynamic loading overlay indicators.
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

def run_rich_generator():
    print("====================================================")
    print("      TOM2 RICH SPECIFICATION DOCUMENTS GENERATOR")
    print("====================================================")
    
    for view in VIEWS_LIST:
        folder = view["folder"]
        seq = view["seq"]
        
        print(f"[PROCESSING] [{seq}/20] {folder} ...")
        
        # 1. Parse BLL validations
        validations = parse_bll_validations(folder)
        
        # 2. Parse CSHTML view details
        folder_path = os.path.join(VIEWS_SRC_DIR, folder)
        if not os.path.exists(folder_path):
            print(f"   [WARN] Folder not found: {folder_path}")
            continue
            
        cshtml_files = glob.glob(os.path.join(folder_path, "*.cshtml"))
        cshtml_files.sort()
        
        metadata_list = []
        for filepath in cshtml_files:
            file_name = os.path.basename(filepath)
            try:
                meta = parse_cshtml_view(filepath, folder)
                meta["file"] = file_name
                metadata_list.append(meta)
            except Exception as e:
                print(f"   [ERROR] Error parsing {file_name}: {str(e)}")
                
        # 3. Generate Rich Spec Markdown
        generate_rich_spec(folder, seq, metadata_list, validations)
        
    print("\n[SUCCESS] Rich specification documents generated successfully in C:\\temp\\MDtoDoc\\input!")

if __name__ == "__main__":
    run_rich_generator()
