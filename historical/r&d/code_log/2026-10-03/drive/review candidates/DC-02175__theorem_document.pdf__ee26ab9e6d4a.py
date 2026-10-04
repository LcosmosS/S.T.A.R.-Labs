# Extracting the full text of the relevant sections identified earlier
# This will help in summarizing the hypotheses, methods, and findings in detail
# Function to extract full text of relevant sections
def extract_full_sections(text, section_titles):
full_sections = {}
for title in section_titles:
start = text.find(title)
end = text.find('\n', start + len(title))if start != -1 and end != -1:
full_sections[title] = text[start:end].strip()
return full_sections
# Extracting full text for the identified relevant sections
full_relevant_sections = extract_full_sections(pdf_text, relevant_sections)
# Displaying the extracted sections for review
