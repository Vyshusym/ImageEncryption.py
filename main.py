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

    # Sidebar
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

                # Decode Base64 if provided by user (uncomment if applicable)
                # encrypted_data = base64.b64decode(encrypted_data)

                decrypted_image = decrypt_image(encrypted_data, key_bytes)
                st.image(decrypted_image, caption="Decrypted Image", use_column_width=True)

                # Save decrypted image to bytes for download
                decrypted_image_bytes = io.BytesIO()
                decrypted_image_format = decrypted_image.format or "PNG"  # Default to PNG if format is missing
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


if __name__ == "__main__":
    main()
