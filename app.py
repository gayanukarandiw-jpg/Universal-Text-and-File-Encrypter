import io
import os
import hashlib
import binascii
from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet, InvalidToken

app = Flask(__name__)

def make_pass(user_password, salt):
    # Generates the secure key format needed for Fernet
    key = hashlib.pbkdf2_hmac('sha256', user_password.encode(), salt, iterations=600000, dklen=32)
    return binascii.b2a_base64(key)

def TXT_encrypt(user_input, encoded_pass, salt):
    fernet = Fernet(encoded_pass)
    encrypted_msg = fernet.encrypt(user_input.encode())
    encrypted_complete = salt + encrypted_msg # First 16 bytes reserved for salt
    return binascii.b2a_base64(encrypted_complete).decode("utf-8")

def TXT_decrypt(encrypted_msg, encoded_pass):
    try:
        fernet = Fernet(encoded_pass)
        return fernet.decrypt(encrypted_msg).decode()
    except InvalidToken:
        return "⛔ Incorrect Secret Key"



# HomePage
@app.route("/")
def home():
    return render_template("index.html")


# Second Page: Text Encrypt
@app.route("/text", methods=["GET", "POST"])
def text_mode():
    result = ""
    error = ""
    
    if request.method == "POST":
        action = request.form.get("action")         
        user_password = request.form.get("password") # Reads the secret key input box
        
        if action == "encrypt":
            user_input = request.form.get("text_to_process")
            current_salt = os.urandom(16) 
            encoded_pass = make_pass(user_password, current_salt)
            result = TXT_encrypt(user_input, encoded_pass, current_salt)
            
        
        elif action == "decrypt":
            try:
                user_input = request.form.get("text_to_process").strip()
                decoded_input = binascii.a2b_base64(user_input)
                
                # Extract salt and Encrypted Text
                extracted_salt, encrypt_text = decoded_input[:16], decoded_input[16:]
                encoded_pass = make_pass(user_password, extracted_salt)
                result = TXT_decrypt(encrypt_text, encoded_pass)
            except Exception:
                error = "⛔ Invalid Encrypted Text Format Was Provided"

    # Send Result 
    return render_template("text.html", result=result, error=error)


# File ENcrypt
@app.route("/file", methods=["GET", "POST"])
def file_mode():
    error = ""
    
    if request.method == "POST":
        action = request.form.get("action")
        user_password = request.form.get("password")
        
        if 'file_input' not in request.files:
            return render_template("file.html", error="⛔ No file selected")
            
        file = request.files['file_input']
        if file.filename == '':
            return render_template("file.html", error="⛔ No file selected")

        try:
            # Read the uploaded file's binary data 
            file_content = file.read()
            original_filename = file.filename

            if action == "encrypt":
                current_salt = os.urandom(16)
                encoded_pass = make_pass(user_password, current_salt)
                fernet = Fernet(encoded_pass)
                encrypted_file_data = fernet.encrypt(file_content)
                encrypted_file_final = current_salt + encrypted_file_data
                final_bytes = binascii.b2a_base64(encrypted_file_final)
                
                # Send the file back to the browser 
                return send_file(
                    io.BytesIO(final_bytes),
                    as_attachment=True,
                    download_name=f"{original_filename}.opcu"#.opcu = only password can unlock :)
                )

            elif action == "decrypt":
                try:
                    # Convert cleaner base64 version back to normal binary cversion
                    default_encrypted_content = binascii.a2b_base64(file_content)
                    extracted_salt, encrypted_data = default_encrypted_content[:16], default_encrypted_content[16:]
                    
                    encoded_pass = make_pass(user_password, extracted_salt)
                    fernet = Fernet(encoded_pass)
                    og_file_content = fernet.decrypt(encrypted_data)
                    new_filename = original_filename.removesuffix(".opcu")
                    if new_filename == original_filename:
                        new_filename = "decrypted_" + original_filename

                    return send_file(
                        io.BytesIO(og_file_content),
                        as_attachment=True,
                        download_name=new_filename
                    )
                except InvalidToken:
                    error = "⛔ Incorrect Secret Key"
                except Exception:
                    error = "⛔ Invalid Encrypted File Format"

        except Exception as e:
            error = f"⛔ An error occurred: {str(e)}"

    return render_template("file.html", error=error)

if __name__ == "__main__":
    app.run(debug=True) # start flask