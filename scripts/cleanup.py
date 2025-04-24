import os
import shutil
from pathlib import Path

def cleanup_codebase():
    """Remove unnecessary files from the codebase."""
    base_dir = Path('.')
    
    # Counter for removed items
    removed_count = {
        'pycache_dirs': 0,
        'pyc_files': 0,
        'vscode_counter': 0
    }
    
    # Remove __pycache__ directories and .pyc files
    for root, dirs, files in os.walk(base_dir):
        # Skip the virtual environment directory
        if 'fresh_venv' in root:
            continue
            
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                removed_count['pycache_dirs'] += 1
                print(f"Removed: {pycache_path}")
            except Exception as e:
                print(f"Error removing {pycache_path}: {e}")
        
        # Remove .pyc files (in case they exist outside __pycache__)
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    removed_count['pyc_files'] += 1
                    print(f"Removed: {pyc_path}")
                except Exception as e:
                    print(f"Error removing {pyc_path}: {e}")
    
    # Remove .VSCodeCounter directory if it exists
    vscode_counter_dir = base_dir / '.VSCodeCounter'
    if vscode_counter_dir.exists():
        try:
            shutil.rmtree(vscode_counter_dir)
            removed_count['vscode_counter'] += 1
            print(f"Removed: {vscode_counter_dir}")
        except Exception as e:
            print(f"Error removing {vscode_counter_dir}: {e}")
    
    # Summary
    print("\nCleanup Summary:")
    print(f"- Removed {removed_count['pycache_dirs']} __pycache__ directories")
    print(f"- Removed {removed_count['pyc_files']} .pyc files")
    print(f"- Removed {removed_count['vscode_counter']} .VSCodeCounter directories")
    
    # Additional git commands for .gitignore setup if git is being used
    print("\nSuggested next steps:")
    print("1. To prevent Python cache files from being tracked in your repository, add these lines to your .gitignore file:")
    print("   __pycache__/")
    print("   *.py[cod]")
    print("   *$py.class")
    print("   .VSCodeCounter/")
    
if __name__ == "__main__":
    cleanup_codebase()