import functools
from .logger import configurar_logger

def log_json(nome_logger: str = "json_logger"):
    """
    Decorator para logar entrada, saída e exceções de funções em JSON.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = configurar_logger(nome_logger)
            logger.info("Chamada da função", extra={"args": args, "kwargs": kwargs})
            try:
                result = func(*args, **kwargs)
                logger.info("Retorno da função", extra={"retorno": result})
                return result
            except Exception as e:
                logger.exception("Exceção capturada")
                raise
        return wrapper
    return decorator