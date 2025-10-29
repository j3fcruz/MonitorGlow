# core/crypto_utils.py
from cryptography.fernet import Fernet


def decrypt_fernet(encrypted_data: bytes, key: bytes) -> str:
    """
    Decrypts a Fernet-encrypted byte string and returns a UTF-8 string.

    Args:
        encrypted_data (bytes): Encrypted data.
        key (bytes): Fernet key.

    Returns:
        str: Decrypted text.
    """
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()
