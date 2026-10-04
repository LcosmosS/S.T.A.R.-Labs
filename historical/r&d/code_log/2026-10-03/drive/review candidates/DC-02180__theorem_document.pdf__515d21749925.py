# Now that I have the themes analysis for each document, I will summarize the k
# This will help in understanding how each document contributes to the overarch
# Function to summarize findings based on themes
def summarize_findings(themes_analysis):
summaries = {}
for doc, themes in themes_analysis.items():
# Extracting the most relevant themes for summary
