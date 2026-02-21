from json_log_library.logger import configurar_logger
from json_log_library.decorators import log_execucao

logger = configurar_logger()


@log_execucao(logger)
def dividir(a: int, b: int) -> float:
    logger.debug(
        "Executando regra de negócio",
        extra={
            "operacao": "divisao",
            "valor_a": a,
            "valor_b": b
        }
    )
    return a / b

dividir(10, 2)