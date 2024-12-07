subscriptions = {}
exception_subscriptions = set()
processed_messages = {}

def add_subscription(subscriber, group, keyword):
    if group not in subscriptions:
        subscriptions[group] = {}
    if subscriber not in subscriptions[group]:
        subscriptions[group][subscriber] = set()
    subscriptions[group][subscriber].add(keyword)

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