# custom_password_manager
 Free Custom Python Password Manager
# Step 1: Install Python
Download Python:

Go to the official Python website.

Download the latest version of Python for Windows (make sure to check the box "Add Python to PATH" during installation).

Verify Installation:

Open Command Prompt (CMD) and type:

python --version

If the Python version is displayed (e.g., Python 3.11.5), the installation is successful.


# Step 2: Install Required Python Packages
The script uses the following Python packages:

PyQt5 (for the graphical interface)

cryptography (for encryption)

Install the Packages:

In Command Prompt, run the following commands:
pip install PyQt5 cryptography

Verify Installation:
Check if the packages are installed:
pip show PyQt5 cryptography
If information about the packages is displayed, the installation is successful.

# Step 3: Download the Script

# Step 4: Run the Script
Open Command Prompt:

Open CMD and navigate to the directory where the script is located:
cd C:\PasswordManager
Run the Script:

In CMD, type:
python password_manager.py
If everything is set up correctly, the "Password Manager" application will launch.
If you follow these steps, you will successfully install everything needed and run the script.

⚠️ Important Warning ⚠️
Do not close the Command Prompt (CMD) window while the application is running!
The Python script runs in the background, and closing the CMD window will terminate the application. Keep the CMD window open for as long as you are using the Password Manager.
# ERRORS
How to Fix the Error (ValueError: Fernet key must be 32 url-safe base64-encoded bytes.)
1. Generate a Valid Fernet Key
The cryptography library provides a built-in method to generate a valid Fernet key. Replace the ENCRYPTION_KEY in your script with a newly generated key.

Run the following Python code to generate a valid key:
(python/cmd)

from cryptography.fernet import Fernet

# Generate a new Fernet key
key = Fernet.generate_key()
print(key.decode())  # Decode to a string for use in your script

This will output a valid 32-byte URL-safe base64-encoded key, such as:

tenKfqCgtyGIIkINBq51zOuZx38F_0UK2VZQF9umOdw=

2. Update the ENCRYPTION_KEY in Your Script
Replace the existing ENCRYPTION_KEY in your script with the newly generated key. For example:
# Replace this with your generated key
ENCRYPTION_KEY = "tenKfqCgtyGIIkINBq51zOuZx38F_0UK2VZQF9umOdw="

# Steps to Fix and Run the Script
Generate a New Key:

Run the Python code provided above to generate a valid key.

Replace the Key:

Open your script (password_manager_gui.py) and replace the ENCRYPTION_KEY with the newly generated key.

Run the Script Again:

Navigate to the script's directory in Command Prompt:

cd D:\custom_password_manager-main

Run the script:

python password_manager_gui.py

# After updating the key, the script should run without errors.
