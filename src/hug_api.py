from hugchat import hugchat
from hugchat.login import Login
from logs.create_log import read_log
from logs.check_log import check_file_log

capture_id_chat = []


def import_loog():
    if check_file_log():
        email, passwd = read_log()
        return email, passwd
    else:
        print("No se ha encontrado el fichero de log")
        return None, None


def create_cookies():
    EMAIL, PASSWD = import_loog()
    cookie_path_dir = "./storage/"
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    return cookies


def capture_id_chat_id(id_chat):
    if not capture_id_chat:
        capture_id_chat.append(id_chat)
    return capture_id_chat


# Variable global para mantener la instancia del chatbot
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
    chatbot = create_chatbot()  # Esto ahora reutilizará la instancia global si ya existe
    print(f"Iniciando chat con mensaje: {send}")
    try:
        if not capture_id_chat:
            new_chat = chatbot.new_conversation()
            capture_id_chat.append(new_chat.id)
        id_chat_capture = capture_id_chat[0]
        query_result = chatbot.chat(text=send, conversation_id=id_chat_capture)
        print(f"Id_chat: {id_chat_capture}, Respuesta: {query_result}")
        return query_result
    except Exception as e:
        print(f"Error al iniciar chat: {e}")
        return "Error al iniciar la conversación."


async def chat_continue(send):
    global capture_id_chat, global_chatbot
    chatbot = global_chatbot  # Reutiliza la instancia global del chatbot
    if chatbot is None:
        print("El chatbot no ha sido inicializado.")
        return "El chatbot no ha sido inicializado."

    if not capture_id_chat:
        print("No se ha encontrado el id_chat")
        return "No se ha encontrado el id_chat para continuar la conversación."
    id_chat_capture = capture_id_chat[0]
    try:
        print(f"Continuando chat con mensaje: {send}, {id_chat_capture}")
        query_result = chatbot.chat(text=send, conversation_id=id_chat_capture)
        print(f"Respuesta: {query_result}")
        return query_result
    except Exception as e:
        print(f"Error al continuar el chat: {e}")
        return "Error al continuar la conversación."


def chat_end():
    if import_loog() is not None:
        create_chatbot().delete_all_conversations()