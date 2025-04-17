import json
import os
import argparse
from collections import defaultdict

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None

def save_json_file(data, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Cleaned data saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving JSON file {output_file}: {e}")
        return False

def find_duplicates(data):
    seen_values = {}
    duplicates = []
    
    def search_for_duplicates(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    search_for_duplicates(value, new_path)
                else:
                    if isinstance(value, str) and len(value) > 20:
                        if value in seen_values:
                            duplicates.append({
                                "value": value,
                                "paths": [seen_values[value], new_path]
                            })
                        else:
                            seen_values[value] = new_path
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    search_for_duplicates(item, new_path)
    
    search_for_duplicates(data)
    return duplicates

def merge_contact_details(data):
    contact_details = None
    
    for key, value in data.items():
        if isinstance(value, dict) and "Contact_Details" in key:
            contact_details = value
            break
        elif isinstance(value, dict) and "contact_details" in value.get("content", {}):
            contact_details = value["content"]["contact_details"]
            break
    
    if not contact_details:
        return data
    
    cleaned_data = data.copy()
    if "Contact_Details" not in cleaned_data:
        cleaned_data["Contact_Details"] = contact_details
    
    for key in list(cleaned_data.keys()):
        if key != "Contact_Details" and isinstance(cleaned_data[key], dict):
            if "content" in cleaned_data[key] and "contact_details" in cleaned_data[key]["content"]:
                del cleaned_data[key]["content"]["contact_details"]
    
    return cleaned_data

def consolidate_campus_info(data):
    campuses = {}
    
    for key, value in data.items():
        if "Campus" in key and isinstance(value, dict):
            campus_name = key.split("_")[-1]
            
            if campus_name not in campuses:
                campuses[campus_name] = {}
            
            if "content" in value and "about_us" in value["content"]:
                about = value["content"]["about_us"]
                campuses[campus_name].update({
                    "details": about.get("campus_details", ""),
                    "facilities": about.get("facilities", [])
                })
            
            if campus_name == "Paloura" and "content" in value and "about_us" in value["content"]:
                if "research_facilities" in value["content"]["about_us"]:
                    campuses[campus_name]["research_facilities"] = value["content"]["about_us"]["research_facilities"]
    
    cleaned_data = data.copy()
    if campuses:
        cleaned_data["Campuses"] = campuses
        
        for key in list(cleaned_data.keys()):
            if "Campus" in key and key != "Campuses":
                del cleaned_data[key]
    
    return cleaned_data

def normalize_structure(data):
    normalized = {}
    
    if "IIT_Jammu" in data:
        normalized["Institution"] = {
            "Name": "Indian Institute of Technology Jammu",
            "Recognition": data["IIT_Jammu"].get("Recognition", ""),
            "Funding": data["IIT_Jammu"].get("Funding", ""),
            "Governance": data["IIT_Jammu"].get("Governance", ""),
            "Establishment": data["IIT_Jammu"].get("Establishment", "")
        }
    
    if "Jammu" in data:
        normalized["Location"] = data["Jammu"]
    
    if "IIT_Jammu_Vision_and_Mission" in data:
        vision_content = data["IIT_Jammu_Vision_and_Mission"].get("content", {})
        normalized["Vision_and_Mission"] = {
            "Vision": vision_content.get("vision", ""),
            "Motto": vision_content.get("motto", ""),
            "Culture": vision_content.get("details", {}).get("culture", ""),
            "Goals": vision_content.get("details", {}).get("goals", {})
        }
    
    if "Contact_Details" in data:
        normalized["Contact_Details"] = data["Contact_Details"]
    
    if "Campuses" in data:
        normalized["Campuses"] = data["Campuses"]
    
    return normalized if normalized else data

def clean_data(data):
    cleaned_data = merge_contact_details(data)
    cleaned_data = consolidate_campus_info(cleaned_data)
    cleaned_data = normalize_structure(cleaned_data)
    return cleaned_data

def process_file(input_file, output_file):
    data = load_json_file(input_file)
    if not data:
        return False
    
    print(f"\nProcessing file: {input_file}")
    print(f"Original data has {len(data)} top-level keys")
    
    duplicates = find_duplicates(data)
    if duplicates:
        print(f"Found {len(duplicates)} potential duplicate content blocks")
    
    cleaned_data = clean_data(data)
    
    print(f"Cleaned data has {len(cleaned_data)} top-level keys")
    
    return save_json_file(cleaned_data, output_file)

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    success_count = 0
    failure_count = 0
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            if process_file(input_path, output_path):
                success_count += 1
            else:
                failure_count += 1
    
    print(f"\nProcessed {success_count + failure_count} files")
    print(f"Success: {success_count}, Failure: {failure_count}")

def main():
    parser = argparse.ArgumentParser(description='Clean and structure JSON data files.')
    parser.add_argument('input', help='Input JSON file or directory')
    parser.add_argument('--output', help='Output JSON file or directory (default: adds "_cleaned" to input filename)')
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        output_dir = args.output if args.output else args.input + "_cleaned"
        process_directory(args.input, output_dir)
    else:
        if not args.output:
            base, ext = os.path.splitext(args.input)
            output_file = f"{base}_cleaned{ext}"
        else:
            output_file = args.output
        
        process_file(args.input, output_file)

if __name__ == "__main__":
    main()
