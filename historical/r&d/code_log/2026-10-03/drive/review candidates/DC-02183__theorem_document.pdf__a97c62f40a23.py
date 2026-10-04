# Function to extract text from PDF files
def extract_text_from_pdfs(pdf_files):
text_data = {}
for pdf in pdf_files:
doc = fitz.open(pdf)
text = ""
for page in doc:
text += page.get_text() + '\n'
text_data[pdf] = text
doc.close()
return text_data
# Extracting text from all PDF files
pdf_texts = extract_text_from_pdfs(pdf_files)
# Displaying the first 500 characters of each document to get an overview
overview = {pdf: text[:500] for pdf, text in pdf_texts.items()}
