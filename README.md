# Image Encryption: Securing Visual Data in the Digital Realm

<div align="center">
  <b>University of Mysore</b><br>
  <b>Mysore University School of Engineering</b><br>
  <b>Department of Computer Science and Design</b><br>
  <b>Author: Vyshali</b><br>
  <b>Date: Dec 29, 2024</b>
</div>

## Access this project : https://project-by-vyshali-image-encryption-01.streamlit.app/


https://github.com/user-attachments/assets/6a476d43-a76f-400d-9782-a5e205ccbb8d


## Abstract

The proliferation of digital images across platforms demands strong protection against unauthorized access and tampering. This project presents a **Streamlit‑based application** that encrypts and decrypts images using **AES (via the Fernet implementation)** to guarantee confidentiality and integrity of visual data. We derive **32‑byte keys from user input** using SHA‑256 and Base64 encoding, process images with Pillow, and provide a **user‑friendly interface** for secure image handling.

---

## Introduction

Digital images often carry sensitive information — medical scans, financial documents, or personal photos. Without encryption, interception or modification can result in privacy breaches or data corruption. **AES** is a U.S. government‑standard symmetric cipher renowned for both security and efficiency. **Fernet**, from the Python Cryptography library, provides authenticated encryption built on AES, ensuring data cannot be tampered with undetected. **Pillow (PIL fork)** offers robust image I/O and manipulation, making it ideal for preparing data for encryption and reconstructing images after decryption.

---

## Methodology

### Requirement Analysis

* **Domains Considered:**

  * Healthcare confidentiality
  * Financial document security
  * Secure multimedia messaging

### Algorithm Selection

* **AES/Fernet:** Chosen for symmetric authenticated encryption; balances strong security with performance suitable for real‑time use.
* **Key Derivation:** SHA‑256 hashing ensures a fixed 32‑byte key, then URL‑safe Base64 encodes it for Fernet compatibility.

### Implementation

* **Language:** Python, for rapid development and rich library support.
* **Front End:** Streamlit for an interactive web UI with minimal code.
* **Image Handling:** Pillow to read, display, and save images.
* **Key Generation:** Custom `key_generate.py` uses `hashlib.sha256` and `base64.urlsafe_b64encode`.

```python
# key_generate.py
import base64
import hashlib

def to_url_safe_base64_32_bytes(user_input):
    if isinstance(user_input, str):
        user_input = user_input.encode('utf-8')
    hashed_input = hashlib.sha256(user_input).digest()
    url_safe_encoded = base64.urlsafe_b64encode(hashed_input).decode('utf-8')
    return url_safe_encoded
```

---

## Testing & Validation

* **Confidentiality:** Verified that encrypted output cannot be decrypted without the correct key.
* **Integrity:** Round‑trip tests confirm decrypted images match originals pixel‑for‑pixel.

---

## Performance Optimization

* Buffered image operations via `io.BytesIO` to minimize disk I/O.
* Key derivation and encryption executed **in-memory** for speed.

---

## User Feedback & Iteration

* Added **sidebar warnings** and **success/error messages** for clarity.
* Integrated **download buttons** for both encrypted `.enc` files and restored image formats.

---

## Code Overview

