import os
import json
import hashlib
from getpass import getpass
from cryptography.fernet import Fernet

# Encryption key (Replace with your own key)
ENCRYPTION_KEY = "KEY"

# Master password for authentication
MASTER_PASSWORD = "MASTER_PASSWORD"

# Initialize Fernet cipher
def init_cipher():
    return Fernet(ENCRYPTION_KEY.encode())

cipher = init_cipher()

# Hash a password using SHA256 (for displaying hashes)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Encrypt a password
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

# Decrypt a password
def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

# Load existing passwords from file
def load_passwords(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

# Save passwords to file
def save_passwords(passwords, filename):
    with open(filename, 'w') as file:
        json.dump(passwords, file, indent=4)

# Verify Master Password
def verify_master_password():
    entered_password = getpass("Enter master password: ")
    if entered_password != MASTER_PASSWORD:
        print("Incorrect master password!")
        return False
    return True

# Add a new password
def add_password(passwords):
    if not verify_master_password():
        return

    website = input("Enter the website or app name: ")
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    encrypted_password = encrypt_password(password)
    password_hash = hash_password(encrypted_password)

    passwords[website] = {
        'username': username,
        'password_hash': password_hash,
        'encrypted_password': encrypted_password
    }

    print(f"Password added for {website}.")

# Retrieve and show password hash (not the original password)
def retrieve_password(passwords):
    if not verify_master_password():
        return

    website = input("Enter the website or app name: ")

    if website in passwords:
        # Show just the username and the hashed password
        username = passwords[website]['username']
        password_hash = passwords[website]['password_hash']
        print(f"Username: {username}, Hashed Password: {password_hash}")
    else:
        print(f"No password found for {website}.")

# Hash Decryption using Master Password
def hash_decryption(passwords):
    if not verify_master_password():
        return

    password_hash_input = input("Enter the hash of the password: ")
    
    # Search for a password with the matching hash
    for website, data in passwords.items():
        if data['password_hash'] == password_hash_input:
            # Decrypt the password
            encrypted_password = data['encrypted_password']
            decrypted_password = decrypt_password(encrypted_password)
            print(f"Decrypted Password for {website}: {decrypted_password}")
            return

    print("Hash not found in stored passwords.")

# Change an existing password
def change_password(passwords):
    if not verify_master_password():
        return

    website = input("Enter the website or app name: ")
    
    if website in passwords:
        new_password = getpass("Enter your new password: ")
        encrypted_password = encrypt_password(new_password)
        password_hash = hash_password(encrypted_password)

        passwords[website]['encrypted_password'] = encrypted_password
        passwords[website]['password_hash'] = password_hash

        print(f"Password updated for {website}.")
    else:
        print(f"No password found for {website}.")

# Show all stored websites
def show_all_websites(passwords):
    if not verify_master_password():
        return

    if passwords:
        print("\nStored Websites:")
        for website in passwords.keys():
            print(f"- {website}")
    else:
        print("No passwords stored yet.")

# Delete a website's password
def delete_password(passwords):
    if not verify_master_password():
        return

    website = input("Enter the website or app name to delete: ")
    
    if website in passwords:
        del passwords[website]
        print(f"Password for {website} deleted.")
    else:
        print(f"No password found for {website}.")
    
def main():
    filename = 'passwords.json'
    passwords = load_passwords(filename)

    while True:
        print("\nPassword Manager Menu:")
        print("1. Add a new password")
        print("2. Retrieve a password (Show hash only)")
        print("4. Hash Decryption (Enter hash + master password)")
        print("5. Change an existing password")
        print("6. Show all stored websites")
        print("7. Delete a website's password")

        choice = input("Enter your choice (1-7) or type 'exit' to quit: ")

        if choice.lower() == 'exit':
            print("Exiting Password Manager. Goodbye!")
            break
        elif choice == '1':
            add_password(passwords)
            save_passwords(passwords, filename)
        elif choice == '2':
            retrieve_password(passwords)
        elif choice == '4':
            hash_decryption(passwords)
        elif choice == '5':
            change_password(passwords)
            save_passwords(passwords, filename)
        elif choice == '6':
            show_all_websites(passwords)
        elif choice == '7':
            delete_password(passwords)
            save_passwords(passwords, filename)
        else:
            print("Invalid choice. Please enter a number from 1 to 7 or type 'exit' to quit.")

if __name__ == "__main__":
    main()
