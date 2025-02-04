import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QMessageBox, QFormLayout, QLineEdit, QInputDialog
)
from PyQt5.QtGui import QFont, QClipboard
from PyQt5.QtCore import Qt
from cryptography.fernet import Fernet
import hashlib

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
    entered_password, ok = QInputDialog.getText(None, "Master Password", "Enter master password:", QLineEdit.Password)
    if not ok or entered_password != MASTER_PASSWORD:
        QMessageBox.critical(None, "Error", "Incorrect master password!")
        return False
    return True

# Main Application
class PasswordManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setGeometry(300, 300, 500, 400)
        self.passwords = load_passwords('passwords.json')
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 15px 30px;
                font-size: 16px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                font-size: 14px;
                background-color: #3B4252;
                color: #D8DEE9;
            }
            QLabel {
                font-size: 16px;
                color: #D8DEE9;
            }
            QMessageBox {
                background-color: #2E3440;
                color: #D8DEE9;
            }
        """)

        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Password Manager")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Buttons for each function
        buttons = [
            ("Add a new password", self.add_password),
            ("Retrieve a password (Show hash only)", self.retrieve_password),
            ("Hash Decryption (Enter hash + master password)", self.hash_decryption),
            ("Change an existing password", self.change_password),
            ("Show all stored websites", self.show_all_websites),
            ("Delete a website's password", self.delete_password),
            ("Exit", self.close)
        ]

        for text, callback in buttons:
            button = QPushButton(text)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    padding: 15px 30px;
                    font-size: 16px;
                    margin: 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            button.clicked.connect(callback)
            layout.addWidget(button)

        self.setLayout(layout)

    def add_password(self):
        """Add a new password entry."""
        if not verify_master_password():
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Add Password")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2E3440;
                color: #D8DEE9;
            }
            QLabel {
                font-size: 14px;
                color: #D8DEE9;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                font-size: 14px;
                background-color: #3B4252;
                color: #D8DEE9;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout = QFormLayout()

        website_input = QLineEdit()
        website_input.setPlaceholderText("Enter website or app name")
        username_input = QLineEdit()
        username_input.setPlaceholderText("Enter username")
        password_input = QLineEdit()
        password_input.setPlaceholderText("Enter password")
        password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Website:", website_input)
        layout.addRow("Username:", username_input)
        layout.addRow("Password:", password_input)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)

        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            website = website_input.text()
            username = username_input.text()
            password = password_input.text()

            if website and username and password:
                encrypted_password = encrypt_password(password)
                password_hash = hash_password(encrypted_password)

                self.passwords[website] = {
                    'username': username,
                    'password_hash': password_hash,
                    'encrypted_password': encrypted_password
                }

                save_passwords(self.passwords, 'passwords.json')
                QMessageBox.information(self, "Success", f"Password added for {website}.")

    def retrieve_password(self):
        """Retrieve a password hash for a website."""
        if not verify_master_password():
            return

        website, ok = QInputDialog.getText(self, "Website", "Enter website or app name:")
        if not ok or not website:
            return

        if website in self.passwords:
            username = self.passwords[website]['username']
            password_hash = self.passwords[website]['password_hash']

            # Create a custom message box with a "Copy Hash" button
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Password Hash")
            msg_box.setText(f"Username: {username}\nHashed Password: {password_hash}")
            msg_box.setIcon(QMessageBox.Information)

            # Add a "Copy Hash" button
            copy_button = msg_box.addButton("Copy Hash", QMessageBox.ActionRole)
            copy_button.clicked.connect(lambda: self.copy_to_clipboard(password_hash))

            # Add an "OK" button
            msg_box.addButton(QMessageBox.Ok)

            msg_box.exec_()
        else:
            QMessageBox.warning(self, "Error", "No password found for this website.")

    def copy_to_clipboard(self, text):
        """Copy text to the clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "Copied", "Hash copied to clipboard!")

    def hash_decryption(self):
        """Decrypt a password using its hash."""
        if not verify_master_password():
            return

        hash_value, ok = QInputDialog.getText(self, "Hash", "Enter hash of the password:")
        if not ok or not hash_value:
            return

        for website, data in self.passwords.items():
            if data['password_hash'] == hash_value:
                decrypted_password = decrypt_password(data['encrypted_password'])
                QMessageBox.information(self, "Decrypted Password", f"Decrypted Password for {website}: {decrypted_password}")
                return

        QMessageBox.warning(self, "Error", "Hash not found in stored passwords.")

    def change_password(self):
        """Change an existing password."""
        if not verify_master_password():
            return

        website, ok = QInputDialog.getText(self, "Website", "Enter website or app name:")
        if not ok or not website:
            return

        if website in self.passwords:
            new_password, ok = QInputDialog.getText(self, "New Password", "Enter new password:", QLineEdit.Password)
            if not ok or not new_password:
                return

            encrypted_password = encrypt_password(new_password)
            password_hash = hash_password(encrypted_password)

            self.passwords[website]['encrypted_password'] = encrypted_password
            self.passwords[website]['password_hash'] = password_hash

            save_passwords(self.passwords, 'passwords.json')
            QMessageBox.information(self, "Success", f"Password updated for {website}.")
        else:
            QMessageBox.warning(self, "Error", "No password found for this website.")

    def show_all_websites(self):
        """Show all stored websites."""
        if not verify_master_password():
            return

        websites = "\n".join(self.passwords.keys())
        QMessageBox.information(self, "Stored Websites", f"Stored Websites:\n{websites}")

    def delete_password(self):
        """Delete a website's password."""
        if not verify_master_password():
            return

        website, ok = QInputDialog.getText(self, "Website", "Enter website or app name to delete:")
        if not ok or not website:
            return

        if website in self.passwords:
            del self.passwords[website]
            save_passwords(self.passwords, 'passwords.json')
            QMessageBox.information(self, "Success", f"Password for {website} deleted.")
        else:
            QMessageBox.warning(self, "Error", "No password found for this website.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordManagerApp()
    window.show()
    sys.exit(app.exec_())