from collections import defaultdict

subscriptions = defaultdict(lambda: defaultdict(set))
exception_subscriptions = set()
processed_messages = {}

def add_subscription(subscriber, subscription, keyword):
    subscriptions[subscriber][subscription].add(keyword)

def clear_subscriptions():
    subscriptions.clear()


def add_processed_message(group_id, user_id, message_id):
    key = f"{group_id}_{user_id}"
    if key not in processed_messages:
        processed_messages[key] = set()
    processed_messages[key].add(message_id)

def is_message_processed(group_id, user_id, message_id):
    key = f"{group_id}_{user_id}"
    return message_id in processed_messages.get(key, set())