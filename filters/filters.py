from models import db


def user_in_chat_from_service_to_client(receiver_chat_id, sender_chat_id, service_or_client: str = 'client',
                                        current_event_id=None):
    """
    :param receiver_chat_id: receiver based in client bot
    :param sender_chat_id: sender based in service bot
    :param service_or_client: elect chat, 'service' to service, 'client' to client
    :param current_event_id: user current event
    :return: boolean

    """
    user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == receiver_chat_id])

    receiver_user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == receiver_chat_id])
    sender_user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == sender_chat_id])

    if isinstance(receiver_user, db.User) and isinstance(sender_user, db.User):
        # dont send keyboard if receiver in chat in service, id's same and sender user in client chat
        return receiver_user.in_chat_client \
               and receiver_user.current_event_id == sender_user.current_event_id \
               and sender_user.in_chat_service

