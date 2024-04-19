from hugchat import hugchat
from hugchat.login import Login
from create_log import read_log
from check_log import check_file_log

def import_loog():
    if check_file_log():
        email, passwd = read_log()
        return email, passwd
    else:
        print("No se ha encontrado el fichero de log")
        return None, None


def create_cookies():
    EMAIL, PASSWD = import_loog()
    cookie_path_dir = "./cookies/"
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    return cookies

def create_chatbot():
    cookies = create_cookies()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot

async def chat_init(mensaje):
    chatbot = create_chatbot()
    print(f"Iniciando chat con mensaje: {mensaje}")
    id_chat = chatbot.get_conversation_from_id("Chat GPT")
    query_result:str = chatbot.chat(text=mensaje, model="Chat GPT", system_prompt="Assitente personal", conversation=id_chat)
    print(f"Respuesta: {query_result}")
    return query_result, id_chat  # Accede a la propiedad .text del objeto Message


async def chat_continuo(mensaje, id_chat):
    chatbot = create_chatbot()
    print(f"Continuando chat {id_chat} con mensaje: {mensaje}")
    query_result:str = chatbot.chat(text=mensaje, conversation=id_chat)
    print(f"Respuesta: {query_result}")
    return query_result  # Accede a la propiedad .text del objeto Message



