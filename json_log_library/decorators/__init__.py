from typing import Literal
import logging
from .v1 import LogExecucaoV1


def log_execucao(
    logger: logging.Logger,
    versao: Literal["v1"] = "v1"
):
    if versao == "v1":
        return LogExecucaoV1(logger)

    raise ValueError(f"Versão não suportada: {versao}")
