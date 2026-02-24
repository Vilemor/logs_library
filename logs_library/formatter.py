import logging
import json
import os
import traceback
from datetime import datetime
from typing import Any, Dict


class JsonLogFormatter(logging.Formatter):
    def __init__(self, id_execucao: str):
        super().__init__()
        self.id_execucao = id_execucao
        self._campos_padrao = set(logging.LogRecord(
            name="",
            level=0,
            pathname="",
            lineno=0,
            msg="",
            args=(),
            exc_info=None
        ).__dict__.keys())

    def _extract_error_info(self, exc_info):
        exc_type, exc_value, exc_tb = exc_info
        tb_last = traceback.extract_tb(exc_tb)[-1] if exc_tb else None

        # Causa raiz (se houver)
        root_exc = exc_value
        while hasattr(root_exc, "__cause__") and root_exc.__cause__:
            root_exc = root_exc.__cause__

        error_info = {
            "tipo": exc_type.__name__,
            "mensagem": str(exc_value),
            "local_erro": {
                "arquivo": os.path.basename(tb_last.filename) if tb_last else None,  # <-- só o nome do arquivo!
                "linha": tb_last.lineno if tb_last else None,
                "funcao": tb_last.name if tb_last else None,
                "codigo": tb_last.line if tb_last else None,
            },
            "causa_raiz": str(root_exc) if root_exc is not exc_value else None,
        }
        return error_info

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "id_execucao": self.id_execucao,
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nivel": record.levelname,
            "mensagem": record.getMessage(),
            "funcao": getattr(record, "funcao_real", record.funcName),  # prioriza funcao_real
            "linha": record.lineno,
        }

        # Captura automaticamente qualquer campo extra
        for key, value in record.__dict__.items():
            if key not in self._campos_padrao:
                log_data[key] = value

        # Estrutura erro detalhado e enxuto
        if record.exc_info:
            log_data["erro"] = self._extract_error_info(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False, indent=4)