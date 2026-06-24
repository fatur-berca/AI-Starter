# Guidelines for Downstream AI Agents: Markdown & Image Formatting for DOCX Compilation

This directory contains a specialized Python utility `md_to_docx.py` that compiles Markdown files and local screenshot images into a beautifully styled, high-fidelity Microsoft Word (`.docx`) document.

If you are an AI assistant tasked with describing screenshots and generating functional specifications, follow these instructions to ensure flawless rendering.

---

## 1. Input Directory Structure

All raw assets must be saved inside the `input/` subdirectory relative to the compilation script:
```
C:\temp\MDtoDoc\
├── md_to_docx.py
├── requirements.txt
├── input/                  <--- Place all source files here
│   ├── 01_login.png
│   ├── 01_login.md
│   ├── 02_dashboard.png
│   └── 02_dashboard.md
└── output/                 <--- Word document will be generated here
    └── Functional_Specification_Document.docx
```

---

## 2. Naming Conventions & Sequential Ordering

* **Strict Alphabetical Ordering:** The script merges all `.md` files inside the `input/` folder **alphabetically**. Always prefix your filenames with a two-digit sequence number:
  * `01_login_flow.md`
  * `02_dashboard_overview.md`
  * `03_user_settings.md`
* **Matching Screenshots:** Keep screenshot files in the same `input/` directory and use the same prefix/description for clarity (e.g., `01_login.png`, `02_dashboard.png`).

---

## 3. How to Reference Images inside Markdown

To make sure the Python script successfully embeds the screenshots into the compiled Word document, use the standard Markdown image format. The text inside `[...]` will automatically serve as the **Figure Caption** centered below the image in the Word document:

```markdown
![Login Screen - UI form with email, password, and single sign-on buttons.](01_login.png)
```

> **CRITICAL:** Do NOT include subdirectory paths inside the image URL. Just specify the raw filename (e.g., `01_login.png`). The compiler is configured to automatically resolve the paths within the `input/` directory.

---

## 4. Markdown Formatting Support & Word Layout Style

The compiler transforms standard Markdown tags into premium corporate-styled Microsoft Word elements:

| Markdown Element | Word Rendering Style |
| :--- | :--- |
| **Headings (`#`, `##`, `###`)** | Deep Navy `#1F4E79`, Trebuchet/Calibri, with precise padding margins to prevent orphaned titles. |
| **Normal Text** | Charcoal Gray `#333333` body text at 11pt, 1.15 line spacing, 6pt space-after. |
| **Bold & Italic** | Native bold and italic formatting supported inside paragraphs, lists, and tables. |
| **Lists (`-`, `1.`)** | Proper Word bullet and numbered indents (up to 2 levels of nesting supported). |
| **Blockquotes (`>`)** | Indented 0.4" left/right, italicized, and colored in subtle charcoal gray. |
| **Tables (`\|` headers `\|`)** | Light Navy `#E6EDF5` header row, zebra striping, soft grey gridlines, and cell margins. |
| **Code blocks (```` ``` ````)** | Courier/Consolas font with light gray `#F2F2F2` background block shading. |

---

## 5. Recommended Prompt for Image-to-Markdown AI

When a user feeds you screenshots of a web page and asks you to generate functional specifications, use this structure to ensure perfect document alignment:

```markdown
# [Feature Name / Path]

Brief description of the screen's purpose, path/URL (e.g. `/dashboard`), and audience.

![[Visual Caption describing the screen layout]]([exact_screenshot_filename])

## 1. Functional Overview
Explain what actions a user can perform on this screen.

## 2. Component/Field Definitions
Use a Markdown table to define input fields, buttons, and display cards:

| Component ID | Element Type | Description / Validation Rules |
| :--- | :--- | :--- |
| Email Input | Input Text | Must be a valid email format. |
| Login Button | Button | Submits credentials; disabled if form is invalid. |

## 3. Dynamic Behavior
* **Hover State:** Highlight buttons on hover.
* **Error Handling:** Display inline red text under the field if inputs are invalid.
```

---

## 6. How to Run the Program (Execution Command)

Ensure all dependencies are installed first:
```bash
pip install -r requirements.txt
```

Run the compiler script:
```bash
python md_to_docx.py
```
The compiled Word file will be saved in `output/Functional_Specification_Document.docx`.
