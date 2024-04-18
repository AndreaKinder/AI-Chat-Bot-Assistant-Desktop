from hugchat import hugchat
from hugchat.login import Login
from hugchat.hugchat import Conversation


EMAIL = "andreavillartr@gmail.com"
PASSWD = "HK3pJde@feAQge"
cookie_path_dir = "./cookies/"
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

async def chat_init(mensaje):
    print(f"Iniciando chat con mensaje: {mensaje}")
    id_chat = chatbot.get_conversation_from_id("Chat GPT")
    query_result:str = chatbot.chat(text=mensaje, model="Chat GPT", system_prompt="Assitente personal", conversation=id_chat)
    print(f"Respuesta: {query_result}")
    return query_result, id_chat  # Accede a la propiedad .text del objeto Message


async def chat_continuo(mensaje, id_chat):
    print(f"Continuando chat {id_chat} con mensaje: {mensaje}")
    query_result:str = chatbot.chat(text=mensaje, conversation=id_chat)  # Asegúrate de usar await aquí
    print(f"Respuesta: {query_result}")
    return query_result  # Accede a la propiedad .text del objeto Message



