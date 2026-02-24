from flask import Flask, request, jsonify
import os, random, string, json

app = Flask(__name__)
ADMIN_PASSWORD = "DHANLIB-ADMIN-2024"
DB_FILE = "keys.json"

# Load dari file
def load_keys():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "SUMMIT-AAAA-BBBB-1111": {"owner": "PlayerSatu", "active": True},
        "SUMMIT-CCCC-DDDD-2222": {"owner": "PlayerDua", "active": True},
        "SUMMIT-KIT-PREMIUM-DHANLIB-V1": {"owner": "DhanLiB", "active": True},
    }

# Simpan ke file
def save_keys(keys):
    with open(DB_FILE, "w") as f:
        json.dump(keys, f, indent=2)

@app.route("/check", methods=["GET"])
def check_key():
    keys = load_keys()
    key = request.args.get("key", "")
    if key in keys:
        data = keys[key]
        if data["active"]:
            return jsonify({"status": "valid", "owner": data["owner"]})
        else:
            return jsonify({"status": "revoked"})
    return jsonify({"status": "invalid"})

@app.route("/generate", methods=["GET"])
def generate_key():
    if request.args.get("admin", "") != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Password salah!"})
    owner = request.args.get("owner", "")
    if not owner:
        return jsonify({"status": "error", "message": "Owner kosong!"})
    keys = load_keys()
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    new_key = f"SUMMIT-{rand[:4]}-{rand[4:]}-{random.randint(1000,9999)}"
    keys[new_key] = {"owner": owner, "active": True}
    save_keys(keys)
    return jsonify({"status": "success", "key": new_key, "owner": owner})

@app.route("/revoke", methods=["GET"])
def revoke_key():
    if request.args.get("admin", "") != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Password salah!"})
    key = request.args.get("key", "")
    keys = load_keys()
    if key not in keys:
        return jsonify({"status": "error", "message": "Key tidak ditemukan!"})
    keys[key]["active"] = False
    save_keys(keys)
    return jsonify({"status": "success", "message": f"Key {key} dicabut!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
