import collections.abc
from typing import Optional, Sequence, Union


def get_allow_block_lists(filter_list):
    allow_list = []
    block_list = []

    if filter_list:
        for item in filter_list:
            if item.startswith("!"):
                block_list.append(item[1:].strip())
            else:
                allow_list.append(item.strip())

    return allow_list, block_list


def is_string_allowed(
    string: Union[str, Sequence[str]], filter_list: Optional[list[str]] = None
) -> bool:
    """
    Checks if a string is allowed based on the provided filter list.
    :param string: The string or sequence of strings to check (e.g., domain or hostname).
    :param filter_list: List of allowed/blocked strings. Strings starting with "!" are blocked.
    :return: True if the string or sequence of strings is allowed, False otherwise.
    """
    if not filter_list:
        return True

    allow_list, block_list = get_allow_block_lists(filter_list)
    strings = [string] if isinstance(string, str) else list(string)

    # If allow list is non-empty, require domain to match one of them
    if allow_list:
        if not any(s.endswith(allowed) for s in strings for allowed in allow_list):
            return False

    # Block list always removes matches
    if any(s.endswith(blocked) for s in strings for blocked in block_list):
        return False

    return True


def get_message_list(messages_map, message_id):
    """
    Reconstructs a list of messages in order up to the specified message_id.
    :param message_id: ID of the message to reconstruct the chain
    :param messages: Message history dict containing all messages
    :return: List of ordered messages starting from the root to the given message
    """
    if not messages_map:
        return []

    current_message = messages_map.get(message_id)
    if not current_message:
        return []

    message_list = []
    while current_message:
        message_list.insert(0, current_message)
        parent_id = current_message.get("parentId")
        current_message = messages_map.get(parent_id) if parent_id else None

    return message_list
