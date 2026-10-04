# I will attempt to extract the mathematical content again, ensuring that I han
# Function to extract mathematical content from the text, ensuring proper handl
def extract_mathematical_content_v2(pdf_texts):
math_content = {}
for pdf, text in pdf_texts.items():
# Clean the text to avoid issues with special characters
cleaned_text = re.sub(r'[^\$\w\s\$]', '', text)
# Find all mathematical expressions using regex
equations = re.findall(r'\$\$(.*?)\$\$', cleaned_text, re.DOTALL)
math_content[pdf] = equations
return math_content
# Extracting mathematical content from the PDF texts again
mathematical_content_v2 = extract_mathematical_content_v2(pdf_texts)
# Displaying the extracted mathematical content
