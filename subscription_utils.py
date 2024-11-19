from collections import defaultdict

subscriptions = defaultdict(lambda: defaultdict(set))
exception_subscriptions = set()

def add_subscription(subscriber, subscription, keyword):
    subscriptions[subscriber][subscription].add(keyword)

def get_subscriptions_with_keywords(subscriber):
    if subscriber in subscriptions:
        return {
            group: list(keywords if isinstance(keywords, set) else keywords.keys())
            for group, keywords in subscriptions[subscriber].items()
        }
    else:
        return {}

def remove_subscriber(recipient_username):
    if recipient_username in subscriptions:
        del subscriptions[recipient_username]
        return True
    return False

def remove_subscription(recipient_username, group_username):
    if recipient_username in subscriptions and group_username in subscriptions[recipient_username]:
        del subscriptions[recipient_username][group_username]
        return True
    return False

def remove_keyword(recipient_username, group_username, keyword):
    if (recipient_username in subscriptions and
        group_username in subscriptions[recipient_username] and
        keyword in subscriptions[recipient_username][group_username]):
        subscriptions[recipient_username][group_username].remove(keyword)
        if not subscriptions[recipient_username][group_username]:
            del subscriptions[recipient_username][group_username]
        return True
    return False

def clear_subscriptions():
    subscriptions.clear()