"""
This file sends a bash command according to the operating system
to start the Streamlit server and create a local hostet webpage.
"""

import os
import platform
import subprocess

# Define paths
venv_path = ".venv"  # Change if your virtual environment has a different name
app_file = "Streamlit_App.py"  # Adjust to your actual filename

# Detect OS and construct activation command
if platform.system() == "Windows":
    activate_cmd = f"streamlit run {app_file}"
else:
    activate_cmd = f"streamlit run {app_file}"

# Run the command in a new shell
subprocess.run(activate_cmd, shell=True)
