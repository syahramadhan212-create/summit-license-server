from flask import Flask, request, jsonify
import os, random, string, json

app = Flask(__name__)
ADMIN_PASSWORD = "DHANLIB-ADMIN-2024"
DB_FILE = "keys.json"

def load_keys():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "SUMMIT-KIT-PREMIUM-DHANLIB-V1": {"owner": "DhanLiB", "active": True, "gameids": []},
    }

def save_keys(keys):
    with open(DB_FILE, "w") as f:
        json.dump(keys, f, indent=2)

# ═══════════════════════════════════════
# CEK KEY + DETEKSI GAME ID
# ═══════════════════════════════════════
@app.route("/check", methods=["GET"])
def check_key():
    keys = load_keys()
    key = request.args.get("key", "")
    gameid = request.args.get("gameid", "")

    if key not in keys:
        return jsonify({"status": "invalid"})

    data = keys[key]

    if not data["active"]:
        return jsonify({"status": "revoked"})

    # Cek Game ID
    if gameid:
        if "gameids" not in data:
            data["gameids"] = []

        if gameid not in data["gameids"]:
            # Game ID baru
            if len(data["gameids"]) >= 1:
                # Sudah ada 1 game ID berbeda = kemungkinan dijual lagi!
                data["active"] = False
                save_keys(keys)
                return jsonify({
                    "status": "revoked",
                    "reason": "Key dipakai di lebih dari 1 game!"
                })
            else:
                # Game ID pertama, simpan
                data["gameids"].append(gameid)
                save_keys(keys)

    return jsonify({"status": "valid", "owner": data["owner"]})

# ═══════════════════════════════════════
# GENERATE KEY BARU
# ═══════════════════════════════════════
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
    keys[new_key] = {"owner": owner, "active": True, "gameids": []}
    save_keys(keys)
    return jsonify({"status": "success", "key": new_key, "owner": owner})

# ═══════════════════════════════════════
# CABUT KEY
# ═══════════════════════════════════════
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

# ═══════════════════════════════════════
# LIHAT SEMUA KEY (untuk kamu sebagai admin)
# ═══════════════════════════════════════
@app.route("/list", methods=["GET"])
def list_keys():
    if request.args.get("admin", "") != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Password salah!"})
    keys = load_keys()
    return jsonify({"status": "success", "keys": keys})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
