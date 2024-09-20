import os

def modify_env_file(pairs_dict, env_file=".env"):
    """
    Modify the .env file by updating or adding multiple key-value pairs from a dictionary.
    
    :param pairs_dict: Dictionary containing key-value pairs to update in the .env file.
    :param env_file: The path to the .env file (default is '.env').
    """
    # Read the existing content from the .env file
    if os.path.exists(env_file):
        with open(env_file, "r") as file:
            lines = file.readlines()
    else:
        lines = []

    # Track the keys that have been updated
    updated_keys = set()

    # Go through each line and update the keys if found
    new_lines = []
    for line in lines:
        key_in_line = line.split('=')[0].strip()
        if key_in_line in pairs_dict:
            # If key exists in the dictionary, update its value
            new_lines.append(f"{key_in_line}={pairs_dict[key_in_line]}\n")
            updated_keys.add(key_in_line)
        else:
            new_lines.append(line)
    
    # Add any key-value pairs that were not found in the .env file
    for key, value in pairs_dict.items():
        if key not in updated_keys:
            new_lines.append(f"{key}={value}\n")
    
    # Write the modified content back to the .env file
    with open(env_file, "w") as file:
        file.writelines(new_lines)
