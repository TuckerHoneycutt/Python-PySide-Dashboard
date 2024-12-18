import subprocess
import os
import sys
from datetime import datetime

def build_app():
    # Configuration
    build_command = [
        'pyinstaller',
        '--onefile',
        '--noconsole',
        '--name', 'ASCEND',
        '--icon=/Users/tuckerhoneycutt/projects/python/Work/n1uTw9NYigfpF0A2dRwLnplEskWfgjmT.icns',
        '--exclude', 'PyQt5',
        'MainGui.py'
    ]

    # Create builds directory if it doesn't exist
    if not os.path.exists('builds'):
        os.makedirs('builds')

    # Get timestamp for build
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    try:
        # Run PyInstaller
        print("Starting build process...")
        subprocess.run(build_command, check=True)

        # Move the built executable to builds directory with timestamp
        dist_path = os.path.join('dist', 'ASCEND')
        if sys.platform == 'darwin':  # For macOS
            new_name = f'ASCEND_{timestamp}'
        else:  # For Windows
            new_name = f'ASCEND_{timestamp}.exe'

        new_path = os.path.join('builds', new_name)

        os.rename(dist_path, new_path)
        print(f"Build completed successfully! Executable saved as: {new_path}")

        # Clean up PyInstaller artifacts
        for dir_name in ['build', 'dist']:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(dir_name)

        if os.path.exists('ASCEND.spec'):
            os.remove('ASCEND.spec')

        print("Cleanup completed.")

    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    build_app()
