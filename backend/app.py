from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bots.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default="stopped")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/bots', methods=['GET'])
def get_bots():
    bots = Bot.query.all()
    return jsonify([{"id": b.id, "name": b.name, "status": b.status} for b in bots])

@app.route('/api/start_bot/<int:bot_id>', methods=['POST'])
def start_bot(bot_id):
    bot = Bot.query.get(bot_id)
    if bot:
        bot.status = "running"
        db.session.commit()
        return jsonify({"message": f"Bot {bot.name} started."})
    return jsonify({"error": "Bot not found"}), 404

@app.route('/api/stop_bot/<int:bot_id>', methods=['POST'])
def stop_bot(bot_id):
    bot = Bot.query.get(bot_id)
    if bot:
        bot.status = "stopped"
        db.session.commit()
        return jsonify({"message": f"Bot {bot.name} stopped."})
    return jsonify({"error": "Bot not found"}), 404

if __name__ == '__main__':
    db.create_all()

    # Use fixed Ngrok domain
    os.system("ngrok http --url=driven-boxer-partly.ngrok-free.app 5000")
    print("Server running at: https://driven-boxer-partly.ngrok-free.app")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
