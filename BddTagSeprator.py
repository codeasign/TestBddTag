import subprocess
import re
import json

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

def find_variable_occurrences(cs_files, variable_name):
    variable_occurrences = []
    for cs_file in cs_files:
        try:
            with open(cs_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line_number, line in enumerate(lines, start=1):
                    if re.search(rf'{variable_name} = "(.*?)"', line):
                        matches = re.findall(rf'{variable_name} = "(.*?)"', line)
                        for match in matches:
                            variable_occurrences.append((cs_file, line_number, match))
        except Exception as e:
            print(f"Error reading file {cs_file}: {str(e)}")
    
    return variable_occurrences

if __name__ == "__main__":
    finalCommand=""
    commit_hash = input("Enter the commit hash: ")
    variable_name = "BddFeatureMapper"  # Change this to the variable name you want to search for

    cs_files = list_cs_files_in_commit(commit_hash)

    if cs_files is not None:
        if cs_files:
            print(f"Searching for '{variable_name}' in .cs files of commit {commit_hash}:")
            variable_occurrences = find_variable_occurrences(cs_files, variable_name)
            if variable_occurrences:
                tags = set()  # To store unique values
                for _, _, tag in variable_occurrences:
                    tags.update(tag.split(','))  # Split by commas and add to the set

                # Convert set to a list to maintain order and remove duplicates
                tags_list = list(tags)

                # Create a JSON structure
                tags_json = {"BddFeatureMapper": tags_list}

                # Print the JSON structure
                print(json.dumps(tags_json, indent=2))

                counter = 0
                categoryTextAppended =""
                for category in tags_list:
                    if counter:0
                    categoryFetch = f"cat == {category} ||"
                    counter = counter+1
                    categoryTextAppended =  categoryTextAppended + categoryFetch
                else:
                    if(counter<len(tags_list)-1):
                        categoryFetch = f"cat == {category} ||"
                        categoryTextAppended =  categoryTextAppended + categoryFetch
                
                command = f"nunit3-console.exe \"D:\codes\mygitrepo\C#Learning\BddtagEnforcerTest\TestSpecFlowProject\\bin\Debug\\net6.0\TestSpecFlowProject.dll\" --where  "
                categoryTextAppended = categoryTextAppended.rstrip(categoryTextAppended[-2])
                finalCommand  = command + "\"" + categoryTextAppended + "\""

            else:
                print(f"No occurrences of '{variable_name}' found in .cs files.")
        else:
            print(f"No .cs files found in commit {commit_hash}.")
        
    result = subprocess.run(finalCommand)
    print(result)
