from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import COLORS, APP_NAME, LEVELS, BADGES
from core.database import (
    get_profile, update_profile, get_quiz_history, get_best_score,
    save_quiz_result, mark_stage_explored, get_stages_explored,
    mark_myth_revealed, get_myths_revealed, get_earned_badges,
    earn_badge, add_bookmark, get_bookmarks, remove_bookmark,
    save_chat_message, get_chat_history, clear_chat_history,
    mark_glossary_read, reset_all_data, add_xp, get_level
)
from core.language import TRANSLATIONS
from services.live_data import live_data_service

app = Flask(__name__)
CORS(app)

# --- WEB ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

# --- API ENDPOINTS ---

@app.route('/api/config')
def get_config():
    return jsonify({
        "colors": COLORS,
        "app_name": APP_NAME,
        "levels": LEVELS,
        "badges": BADGES,
        "translations": TRANSLATIONS
    })

@app.route('/api/profile', methods=['GET', 'POST'])
def profile_api():
    if request.method == 'POST':
        data = request.json
        update_profile(**data)
        return jsonify({"status": "success"})
    return jsonify(get_profile())

@app.route('/api/xp/add', methods=['POST'])
def add_xp_api():
    data = request.json
    amount = data.get('amount', 0)
    new_xp = add_xp(amount)
    level = get_level(new_xp)
    return jsonify({"xp": new_xp, "level": level})

@app.route('/api/quiz/history')
def quiz_history_api():
    return jsonify(get_quiz_history())

@app.route('/api/quiz/save', methods=['POST'])
def save_quiz_api():
    data = request.json
    save_quiz_result(
        data['category'], data['score'], data['total'],
        data['xp'], data.get('badge', ''), data.get('time_taken', 0)
    )
    return jsonify({"status": "success"})

@app.route('/api/learning/progress')
def learning_progress_api():
    return jsonify({
        "explored_stages": get_stages_explored(),
        "revealed_myths": get_myths_revealed()
    })

@app.route('/api/learning/explore', methods=['POST'])
def explore_stage_api():
    data = request.json
    mark_stage_explored(data['stage_id'], data['stage_name'])
    return jsonify({"status": "success"})

@app.route('/api/myths/reveal', methods=['POST'])
def reveal_myth_api():
    data = request.json
    mark_myth_revealed(data['myth_id'])
    return jsonify({"status": "success"})

@app.route('/api/badges')
def badges_api():
    return jsonify(get_earned_badges())

@app.route('/api/badges/earn', methods=['POST'])
def earn_badge_api():
    data = request.json
    newly_earned = earn_badge(data['badge_id'])
    return jsonify({"newly_earned": newly_earned})

@app.route('/api/bookmarks', methods=['GET', 'POST', 'DELETE'])
def bookmarks_api():
    if request.method == 'POST':
        data = request.json
        add_bookmark(data['type'], data['id'], data['title'], data['content'])
        return jsonify({"status": "success"})
    elif request.method == 'DELETE':
        item_id = request.args.get('id')
        remove_bookmark(item_id)
        return jsonify({"status": "success"})
    return jsonify(get_bookmarks())

@app.route('/api/chat', methods=['GET', 'POST', 'DELETE'])
def chat_api():
    if request.method == 'POST':
        data = request.json
        save_chat_message(data['role'], data['message'])
        return jsonify({"status": "success"})
    elif request.method == 'DELETE':
        clear_chat_history()
        return jsonify({"status": "success"})
    return jsonify(get_chat_history())

@app.route('/api/learning/content')
def learning_content_api():
    with open("data/election_content.json", "r", encoding="utf-8") as f:
        import json
        return jsonify(json.load(f))

@app.route('/api/learning/myths')
def myths_api():
    with open("data/myths_facts.json", "r", encoding="utf-8") as f:
        import json
        return jsonify(json.load(f))

@app.route('/api/learning/glossary')
def glossary_api():
    with open("data/glossary.json", "r", encoding="utf-8") as f:
        import json
        return jsonify(json.load(f))

@app.route('/api/quiz/data')
def quiz_data_api():
    with open("data/quiz_data.json", "r", encoding="utf-8") as f:
        import json
        return jsonify(json.load(f))

@app.route('/api/chat/faq')
def chat_faq_api():
    with open("data/chatbot_faq.json", "r", encoding="utf-8") as f:
        import json
        return jsonify(json.load(f))

@app.route('/api/live-data')
def live_data_api():
    return jsonify({
        "updates": live_data_service.get_updates(),
        "last_updated": live_data_service.get_last_updated_string()
    })

@app.route('/api/glossary/read', methods=['POST'])
def glossary_read_api():
    data = request.json
    mark_glossary_read(data['term'])
    return jsonify({"status": "success"})

@app.route('/api/reset', methods=['POST'])
def reset_api():
    reset_all_data()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Default to port 8080 for Google Cloud Shell compatibility
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
