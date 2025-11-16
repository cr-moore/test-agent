

def read_test_file(file_path):
    """Read and parse test file containing website URL and test instructions."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    website = lines[0].split('-')[1].strip()
    instructions = ''.join(lines[3:]).strip()


    return {
        'website': website,
        'instructions': instructions
    }