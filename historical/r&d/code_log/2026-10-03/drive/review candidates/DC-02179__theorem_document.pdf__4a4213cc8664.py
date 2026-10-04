# Now that I have extracted the text from all supporting documents, I will anal
# Analyzing the extracted texts for key themes and findings
import re
from collections import Counter
# Function to extract key themes and findings from the text
def extract_themes(text):
# Clean and split the text into words
words = re.findall(r'\w+', text.lower())
# Count the frequency of each word
word_counts = Counter(words)
# Extract the most common words as potential themes
common_themes = word_counts.most_common(20)
return common_themes
# Analyzing each document for themes
themes_analysis = {}
for doc, text in extracted_texts_all.items():
themes_analysis[doc] = extract_themes(text)
# Displaying the themes analysis for each document
