import logging
import json
from datetime import datetime
from typing import Any, Dict


class JsonLogFormatter(logging.Formatter):

    def __init__(self, id_execucao: str):
        super().__init__()
        self.id_execucao = id_execucao

        # Campos padrão do LogRecord (para evitar sobrescrever)
        self._campos_padrao = set(logging.LogRecord(
            name="",
            level=0,
            pathname="",
            lineno=0,
            msg="",
            args=(),
            exc_info=None
        ).__dict__.keys())

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "id_execucao": self.id_execucao,
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nivel": record.levelname,
            "mensagem": record.getMessage(),
            "funcao": record.funcName,
            "linha": record.lineno,
        }

        # Captura automaticamente qualquer campo extra
        for key, value in record.__dict__.items():
            if key not in self._campos_padrao:
                log_data[key] = value

        # Estrutura erro
        if record.exc_info:
            exc_type, exc_value, _ = record.exc_info
            log_data["erro"] = {
                "tipo": exc_type.__name__,
                "mensagem": str(exc_value),
                "traceback": self.formatException(record.exc_info),
            }

        return json.dumps(log_data, ensure_ascii=False)