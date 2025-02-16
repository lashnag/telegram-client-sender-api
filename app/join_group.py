import os
import logging
from telethon import TelegramClient
from telethon.errors import UserAlreadyParticipantError, InviteHashExpiredError
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from exceptions import InvalidGroupException
from environments_loader import get_credentials

api_id, api_hash, phone_number = get_credentials()

current_dir = os.path.dirname(os.path.abspath(__file__))
session_file_path = os.path.join(current_dir, '../mounted/session.txt')

with open(session_file_path, "r", encoding="utf-8") as file:
    session_string = file.read()

client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def join_group(group_name):
    await client.start(phone_number)
    if group_name.startswith("+"):
        await try_to_join_private_group(group_name.lstrip("+"))
    else:
        await try_to_join_public_group(group_name)


async def try_to_join_public_group(group_name):
    try:
        await client(JoinChannelRequest(group_name))
    except ValueError as invalid_group:
        logging.getLogger().warning(f"ValueError occurred when trying to join the group: {group_name} {invalid_group}")
        raise InvalidGroupException(f"ValueError error occurred when trying to join the group: {group_name} {invalid_group}")
    except Exception as common_error:
        logging.getLogger().warning(f"Common error occurred when trying to join the group: {group_name} {common_error}")
        raise Exception(f"Common error occurred when trying to join the group: {group_name} {common_error}")

async def try_to_join_private_group(invite_code):
    try:
        await client(ImportChatInviteRequest(invite_code))
    except UserAlreadyParticipantError as already_participant:
        logging.getLogger().warning(f"Already participant: {invite_code} {already_participant}")
    except InviteHashExpiredError as invalid_group:
        logging.getLogger().warning(f"Failed to join private group: {invite_code} {invalid_group}")
        raise InvalidGroupException(f"Failed to join private group: {invite_code} {invalid_group}")
    except Exception as common_error:
        logging.getLogger().warning(f"Common error occurred when trying to join the private group: {invite_code} {common_error}")
        raise Exception(f"Common error occurred when when trying to join the private group: {invite_code} {common_error}")