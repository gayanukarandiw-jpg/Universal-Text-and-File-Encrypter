# 🔒 Universal File And Text Encrypter

A sleek, modern web application built with **Flask** and **Python** that provides high-security encryption and decryption utilities for both plain text messages and physical file objects.

![Preview](https://img.shields.io/badge/Security-AES--Fernet-emerald?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-black?style=for-the-badge&logo=flask)

---

## 🚀 Core Features

- **Cyber-Vault UI:** Beautiful glass-morphism dashboard interface styled with premium glowing neon accents and responsive fluid animations.
- **Text Cipher Engine:** Instantly converts sensitive string payloads into clean, transferable base64 encrypted tokens.
- **Secure File Vault:** Features a stream-in-memory framework allowing users to upload any local file type, apply encryption protocols, and instantly receive a protected `.opcu` package download.
- **Enhanced Security Protocol:** Uses industry-standard **AES-128-CBC** via Fernet specifications, fortified with individual unique `os.urandom(16)` salting and high-iteration `PBKDF2` key derivation per action.
- **Client-Side Safety:** Auto-wipes authorization secret passphrase input fields instantly upon form submission to prevent post-execution browser snooping.

---

## 📦 Technical Architecture & Data Flow

When you process data through the system, it follows a secure pipeline mapping the web UI down to local runtime cryptographic structures:

1. **Frontend Request:** The browser captures inputs through forms using `enctype="multipart/form-data"` for file binary streams.
2. **Key Derivation (PBKDF2):** Passwords undergo standard PBKDF2 hashing using SHA-256 with 600,000 iterations against a dynamically generated salt chunk.
3. **Fernet Encryption:** The message payload is packed inside an authenticated cryptographic envelope.
4. **Memory Delivery:** Flask uses a non-blocking `io.BytesIO` buffer to instantly pass file attachments back down the network as an automatic browser download—leaving no permanent trail on the server's filesystem.

---

## 🛠️ Installation & Local Setup

Clone the repository and jump into the framework directory:
```bash
git clone [https://github.com/gayanukarandiw-jpg/cyber-crypto-vault.git]
cd cyber-crypto-vault
