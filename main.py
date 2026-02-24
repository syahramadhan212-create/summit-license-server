from flask import Flask, request, jsonify
import os

app = Flask(__name__)

VALID_KEYS = {
    "SUMMIT-AAAA-BBBB-1111": {"owner": "PlayerSatu", "active": True},
    "SUMMIT-CCCC-DDDD-2222": {"owner": "PlayerDua", "active": True},
}

@app.route("/check", methods=["GET"])
def check_key():
    key = request.args.get("key", "")
    if key in VALID_KEYS:
        data = VALID_KEYS[key]
        if data["active"]:
            return jsonify({"status": "valid", "owner": data["owner"]})
        else:
            return jsonify({"status": "revoked"})
    return jsonify({"status": "invalid"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
