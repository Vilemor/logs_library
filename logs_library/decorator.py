import functools
from .logger import configurar_logger

def log_json(nome_logger: str = "json_logger"):
    """
    Decorator para logar entrada, saída e exceções de funções em JSON.
    """
    def decorator(func):
        import functools
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = configurar_logger(nome_logger)
            logger.info("Chamada da função", extra={
                "input_args": args,
                "input_kwargs": kwargs
            })
            try:
                result = func(*args, **kwargs)
                logger.info("Retorno da função", extra={"retorno": result})
                return result
            except Exception:
                logger.exception("Exceção capturada")
                raise
        return wrapper
    return decorator