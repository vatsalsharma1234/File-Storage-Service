# File Storage Service

A lightweight backend service that allows users to **upload, download, list, and delete files** while supporting **file deduplication using SHA-256 hashing**.

This project demonstrates core backend concepts such as **file storage systems, hashing, REST APIs, and metadata management**.

---

## Features

- Upload files through REST API
- Download stored files
- List all stored files
- Delete files
- **File deduplication** using SHA-256 hashing
- Stores file metadata (name, size, hash)
- Simple storage layer using local file system

---

## Tech Stack

- Python
- Flask
- REST APIs
- SHA-256 hashing

---

## Project Structure


file-storage-service/
│
├── file_storage_service.py # Main backend service
├── storage/ # Directory where files are stored
└── README.md


---

## How It Works

### File Upload

1. User uploads a file through `/upload`
2. System calculates **SHA-256 hash**
3. If the file already exists (same hash), it is **deduplicated**
4. Otherwise, it is stored in the `storage/` directory
5. Metadata is stored in memory

---

### Metadata Stored

Each file stores:

- File ID
- Filename
- File size
- SHA-256 hash
- Storage path

---

## API Endpoints

### Upload File


POST /upload


Example:


curl -X POST -F "file=@test.txt" http://127.0.0.1:5000/upload


Response:

```json
{
  "message": "File uploaded successfully",
  "file_id": "12345"
}
Download File

GET /download/<file_id>


Example:


curl http://127.0.0.1:5000/download/12345

List Files

GET /files


Example response:

[
  {
    "file_id": "12345",
    "filename": "test.txt",
    "size": 1024
  }
]
Delete File

DELETE /delete/<file_id>


Example:


curl -X DELETE http://127.0.0.1:5000/delete/12345

Installation
1 Clone the repository

git clone https://github.com/yourusername/file-storage-service.git
cd file-storage-service

2 Install dependencies

pip install flask

3 Run the server

python file_storage_service.py
