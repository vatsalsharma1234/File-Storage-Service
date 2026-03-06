import os
import hashlib
import uuid
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

STORAGE_DIR = "storage"
METADATA = {}

os.makedirs(STORAGE_DIR, exist_ok=True)


def hash_file(file_bytes):
    """Compute SHA256 hash of file"""
    sha = hashlib.sha256()
    sha.update(file_bytes)
    return sha.hexdigest()


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    data = file.read()

    file_hash = hash_file(data)

    # Deduplication
    for file_id, meta in METADATA.items():
        if meta["hash"] == file_hash:
            return jsonify({
                "message": "File already exists (deduplicated)",
                "file_id": file_id
            })

    file_id = str(uuid.uuid4())
    file_path = os.path.join(STORAGE_DIR, file_id)

    with open(file_path, "wb") as f:
        f.write(data)

    METADATA[file_id] = {
        "filename": file.filename,
        "hash": file_hash,
        "size": len(data),
        "path": file_path
    }

    return jsonify({
        "message": "File uploaded successfully",
        "file_id": file_id
    })


@app.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):
    if file_id not in METADATA:
        return jsonify({"error": "File not found"}), 404

    meta = METADATA[file_id]
    return send_file(meta["path"], download_name=meta["filename"], as_attachment=True)


@app.route("/files", methods=["GET"])
def list_files():
    files = []

    for file_id, meta in METADATA.items():
        files.append({
            "file_id": file_id,
            "filename": meta["filename"],
            "size": meta["size"]
        })

    return jsonify(files)


@app.route("/delete/<file_id>", methods=["DELETE"])
def delete_file(file_id):
    if file_id not in METADATA:
        return jsonify({"error": "File not found"}), 404

    meta = METADATA[file_id]

    os.remove(meta["path"])
    del METADATA[file_id]

    return jsonify({"message": "File deleted"})


if __name__ == "__main__":
    app.run(debug=True)
