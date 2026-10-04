# Import necessary libraries for PDF processing and analysis
import fitz
import pandas as pd
import numpy as np
from collections import defaultdict
def extract_pdf_content(filename):
try:
doc = fitz.open(filename)
