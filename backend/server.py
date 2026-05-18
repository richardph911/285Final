from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'votes.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            cuisine TEXT,
            image_url TEXT,
            emoji TEXT
        );
        CREATE TABLE IF NOT EXISTS votes (
            id TEXT PRIMARY KEY,
            item_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            choice TEXT NOT NULL CHECK(choice IN ('yes', 'no')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(item_id, session_id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        );
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/items')
def get_items():
    conn = get_db()
    items = conn.execute('SELECT * FROM items ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(row) for row in items])

@app.route('/vote', methods=['POST'])
def post_vote():
    data = request.get_json(silent=True) or {}
    item_id = data.get('itemId', '').strip()
    choice = data.get('choice', '').strip()
    session_id = data.get('sessionId', '').strip()

    if not item_id or not choice or not session_id:
        return jsonify({'error': 'itemId, choice, and sessionId are required'}), 400
    if choice not in ('yes', 'no'):
        return jsonify({'error': 'choice must be yes or no'}), 400
    if not (8 <= len(session_id) <= 64):
        return jsonify({'error': 'invalid sessionId'}), 400

    conn = get_db()
    item = conn.execute('SELECT id FROM items WHERE id = ?', (item_id,)).fetchone()
    if not item:
        conn.close()
        return jsonify({'error': 'item not found'}), 404

    conn.execute('''
        INSERT INTO votes (id, item_id, session_id, choice)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(item_id, session_id) DO UPDATE SET choice = excluded.choice
    ''', (str(uuid.uuid4()), item_id, session_id, choice))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/results')
def get_results():
    conn = get_db()
    rows = conn.execute('''
        SELECT
            i.id, i.name, i.description, i.cuisine, i.image_url, i.emoji,
            COUNT(CASE WHEN v.choice = 'yes' THEN 1 END) as yes_count,
            COUNT(CASE WHEN v.choice = 'no' THEN 1 END) as no_count,
            COUNT(v.id) as total_votes
        FROM items i
        LEFT JOIN votes v ON i.id = v.item_id
        GROUP BY i.id
        ORDER BY yes_count DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/results/<session_id>')
def get_session_votes(session_id):
    conn = get_db()
    votes = conn.execute(
        'SELECT item_id, choice FROM votes WHERE session_id = ?', (session_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in votes])

if __name__ == '__main__':
    app.run(port=3001, debug=True)
