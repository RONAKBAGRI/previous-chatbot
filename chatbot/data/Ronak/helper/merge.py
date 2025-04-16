import json
from pathlib import Path

def merge_json_files(input_files, output_file):
    merged_data = {"intents": []}

    # Read and combine data
    for file_path in input_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                if "intents" in data:
                    merged_data["intents"].extend(data["intents"])
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
            continue
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {file_path}")
            continue

    # Remove duplicate intents based on the tag, ensuring unique tags
    unique_intents = {}
    for intent in merged_data["intents"]:
        unique_intents[intent["tag"]] = intent

    # Update merged data with the unique intents
    merged_data["intents"] = list(unique_intents.values())

    # Write the merged data to the output file
    with open(output_file, "w") as f:
        json.dump(merged_data, f, indent=4)

# Updated file paths using relative paths for "section_files" folder
parent_directory = Path(__file__).parent.parent
section_files_dir = parent_directory / "section_files"

input_files = [
    section_files_dir / "accounts.json",
    section_files_dir / "alumni_affairs.json",
    section_files_dir / "academic_affair.json",
    section_files_dir / "procurement_section.json",
    section_files_dir / "cds.json",
    section_files_dir / "cep.json",
    section_files_dir / "counselling.json",
    section_files_dir / "eg_saral.json",
    section_files_dir / "library.json",
    section_files_dir / "medical_centre.json",
    section_files_dir / "research_and_consultancy.json",
    section_files_dir / "security_section.json",
    section_files_dir / "student_affairs.json",
    section_files_dir / "tinkerers_lab.json",
    section_files_dir / "tlu.json",
    section_files_dir / "pg_certification.json",
    section_files_dir / "pmrf.json",
    section_files_dir / "student_sections_2.json",
    section_files_dir / "students_section_1.json",
]

# Output file path in the same parent directory as the "helper" folder
output_file = parent_directory / "merged_output.json"

# Run the merge function
merge_json_files(input_files, output_file)
