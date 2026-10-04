# Path to the file containing log_mass values, one per line.
# Adjust this path based on your operating system and file location.
file_path = "/mnt/c/temp/filtered_log_mass.txt"  # For WSL
# file_path = "C:\\temp\\filtered_log_mass.txt"  # For Windows


try:
    with open(file_path, "r") as f:
        # Read all lines and strip whitespace
        values = [line.strip() for line in f.readlines()]
    
    # Join the values with commas, no line breaks
    joined_values = ",".join(values)
    
    # Format the string as a single line
    formatted = f"log_mass=[{joined_values}]"
    
    # Print the formatted string
    print(formatted)
