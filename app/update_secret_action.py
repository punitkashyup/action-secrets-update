import os
import base64
import nacl.secret
import nacl.utils
import requests
import logging
import sys

def encrypt_secret(secret_value, public_key):
    try:
        box = nacl.secret.SecretBox(public_key, encoder=nacl.encoding.Base64Encoder)
        encrypted = box.encrypt(secret_value.encode())
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        logging.error(f"Encryption failed: {e}")
        sys.exit(1)

def decrypt_secret(encrypted_secret, private_key):
    try:
        box = nacl.secret.SecretBox(private_key, encoder=nacl.encoding.Base64Encoder)
        decrypted = box.decrypt(base64.b64decode(encrypted_secret)).decode()
        return decrypted
    except Exception as e:
        logging.error(f"Decryption failed: {e}")
        sys.exit(1)

def update_github_secret(repository_owner, repository_name, secret_name, new_secret_value, token):
    try:
        url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/actions/secrets/{secret_name}"

        # Get the public key for encryption
        response = requests.get(f"https://api.github.com/repos/{repository_owner}/{repository_name}/actions/secrets/public-key", headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()  # Raise an error for bad responses
        public_key = response.json()['key']
        public_key = base64.b64decode(public_key)

        # Encrypt the new secret value
        encrypted_secret = encrypt_secret(new_secret_value, public_key)

        # Update the secret on GitHub
        response = requests.put(url, json={"encrypted_value": encrypted_secret}, headers={"Authorization": f"Bearer {token}"})
        
        response.raise_for_status()  # Raise an error for bad responses

        if response.status_code == 200:
            logging.info(f"Secret '{secret_name}' updated successfully.")
        else:
            logging.error(f"Failed to update secret '{secret_name}'. Status code: {response.status_code}, Response: {response.text}")
            sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    repository_owner = os.getenv("INPUT_REPOSITORY_OWNER")
    repository_name = os.getenv("INPUT_REPOSITORY_NAME")
    secret_name = os.getenv("INPUT_SECRET_NAME")
    new_secret_value = os.getenv("INPUT_NEW_SECRET_VALUE")
    github_token = os.getenv("INPUT_GITHUB_TOKEN")

    if not all([repository_owner, repository_name, secret_name, new_secret_value, github_token]):
        logging.error("Missing required environment variables.")
        sys.exit(1)

    update_github_secret(repository_owner, repository_name, secret_name, new_secret_value, github_token)
