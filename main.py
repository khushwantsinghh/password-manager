import json
import os
from cryptography.fernet import Fernet
import argparse
import getpass

KEY_FILE = "key.key"
DATA_FILE = "passwords.json"

# Generate a key for encryption
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

# Load the key
def load_key():
    return open(KEY_FILE, "rb").read()

# Load passwords
def load_passwords():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "rb") as file:
        data = file.read()
        if data == b'':
            return {}
        decrypted = Fernet(load_key()).decrypt(data)
        return json.loads(decrypted.decode())

# Save passwords
def save_passwords(passwords):
    data = json.dumps(passwords).encode()
    encrypted = Fernet(load_key()).encrypt(data)
    with open(DATA_FILE, "wb") as file:
        file.write(encrypted)

# First time setup
def setup():
    if os.path.exists(KEY_FILE):
        print("Already initialized.")
        return
    generate_key()
    print("🔐 Setup complete. You can now add passwords.")

# Add a new password
def add_password(site):
    passwords = load_passwords()
    if site in passwords:
        print(f"🔁 Password for '{site}' already exists.")
        return
    pwd = getpass.getpass(f"Enter password for {site}: ")
    passwords[site] = pwd
    save_passwords(passwords)
    print(f"✅ Password saved for '{site}'.")

# Get password
def get_password(site):
    passwords = load_passwords()
    if site not in passwords:
        print(f"❌ No password found for '{site}'.")
    else:
        print(f"🔐 Password for '{site}': {passwords[site]}")

# List saved sites
def list_sites():
    passwords = load_passwords()
    if not passwords:
        print("📭 No saved passwords.")
        return
    print("📒 Saved sites:")
    for site in passwords:
        print(f" - {site}")

# CLI setup
parser = argparse.ArgumentParser(description="🔐 CLI Password Manager")
parser.add_argument("command", choices=["init", "add", "get", "list"], help="Action to perform")
parser.add_argument("site", nargs="?", help="Site name")

args = parser.parse_args()

# Command Handling
if args.command == "init":
    setup()
elif args.command == "add":
    if not args.site:
        print("⚠️ Please provide site name. Example: python main.py add facebook")
    else:
        add_password(args.site)
elif args.command == "get":
    if not args.site:
        print("⚠️ Please provide site name. Example: python main.py get facebook")
    else:
        get_password(args.site)
elif args.command == "list":
    list_sites()
