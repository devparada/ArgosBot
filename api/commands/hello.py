"""
hello.py — Comando /hello
"""

from api.utils import enviar_mensaje_telegram


def cmd_hello(chat_id, _data=None):
    enviar_mensaje_telegram("¡Hola! Soy ArgosBot. El servidor funciona. ✅", chat_id)
