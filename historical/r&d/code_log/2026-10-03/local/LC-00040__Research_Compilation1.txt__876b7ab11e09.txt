# Path to the filtered_log_mass.txt file
# Adjust this path according to your setup
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
