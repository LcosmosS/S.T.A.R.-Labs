# I will extract mathematical content from the documents to perform a detailed 
import re
# Function to extract mathematical content from the text
def extract_mathematical_content(pdf_texts):
math_content = {}
for pdf, text in pdf_texts.items():
# Find all mathematical expressions using regex
equations = re.findall(r'\$\$(.*?)\$\$', text, re.DOTALL)
math_content[pdf] = equations
return math_content
# Extracting mathematical content from the PDF texts
mathematical_content = extract_mathematical_content(pdf_texts)
# Displaying the extracted mathematical content
