theoretical_content = {}
for paper in key_papers:
theoretical_content[paper] = extract_pdf_content(paper)
print("Processed: " + paper)
