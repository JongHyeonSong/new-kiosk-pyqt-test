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

def sum_chunks_and_restore(original_file, chunk_dir):
    """Sum chunk files back into the original .onnx file and remove the chunk directory."""
    with open(original_file, 'wb') as outfile:
        for chunk_file in sorted(os.listdir(chunk_dir)):
            chunk_path = os.path.join(chunk_dir, chunk_file)
            if os.path.isfile(chunk_path):
                print(f"Appending chunk: {chunk_path} to {original_file}")
                with open(chunk_path, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)

    # Remove the chunk directory after summing
    remove_directory(chunk_dir)

def process_directory(directory):
    """Process all files in the directory."""
    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            if dir_name.endswith('-onnx'):
                print(dir_name)
                print(dir_name)
                print(dir_name)
                chunk_dir = os.path.join(root, dir_name)
                # Determine the corresponding original .onnx file path
                original_file_name = dir_name.replace('-onnx', '.onnx')
                original_file_path = os.path.join(root, original_file_name)

                sum_chunks_and_restore(original_file_path, chunk_dir)

def main():
    origin_after_dir = 'origin-github'
    origin_before_dir = 'src/impro'

    # Step 1: Remove the origin-before directory if it exists
    remove_directory(origin_before_dir)

    # Step 2: Copy files from origin-github to origin-before
    copy_directory(origin_after_dir, origin_before_dir)

    # Step 3: Process the files to sum chunks and restore original .onnx files
    process_directory(origin_before_dir)

if __name__ == '__main__':
    main()
