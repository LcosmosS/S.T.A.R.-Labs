# I will attempt to extract and analyze the content of all relevant documents t
import fitz # PyMuPDF for PDF handling
import os
# Function to extract text from PDF files
def extract_text_from_pdfs(pdf_files):
pdf_texts = {}
for pdf in pdf_files:
with fitz.open(pdf) as doc:
text = ""
for page in doc:
text += page.get_text() + '\n'pdf_texts[pdf] = text
return pdf_texts
# List of PDF files to analyze
pdf_files = [
'5 Fold Validation.pdf',
