import logging
import json
import sys
from pytest_cases import parametrize_with_cases
try:   
    from logs_library.formatter import JsonLogFormatter
except ImportError:
    from .logs_library.formatter import JsonLogFormatter


def case_info_log():
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Mensagem de info",
        args=(),
        exc_info=None
    )
    return record, "Mensagem de info", "INFO"


def case_warning_log():
    record = logging.LogRecord(
        name="test_logger",
        level=logging.WARNING,
        pathname=__file__,
        lineno=20,
        msg="Mensagem de warning",
        args=(),
        exc_info=None
    )
    return record, "Mensagem de warning", "WARNING"


def case_extra_fields():
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=30,
        msg="Com extra",
        args=(),
        exc_info=None
    )
    record.custom_field = "valor_extra"
    return record, "Com extra", "INFO"


def case_exception_log():
    try:
        1 / 0
    except Exception:
        exc_info = sys.exc_info()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.ERROR,
        pathname=__file__,
        lineno=40,
        msg="Erro ocorreu",
        args=(),
        exc_info=exc_info
    )
    return record, "Erro ocorreu", "ERROR"


@parametrize_with_cases("record,expected_msg,expected_level", cases=".")
def test_json_log_formatter(record, expected_msg, expected_level):
    formatter = JsonLogFormatter(id_execucao="123")
    output = formatter.format(record)
    data = json.loads(output)

    assert data["id_execucao"] == "123"
    assert data["mensagem"] == expected_msg
    assert data["nivel"] == expected_level
    assert data["funcao"] == record.funcName
    assert data["linha"] == record.lineno
    assert "data_hora" in data

    # Testa campo extra se existir
    if hasattr(record, "custom_field"):
        assert data["custom_field"] == "valor_extra"

    # Testa erro se existir
    if record.exc_info:
        assert "erro" in data
        assert data["erro"]["tipo"] == "ZeroDivisionError"
        assert "traceback" in data["erro"]
