import logging
import uuid
from .formatter import JsonLogFormatter


def configurar_logger(nome_logger: str = "json_logger") -> logging.Logger:
    logger = logging.getLogger(nome_logger)

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        id_execucao = str(uuid.uuid4())

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(JsonLogFormatter(id_execucao))

        logger.addHandler(handler)

    return logger
