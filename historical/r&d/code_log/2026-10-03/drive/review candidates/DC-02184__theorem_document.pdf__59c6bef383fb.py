# Now that I have extracted the text from all the PDF documents, I will analyze 
# This will involve processing the text to summarize the main points from each 
from collections import Counter
import re
# Function to analyze the text and extract key themes
def analyze_texts(pdf_texts):
analysis_results = {}
for pdf, text in pdf_texts.items():
# Clean and split the text into words
words = re.findall(r'\w+', text.lower())
# Count the frequency of each word
word_counts = Counter(words)
# Get the most common words
common_words = word_counts.most_common(10)analysis_results[pdf] = common_words
return analysis_results
# Analyzing the extracted texts
analysis_results = analyze_texts(pdf_texts)
# Displaying the analysis results
