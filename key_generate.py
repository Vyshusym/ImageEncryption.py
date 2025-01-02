import base64
import hashlib

def to_url_safe_base64_32_bytes(user_input):
    # Step 1: Convert input to bytes
    if isinstance(user_input, str):
        user_input = user_input.encode('utf-8')

    # Step 2: Hash input to ensure it's 32 bytes
    hashed_input = hashlib.sha256(user_input).digest()

    # Step 3: Base64 URL-safe encoding
    url_safe_encoded = base64.urlsafe_b64encode(hashed_input).decode('utf-8')

    return url_safe_encoded



