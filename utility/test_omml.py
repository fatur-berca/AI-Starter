import sys, os
sys.path.insert(0, r'C:\temp\MD_Utility\MDtoDoc')
os.chdir(r'C:\temp\MD_Utility\MDtoDoc')

# Import only the OMML parts we need
import re, glob, time
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import markdown
from bs4 import BeautifulSoup, NavigableString
from PIL import Image
from lxml import etree as _lxml_etree

# Paste just the OMML section inline
exec(open(r'C:\temp\MD_Utility\MDtoDoc\md_to_docx.py', encoding='utf-8').read())

formula = r'\text{LF}_{\text{trip}} = \sum \left( \frac{\text{QtyBox}_i}{\text{MaxQty}(\text{VehicleType}, \text{Mode}, \text{BrandCategory}_i)} \right) \times 100\%'
para = latex_to_omml_para(formula)
xml  = _lxml_etree.tostring(para, pretty_print=True).decode('utf-8')
print('OK - OMML length:', len(xml))
print(xml[:400])