import os

def save_filenames_to_file(folder_path, exacutable, output_file):
    """Saves all filenames in the specified folder to a text file."""
    try:
        # Get a list of all filenames in the folder
        filenames = os.listdir(folder_path)
        
        # Filter out directories, keep only files
        filenames = [f for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
        
        # Write each filename to a new line in the output file
        with open(output_file, 'w') as file:
            for filename in filenames:
                file.write('python ' + exacutable + ' ' + filename + '\n')
        
        print(f"Successfully saved {len(filenames)} filenames to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage Example
folder_path = 'SCQubit_YAML/test'  # Replace with the path to your folder
output_file = 'task.lst'         # Output file name
exacutable = 'Importable_SCqubits_Cos2phi.py'
save_filenames_to_file(folder_path, exacutable, output_file)