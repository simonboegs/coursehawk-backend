import docx
import os
os.getcwd()
doc = docx.Document('ucr_catalog_removed.docx')
print(doc.paragraphs[0].runs[0].bold)