```python
# main.py
import streamlit as st
import key_generate as key_g
from cryptography.fernet import Fernet
from PIL import Image
import io

def encrypt_image(image, key):
    fernet = Fernet(key)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    encrypted_data = fernet.encrypt(image_bytes.getvalue())
    return encrypted_data

def decrypt_image(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    decrypted_image = Image.open(io.BytesIO(decrypted_data))
    return decrypted_image

def main():
    st.title("Image Encryption and Decryption Using AES")

    st.sidebar.title("Options")
    option = st.sidebar.radio("Choose an action", ["Encrypt an Image", "Decrypt an Image"])

    user_input = st.sidebar.text_input("Encryption Key (Use a valid Fernet key)", type="password")
    key = key_g.to_url_safe_base64_32_bytes(user_input)

    if option == "Encrypt an Image":
        uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", use_column_width=True)

            if key:
                try:
                    key_bytes = key.encode()
                    encrypted_data = encrypt_image(image, key_bytes)
                    st.success("Image Encrypted Successfully!")

                    st.download_button(
                        label="Download Encrypted Image",
                        data=encrypted_data,
                        file_name="encrypted_image.enc",
                        mime="application/octet-stream"
                    )
                except Exception as e:
                    st.error(f"Encryption failed: {e}")
            else:
                st.warning("Please provide a valid encryption key.")

    elif option == "Decrypt an Image":
        encrypted_file = st.file_uploader("Upload Encrypted Image", type=["enc"])
        if encrypted_file and key:
            try:
                key_bytes = key.encode()
                encrypted_data = encrypted_file.read()

                decrypted_image = decrypt_image(encrypted_data, key_bytes)
                st.image(decrypted_image, caption="Decrypted Image", use_column_width=True)

                decrypted_image_bytes = io.BytesIO()
                decrypted_image_format = decrypted_image.format or "PNG"
                decrypted_image.save(decrypted_image_bytes, format=decrypted_image_format)
                st.download_button(
                    label="Download Decrypted Image",
                    data=decrypted_image_bytes.getvalue(),
                    file_name=f"decrypted_image.{decrypted_image_format.lower()}",
                    mime=f"image/{decrypted_image_format.lower()}"
                )
            except Exception as e:
                st.error(f"Decryption failed: {e}")
        else:
            st.warning("Please upload an encrypted image and provide a valid encryption key.")

    st.info(
        """
        **Note**: This software is for **educational purposes** only. The author is not liable for any misuse or damages caused by using this tool.
        Use responsibly and comply with all applicable laws.
        """
    )

if __name__ == "__main__":
    main()
```

---

## Requirements

```txt
# requirements.txt
streamlit
pillow
cryptography
```

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## Disclaimer

> **Note:** This software is intended **only for educational purposes**. The author assumes **no responsibility** for any damage or misuse caused by using this tool. Use it responsibly and adhere to all applicable laws.

---

## Outcome

* **Enhanced Security:** Protection against unauthorized access and tampering.
* **Compatibility:** Works with standard image formats (`.jpg`, `.jpeg`, `.png`).
* **Performance:** Efficient for real-time image encryption and decryption.
* **User-Friendly:** Interactive interface with encryption and decryption options.

---

## How to Run in Google Colab

1. Upload `main.py`, `key_generate.py`, and `requirements.txt` to Colab.
2. Install libraries:

```python
!pip install -r requirements.txt
```

3. Run the app (using localtunnel for public URL):

```python
!pip install streamlit
!pip install pyngrok

# Start Streamlit app
import os
os.system('streamlit run main.py &')

# Tunnel using ngrok
from pyngrok import ngrok
public_url = ngrok.connect(port='8501')
print(public_url)
```

---

## How to Use

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/image-encryption-project.git
   cd image-encryption-project
   ```
2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
3. **Generate Encryption Key**

   * In Python REPL or a script:

     ```python
     from cryptography.fernet import Fernet
     key = Fernet.generate_key().decode()
     print(key)
     ```
   * Copy the printed key for use in the app.
4. **Run the Streamlit App**

   ```bash
   streamlit run main.py
   ```
5. **Encrypt an Image**

   * Select **Encrypt an Image** in the sidebar.
   * Paste your encryption key.
   * Upload a `.jpg`, `.jpeg`, or `.png` file.
   * Download the encrypted `.enc` file.
6. **Decrypt an Image**

   * Select **Decrypt an Image**.
   * Paste the same encryption key used earlier.
   * Upload the `.enc` file.
   * View and download the decrypted image in its original format.
     

## 🔐 How to Use the Image Encryption App

Follow these steps to encrypt & decrypt your images:

1. 📥 **Select “Encrypt”**  

    * Open the app at https://project-by-vyshali-image-encryption-01.streamlit.app
    
    * In the sidebar, choose Encrypt an Image
    
    * Enter your secret password/key

2. 🖼️ **Upload & Encrypt**  
    * Click “Browse files” and pick your image (JPG, PNG, etc.)
    
    * Click Encrypt
    
    * Download the encrypted file (.enc)

3. 📤 **Share Encrypted File**  
    * Send the .enc file via WhatsApp, email, or any messenger
    
    * Make sure the recipient knows the password

4. 🔄 **Decrypt the Image**  
    * Return to https://project-by-vyshali-image-encryption-01.streamlit.app
    
    * In the sidebar, choose Decrypt an Image
    
    * Enter the same password/key
    
    * Upload the received .enc file
    
    * Click Decrypt

5. 📂 **Download Decrypted Image**  
   * After processing, click Download Decrypted Image
   * Your original image is restored, pixel-perfect!

Happy Encrypting! 🔐📸
