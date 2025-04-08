from flask import Flask, request
from bot import Bot

app = Flask(__name__)
bot_instance = Bot()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    bot_instance.app.update_queue.put(update)
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)