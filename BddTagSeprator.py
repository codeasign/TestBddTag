import subprocess
import os
import re

def list_cs_files_in_commit(commit_hash):
    try:
        result = subprocess.run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            file_list = result.stdout.splitlines()
            cs_files = [file.strip() for file in file_list if file.endswith('.cs')]
            return cs_files
        else:
            print("Error executing Git command:")
            print(result.stderr)
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def search_variable_in_cs_files(cs_files, variable_name):
    found_files = {}
    for cs_file in cs_files:
        try:
            with open(cs_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line_number, line in enumerate(lines, start=1):
                    if re.search(rf'\b{variable_name}\b', line):
                        if cs_file not in found_files:
                            found_files[cs_file] = []
                        found_files[cs_file].append((line_number, line.strip()))
        except Exception as e:
            print(f"Error reading file {cs_file}: {str(e)}")
    
    return found_files

if __name__ == "__main__":
    commit_hash = input("Enter the commit hash: ")
    variable_name = "BddFeatureMapper"  # Change this to the variable name you want to search for

    cs_files = list_cs_files_in_commit(commit_hash)

    if cs_files is not None:
        if cs_files:
            print(f"Searching for '{variable_name}' in .cs files of commit {commit_hash}:")
            found_files = search_variable_in_cs_files(cs_files, variable_name)
            if found_files:
                for file, occurrences in found_files.items():
                    print(f"In file: {file}")
                    for line_number, line_content in occurrences:
                        print(f"  Line {line_number}: {line_content}")
            else:
                print(f"No occurrences of '{variable_name}' found in .cs files.")
        else:
            print(f"No .cs files found in commit {commit_hash}.")
