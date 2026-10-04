# Function to extract text from multiple PDF documents
import fitz # PyMuPDF
extracted_texts = {}
for doc in additional_documents:
pdf_document = fitz.open(doc)
text = ''
for page in range(len(pdf_document)):
text += pdf_document[page].get_text()
extracted_texts[doc] = text
pdf_document.close()
# Displaying the titles of the documents and the first 500 characters of their 
