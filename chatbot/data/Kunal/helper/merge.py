import json
import os
from collections import defaultdict

def merge_dicts(a, b):
    for key, value in b.items():
        if key in a:
            if isinstance(a[key], dict) and isinstance(value, dict):
                merge_dicts(a[key], value)
            elif isinstance(a[key], list) and isinstance(value, list):
                a[key].extend(value)
            else:
                a[key] = value
        else:
            a[key] = value

def merge_json_files(file_paths, output_path):
    merged_data = {}

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            merge_dicts(merged_data, data)

    with open(output_path, 'w') as output_file:
        json.dump(merged_data, output_file, indent=4)

if __name__ == "__main__":
    file_paths = [
        'C:\\Users\\kunal\\Dev\\Chatbot\\data\\Kunal\\section_files\\faq.json',
        'C:\\Users\\kunal\\Dev\\Chatbot\\data\\Kunal\\section_files\\media.json',
        'C:\\Users\\kunal\\Dev\\Chatbot\\data\\Kunal\\section_files\\quick_links.json',
        'C:\\Users\\kunal\\Dev\\Chatbot\\data\\Kunal\\section_files\\tendor.json'
    ]
    output_path = 'C:\\Users\\kunal\\Dev\\Chatbot\\data\\Kunal\\merged_output.json'
    
    merge_json_files(file_paths, output_path)
    print(f"Merged JSON files into {output_path}")