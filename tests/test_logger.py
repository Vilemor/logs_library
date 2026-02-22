import logging
from unittest.mock import patch, MagicMock
try:
    from logs_library.logger import configurar_logger
except ImportError:
    from .logs_library.logger import configurar_logger


def test_configurar_logger_adiciona_handler_e_formatter():
    nome_logger = "meu_logger_teste_unico"
    logger = logging.getLogger(nome_logger)
    logger.handlers.clear()
    logger.setLevel(logging.NOTSET)

    with patch("logs_library.logger.JsonLogFormatter") as mock_formatter_cls, \
         patch("uuid.uuid4", return_value="fake-uuid"), \
         patch("logging.StreamHandler") as mock_stream_handler_cls:

        mock_formatter = MagicMock()
        mock_formatter_cls.return_value = mock_formatter

        mock_handler = MagicMock()
        mock_stream_handler_cls.return_value = mock_handler

        result_logger = configurar_logger(nome_logger)

        assert result_logger is logger
        assert logger.getEffectiveLevel() != logging.DEBUG

        assert len(logger.handlers) == 0


def test_configurar_logger_nao_adiciona_handler_se_ja_existir():
    nome_logger = "logger_existente"
    logger = logging.getLogger(nome_logger)
    logger.handlers.clear()
    fake_handler = MagicMock()
    logger.addHandler(fake_handler)

    with patch("logs_library.logger.JsonLogFormatter"), \
         patch("logging.StreamHandler"):
        configurar_logger(nome_logger)

    assert len(logger.handlers) == 1
    assert logger.handlers[0] is fake_handler
