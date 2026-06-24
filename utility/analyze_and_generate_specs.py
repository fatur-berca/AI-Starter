import os
import re
import glob
from bs4 import BeautifulSoup

# Sequential order of the view folders
VIEW_ORDER = [
    "MasterBrand",
    "MasterDepletion",
    "MasterLocation",
    "MasterLocationDetail",
    "MasterSource",
    "MasterSourceModaDetail",
    "MasterSourceRatio",
    "MasterTransportModa",
    "MasterTransportModaType",
    "MasterTransportType",
    "MasterVessel",
    "MasterWhsCapacity",
    "OneTimeSetup",
    "UploadForecast",
    "UploadSourceRatio",
    "UploadWpp",
    "VesselScheduleResult",
    "VesselUpload",
    "WppDetailResult",
    "WppSummaryResult",
]

VIEWS_SRC_DIR = r"C:\Users\fatchurrachman.yudha\source\repos\tom2\hms-tom-dev\Views\AllocationPlanning"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "input"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_cshtml_view(filepath, folder_name):
    """Parses a CSHTML view file and returns key metadata for documentation."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract Title
    title = f"Allocation Planning > {folder_name}"
    title_match = re.search(r'ViewBag\.Title\s*=\s*["\'](.*?)["\']', content)
    if title_match:
        title = title_match.group(1).replace(" > List", "").strip()

    # Clean HTML from Razor comments and C# code blocks for clean BeautifulSoup parsing
    clean_html = re.sub(r'@\*.*?\*@', '', content, flags=re.DOTALL) # Remove razor comments
    clean_html = re.sub(r'@{.*?}', '', clean_html, flags=re.DOTALL)  # Remove inline code blocks
    
    soup = BeautifulSoup(clean_html, 'html.parser')

    # 2. Extract Data Grid Headers
    headers = []
    table_id = "N/A"
    table_tag = soup.find('table')
    if table_tag:
        table_id = table_tag.get('id', 'N/A')
        # Find headers in main header row (usually th-main or the first tr)
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
                    headers.append("[Action/Status]")

    # 3. Extract Form Fields / Filters
    filters = []
    # Search for input fields
    for inp in soup.find_all('input'):
        inp_id = inp.get('id', '')
        placeholder = inp.get('placeholder', '')
        inp_type = inp.get('type', 'text')
        if inp_id or placeholder:
            name = placeholder or inp_id.replace("filter", "").replace("search", "")
            filters.append({
                "id": inp_id or "N/A",
                "type": f"Input ({inp_type})",
                "purpose": f"Filters table rows by {name}" if "filter" in inp_id.lower() else f"User entry for {name}"
            })
            
    # Search for select elements
    for sel in soup.find_all('select'):
        sel_id = sel.get('id', '')
        if sel_id:
            filters.append({
                "id": sel_id,
                "type": "Dropdown Selection",
                "purpose": f"Dropdown selection filter for {sel_id.replace('filter', '')}"
            })

    # 4. Extract AJAX Action Endpoints
    ajax_actions = []
    url_action_matches = re.findall(r'@Url\.Action\(\s*["\'](.*?)["\']\s*,\s*["\'](.*?)["\']\s*\)', content)
    for action, controller in url_action_matches:
        endpoint = f"/AllocationPlanning/{controller}/{action}"
        if endpoint not in ajax_actions:
            ajax_actions.append(endpoint)

    return {
        "title": title,
        "table_id": table_id,
        "headers": headers,
        "filters": filters,
        "ajax_actions": ajax_actions
    }

def generate_spec_markdown(folder_name, seq, metadata_list):
    """Generates a structured, beautiful functional specification markdown document."""
    
    filename = f"{seq}_{folder_name}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # We will combine metadata of all views inside the folder (e.g. Index.cshtml, Detail.cshtml)
    primary_meta = metadata_list[0] if metadata_list else {"title": f"Allocation Planning > {folder_name}"}
    title = primary_meta["title"]
    
    markdown_content = f"""# {title}

This document details the functional specifications, database integrations, and dynamic interface actions for the **{folder_name}** menu inside HMS TOM Allocation Planning.

![{title} View Interface Screen]({seq}_{folder_name}.png)

## 1. Functional Overview
The **{folder_name}** view allows authorized users to inspect, configure, and maintain parameters vital to the Allocation Planning pipeline.

* **Path:** `/AllocationPlanning/{folder_name}`
* **Default Controller:** `AllocationPlanning/{folder_name}Controller`

---

## 2. User Interface Components

"""
    
    # Render details for each file parsed (Index.cshtml, Detail.cshtml, etc.)
    for meta in metadata_list:
        view_file = meta["file"]
        markdown_content += f"### View Template: `{view_file}`\n\n"
        
        # Optional image placeholders for interactive modal flows (only on main Index)
        if view_file.lower() == "index.cshtml":
            markdown_content += f"![Add New Form Modal / View]({seq}_{folder_name}_Add.png)\n\n"
            markdown_content += f"![Edit / Detailed Record Modal]({seq}_{folder_name}_Detail.png)\n\n"
        
        # Grid section
        if meta["headers"]:
            markdown_content += f"#### Data Grid Listing (`#{meta['table_id']}`)\n"
            markdown_content += "Displays real-time records synced from database services. The grid supports sorting, server-side pagination, and global search.\n\n"
            markdown_content += "| Column Name | Description |\n| :--- | :--- |\n"
            for col in meta["headers"]:
                desc = "Dynamic database field value."
                if col == "STATUS": desc = "Indicator showing record status (Active/Inactive)."
                elif "Code" in col: desc = "Unique alphanumeric identifier code."
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
        
    # Append instructions section
    markdown_content += """## 3. Dynamic UI Behavior
* **Real-time Filters:** Table redraws automatically with a 500ms debounce delay after users type inside column filter fields.
* **Server-side Pagination:** Displays 10 records per page by default with dynamic loading overlay indicators.
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"[OK] Generated Specification Draft: input/{filename}")

def analyze_all_views():
    print("====================================================")
    print("  HMS TOM - ALLOCATION PLANNING CODEBASE ANALYZER")
    print("====================================================")
    print(f"Scanning source views in: {VIEWS_SRC_DIR}\n")
    
    for idx, folder in enumerate(VIEW_ORDER):
        seq = f"{idx+1:02d}"
        folder_path = os.path.join(VIEWS_SRC_DIR, folder)
        
        if not os.path.exists(folder_path):
            print(f"[WARN] Folder not found: {folder_path}")
            continue
            
        # Find all .cshtml files in the directory
        cshtml_files = glob.glob(os.path.join(folder_path, "*.cshtml"))
        cshtml_files.sort() # Ensure Index is usually first
        
        metadata_list = []
        for filepath in cshtml_files:
            file_name = os.path.basename(filepath)
            try:
                meta = parse_cshtml_view(filepath, folder)
                meta["file"] = file_name
                metadata_list.append(meta)
            except Exception as e:
                print(f"[ERROR] Error parsing {file_name} in {folder}: {str(e)}")
                
        generate_spec_markdown(folder, seq, metadata_list)
        
    print("\n[SUCCESS] Analysis and draft generation complete! All Markdown files are saved in the input folder.")


if __name__ == "__main__":
    analyze_all_views()
