# SecureDrop API 🛡️

A secure, stateless, "burn-after-reading" secret sharing API. 
Built with modern DevSecOps principles, state-of-the-art AES-GCM encryption, and fully containerized for easy deployment.

## Features

* **Burn-After-Reading:** Secrets are permanently destroyed from the database immediately after being accessed once.
* **Zero-Knowledge Database:** Passwords are encrypted in RAM before hitting the database. The SQLite file contains only AES-GCM ciphertexts and nonces.
* **Stateless Architecture:** No sensitive data is kept in memory. The container can be destroyed and spun up anywhere.
* **DevSecOps Ready:** * Dockerized with a non-root user constraint.
  * Secrets (Master Key) are injected via Environment Variables at runtime.
  * Automated CI/CD pipeline (GitHub Actions) for testing cryptographic functions on every push.

## Tech Stack

* **Framework:** FastAPI (Python 3.11)
* **Database:** SQLite & SQLAlchemy (ORM)
* **Cryptography:** `cryptography` library (AES-GCM 256-bit)
* **Containerization:** Docker & Docker Buildx
* **CI/CD:** GitHub Actions & Pytest

## How to Run (Docker)

The application is fully containerized. You don't need Python installed locally, just Docker.

1. **Clone the repository:**
   ```bash
   git clone git@github.com:YOUR_USERNAME/SecureDrop-API.git
   cd SecureDrop-API
   ```

2. **Create your environment variables:**
   Create a `.env` file in the root directory and generate a secure 32-byte Base64 key:
   ```bash
   echo "ENCRYPTION_KEY=$(python3 -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode('utf-8'))")" > .env
   ```

3. **Build and run the container:**
   ```bash
   docker build -t securedrop-api .
   docker run --rm -p 8000:8000 --env-file .env --name securedrop-container securedrop-api
   ```

4. **Access the API:**
   Open your browser and navigate to the interactive Swagger UI:  
   `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/secrets/` | Encrypts a plaintext secret and returns a unique Link-Key. |
| `GET` | `/secrets/{secret_key}` | Decrypts the secret, returns the plaintext, and permanently deletes the record. |

## Security Notice
This is a portfolio project demonstrating secure backend architecture and DevSecOps pipelines. Ensure that the `.env` file containing the `ENCRYPTION_KEY` is never committed to version control.
