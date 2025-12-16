import os
import shutil
from pathlib import Path
from typing import Dict, List, Callable, Optional, Tuple
from core.constants import EXTENSION_MAP

# Modes
MODE_ROOT = "root"
MODE_FLATTEN = "flatten"
MODE_RECURSIVE = "recursive"

# Safety: Ignored Folders
IGNORED_FOLDERS = {
    '.git', '.idea', '.vscode', '__pycache__', 'node_modules', 
    'venv', 'env', 'bin', 'obj', 'Program Files', 'Windows', 'SteamLibrary'
}

def get_unique_filename(destination_folder: str, filename: str) -> str:
    """
    Returns a unique filename if the file already exists in the destination.
    Example: 'image.jpg' -> 'image_copy_1.jpg'
    """
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(destination_folder, new_filename)):
        new_filename = f"{name}_copy_{counter}{ext}"
        counter += 1
        
    return new_filename

def _organize_single_directory(directory_path: str, target_root_path: str, operation_log: List[Dict], progress_callback=None, current_count=0, total_files=0) -> int:
    """
    Helper function to organize files in a single directory.
    """
    if not os.path.exists(directory_path):
        return current_count

    # Check if this directory name is in IGNORED_FOLDERS (Double check, though os.walk should prevent entry)
    if os.path.basename(directory_path) in IGNORED_FOLDERS:
        return current_count

    moves = []
    
    try:
        for entry in os.scandir(directory_path):
            if entry.is_file():
                ext = os.path.splitext(entry.name)[1].lower()
                category = EXTENSION_MAP.get(ext, 'Others')
                moves.append((entry.path, category, entry.name))
    except PermissionError:
        return current_count # Skip folders we can't access

    for file_path, category, filename in moves:
        target_dir = os.path.join(target_root_path, category)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        if os.path.dirname(file_path) == target_dir:
            if progress_callback:
                progress_callback(current_count, total_files, filename)
            current_count += 1
            continue
            
        try:
            unique_name = get_unique_filename(target_dir, filename)
            destination_path = os.path.join(target_dir, unique_name)
            
            shutil.move(file_path, destination_path)
            
            operation_log.append({
                'original_path': file_path,
                'new_path': destination_path
            })
            
            if progress_callback:
                progress_callback(current_count, total_files, filename)
                
        except Exception as e:
            print(f"Error moving {file_path}: {e}")
            
        current_count += 1
        
    return current_count

def count_files(directory_path: str, recursive: bool = False) -> int:
    count = 0
    if recursive:
        for root, dirs, files in os.walk(directory_path):
            # Safety: Modify dirs in-place to skip ignored folders
            dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
            count += len(files)
    else:
        try:
            count = len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name))])
        except Exception:
            count = 0
    return count

def organize_files(source_dir: str, mode: str = MODE_ROOT, progress_callback: Optional[Callable[[int, int, str], None]] = None) -> List[Dict]:
    """
    Organizes files based on the selected mode, skipping ignored folders.
    """
    operation_log = []
    
    is_recursive = (mode == MODE_FLATTEN or mode == MODE_RECURSIVE)
    total_files = count_files(source_dir, recursive=is_recursive)
    processed_count = 0
    
    if mode == MODE_ROOT:
        processed_count = _organize_single_directory(source_dir, source_dir, operation_log, progress_callback, processed_count, total_files)
        
    elif mode == MODE_FLATTEN:
        for root, dirs, files in os.walk(source_dir):
            # Safety: Skip ignored folders
            dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
            processed_count = _organize_single_directory(root, source_dir, operation_log, progress_callback, processed_count, total_files)

    elif mode == MODE_RECURSIVE:
        for root, dirs, files in os.walk(source_dir):
            # Safety: Skip ignored folders
            dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
            processed_count = _organize_single_directory(root, root, operation_log, progress_callback, processed_count, total_files)

    if progress_callback:
        progress_callback(total_files, total_files, "Completed")
        
    return operation_log

def undo_last_operation(operation_log: List[Dict], progress_callback: Optional[Callable[[int, int, str], None]] = None):
    """
    Reverses the operations in the log with progress updates.
    """
    total_ops = len(operation_log)
    for i, operation in enumerate(reversed(operation_log)):
        try:
            if os.path.exists(operation['new_path']):
                target_dir = os.path.dirname(operation['original_path'])
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                    
                shutil.move(operation['new_path'], operation['original_path'])
                
                # Clean up: Remove the directory we just moved FROM if it is empty
                source_dir = os.path.dirname(operation['new_path'])
                try:
                    # os.rmdir only removes the directory if it is empty.
                    # We accept the OSError if it's not empty.
                    os.rmdir(source_dir)
                except OSError:
                    pass
                
            if progress_callback:
                progress_callback(i + 1, total_ops, f"Restoring {os.path.basename(operation['original_path'])}")
                
        except Exception as e:
            print(f"Undo error: {e}")
            
    if progress_callback:
        progress_callback(total_ops, total_ops, "Undo Completed")
