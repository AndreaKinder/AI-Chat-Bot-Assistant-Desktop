from hugchat import hugchat
from hugchat.login import Login
from src.logs.create_log import read_log
from src.logs.check_log import check_file_log

capture_id_chat = []


def import_log():
    if check_file_log():
        email, passwd = read_log()
        return email, passwd
    else:
        print("No file log.json")
        return None, None


def create_cookies():
    EMAIL, PASSWD = import_log()
    cookie_path_dir = "./storage/"
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    return cookies


def capture_id_chat_id(id_chat):
    if not capture_id_chat:
        capture_id_chat.append(id_chat)
    return capture_id_chat


global_chatbot = None


def create_chatbot():
    global global_chatbot
    if global_chatbot is None:
        cookies = create_cookies()
        global_chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        new_chat = global_chatbot.new_conversation()
        new_id = new_chat.id
        capture_id_chat_id(id_chat=new_id)
    return global_chatbot


async def chat_init(send):
    global capture_id_chat
    chatbot = create_chatbot()
    print(f"Chat init and send: {send}")
    try:
        if not capture_id_chat:
            new_chat = chatbot.new_conversation()
            capture_id_chat.append(new_chat.id)
        id_chat_capture = capture_id_chat[0]
        query_result = chatbot.chat(text=send, conversation_id=id_chat_capture)
        print(f"Id_chat: {id_chat_capture}, Response: {query_result}")
        return query_result
    except Exception as e:
        print(f"Error chat init: {e}")
        return "Error chat init."


async def chat_continue(send):
    global capture_id_chat, global_chatbot
    chatbot = global_chatbot
    if chatbot is None:
        print("El chatbot no init.")
        return "El chatbot no init."

    if not capture_id_chat:
        print("Chat_id not found")
        return "Chat_id not found."
    id_chat_capture = capture_id_chat[0]
    try:
        print(f"Continue chat and send: {send}, {id_chat_capture}")
        query_result = chatbot.chat(text=send, conversation_id=id_chat_capture)
        print(f"Response: {query_result}")
        return query_result
    except Exception as e:
        print(f"Error continue chat: {e}")
        return "Error continue chat."


def chat_end():
    if import_log() is not None:
        create_chatbot().delete_all_conversations()
