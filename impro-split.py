import os
import shutil

def remove_directory(dir_path):
    """Remove the directory and all its contents."""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f"Removed directory: {dir_path}")

def copy_directory(src, dst):
    """Copy files from source directory to destination directory."""
    shutil.copytree(src, dst)
    print(f"Copied files from {src} to {dst}")

def split_file(file_path, chunk_size_mb=10):
    """Split the file into chunks of specified size (in MB)."""
    chunk_size = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    file_chunks = []
    
    # Create a directory for the chunked files
    base_name = os.path.basename(file_path).replace('.onnx', '')
    chunk_dir = os.path.join(os.path.dirname(file_path), f"{base_name}-onnx")
    os.makedirs(chunk_dir, exist_ok=True)

    with open(file_path, 'rb') as f:
        chunk_num = 0
        while True:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                break
            chunk_filename = os.path.join(chunk_dir, f"{base_name}-chunk{chunk_num}.onnx")
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk_data)
            file_chunks.append(chunk_filename)
            chunk_num += 1

    # Remove the original .onnx file after splitting
    os.remove(file_path)
    print(f"Removed original file: {file_path}")

    return file_chunks

def process_directory(directory):
    """Process all files in the directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith('.onnx'):
                print(f"Splitting file: {full_path}")
                split_file(full_path)
            else:
                print(f"Skipping file (not .onnx): {full_path}")

def main():
    origin_dir = 'origin-impro'
    origin_after_dir = 'origin-github'

    # Step 1: Remove origin-github directory
    remove_directory(origin_after_dir)

    # Step 2: Copy files from origin-impro to origin-github
    copy_directory(origin_dir, origin_after_dir)

    # Step 3: Process files to split .onnx files
    process_directory(origin_after_dir)

if __name__ == '__main__':
    main()
