from flask import Flask, request, jsonify
from flask_cors import CORS
from subscription_utils import add_subscription, get_subscriptions_with_keywords, remove_subscriber, \
    remove_subscription, remove_keyword

app = Flask(__name__)
CORS(app)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    subscriber = data.get('subscriber')
    subscription = data.get('subscription')
    keyword = data.get('keyword')

    if subscriber and subscription and keyword:
        add_subscription(subscriber, subscription, keyword)
        return jsonify({"message": "Subscription added successfully"}), 201
    else:
        return jsonify({"error": "Invalid data"}), 400

@app.route('/subscriptions/<username>', methods=['GET'])
def get_subscriptions(username):
    subscriptions_list = get_subscriptions_with_keywords(username)
    return jsonify(subscriptions_list), 200

@app.route('/subscriptions/<username>', methods=['DELETE'])
def delete_subscriber(username):
    remove_subscriber(username)
    return jsonify({"message": "Deleted"}), 204

@app.route('/subscriptions/<username>/<subscription>', methods=['DELETE'])
def delete_subscription(username, subscription):
    remove_subscription(username, subscription)
    return jsonify({"message": "Deleted"}), 204

@app.route('/subscriptions/<username>/<subscription>/<keyword>', methods=['DELETE'])
def delete_keyword(username, subscription, keyword):
    remove_keyword(username, subscription, keyword)
    return jsonify({"message": "Deleted"}), 204

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'response': 'ok'}), 200

async def run_flask():
    app.run(debug=True, host='127.0.0.1', port=20000)