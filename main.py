import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- SIMPLE DATABASE (JSON FILE) ---
DB_FILE = 'local_db.json'

# Data Load karne ka function
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

# Data Save karne ka function
def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- GAME PAGES ---
@app.route('/')
def home():
    return render_template('index.html')

# --- API (LEN-DEN) ---
@app.route('/api/save_score', methods=['POST'])
def save_score():
    try:
        data = request.json
        user_id = str(data.get('user_id', 'unknown'))
        new_score = data.get('score', 0)
        
        # Database Load karo
        db_data = load_db()
        
        # Update karo (Simple Logic)
        if user_id in db_data:
            # Sirf tab update karo agar naya score jyada hai
            if new_score > db_data[user_id]['score']:
                db_data[user_id]['score'] = new_score
        else:
            # New User
            db_data[user_id] = {'score': new_score}
            
        # Save wapas file mein
        save_db(db_data)
        
        return jsonify({"status": "success", "message": "Saved to File!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    db_data = load_db()
    # List banao aur sort karo
    leaderboard = []
    for uid, info in db_data.items():
        leaderboard.append({"name": "Player " + uid[-4:], "score": info['score']})
    
    # Sort by score (High to Low)
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    
    return jsonify(leaderboard[:10])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

