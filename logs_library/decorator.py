import functools
from .logger import configurar_logger

def log_json(
    mensagem: str = None,
    nome_logger: str = "json_logger"
) -> callable:
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = configurar_logger(nome_logger)
            msg = mensagem or f"Chamada da função {func.__name__}"
            logger.info(
                msg,
                extra={
                    "input_args": args,
                    "input_kwargs": kwargs,
                    "funcao_real": func.__name__,  # campo customizado
                }
            )
            try:
                result = func(*args, **kwargs)
                logger.info(
                    f"Retorno da função {func.__name__}",
                    extra={
                        "retorno": result,
                        "funcao_real": func.__name__,  # campo customizado
                    }
                )
                return result
            except Exception:
                logger.exception(
                    f"Exceção capturada em {func.__name__}",
                    extra={"funcao_real": func.__name__}  # campo customizado
                )
                raise
        return wrapper
    return decorator