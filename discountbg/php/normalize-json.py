import json
import os

lines_in_one_folder = 500

def find_json_files(folder_path):
    try:
        # Get a list of all files in the specified folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        # Filter only JSON files
        json_files = [f for f in files if f.endswith('.json')]
        
        return json_files
    except Exception as e:
        print(f"Error: Unable to find JSON files in '{folder_path}' - {e}")

# Replace 'your_folder_path' with the actual path to your folder containing JSON files
folder_path = '/home/kire/learning/python/discountbg/discountbg/data/'
json_files_array = find_json_files(folder_path)

def read_and_save_two_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Ensure that the data is a list (assuming your JSON contains an array)
            if isinstance(data, list):
                result = []
                for i in range(0, len(data), lines_in_one_folder):
                    lines = data[i:i+lines_in_one_folder]
                    result.append(lines)
                return result
            else:
                print(f"Error: JSON data in '{file_path}' is not a list.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON from file '{file_path}'. Check if the file contains valid JSON.")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

def export_to_json(output_file_path, data):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, indent=2, ensure_ascii=False)
        print(f"Data exported to '{output_file_path}' successfully.")
    except Exception as e:
        print(f"Error: Unable to export data to '{output_file_path}' - {e}")

# Replace 'your_file.json' with the actual path to your JSON file

def remove_all_files(folder_path):
    try:
        # Get a list of all files in the specified folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        # Remove each file in the folder
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)
            print(f"Removed file: {file_path}")

        print(f"All files in '{folder_path}' have been removed.")
    except Exception as e:
        print(f"Error: Unable to remove files in '{folder_path}' - {e}")


output_directory = '/home/kire/Documents/Discount-bg/data/'
if json_files_array:
    remove_all_files(output_directory)
    for file in json_files_array:
        file_path = '/home/kire/learning/python/discountbg/discountbg/data/' + file
        
        data_groups = read_and_save_two_lines(file_path)

        # Define a base name for the output files
        output_base_name = file.replace('.json', '')
        
        for i, group in enumerate(data_groups):

            # Replace 'output_file_1.json', 'output_file_2.json', etc., with desired output file names
            output_file_path = f'{output_directory}{output_base_name}_{i + 1}.json'
            export_to_json(output_file_path, group)