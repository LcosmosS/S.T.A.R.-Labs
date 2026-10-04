# Now that I have extracted the text from the PDF files, I will analyze the con
# Function to summarize the content of each document
def summarize_document_content(pdf_texts):
summaries = {}
for pdf, text in pdf_texts.items():
# Summarize the content by extracting key sentences or phrases
sentences = text.split('. ')
key_sentences = sentences[:5] # Taking the first 5 sentences as a summ
summaries[pdf] = ' '.join(key_sentences)
return summaries
# Summarizing the content of the PDF texts
document_summaries = summarize_document_content(pdf_texts)
# Displaying the summaries of the documents
