import os

standard = [
    "Dockerfile",
    "src",
    "description.txt",
    "name.txt",
    "example_input.bin",
    "example_output.bin",
    "config.json",
]

def test_folder_structure(path: str):
    for folder in standard:
        print(f"Checking {folder}")
        folder_path = os.path.join(path, folder)
        assert os.path.exists(folder_path), f"Missing {folder_path}"
        if os.path.isdir(folder_path):
            assert os.listdir(folder_path), f"Empty {folder_path}"
    print("Folder structure is correct.")
    return True
