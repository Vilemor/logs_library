import pytest
from unittest.mock import patch, MagicMock
try:
    from logs_library.decorator import log_json
except ImportError:
    from .logs_library.decorator import log_json


# Caso 1: Mensagem customizada
def case_custom_message():
    return {
        "mensagem": "Minha mensagem customizada",
        "a": 2,
        "b": 3,
        "expected_msg": "Minha mensagem customizada"
    }


# Caso 2: Mensagem padrão
def case_default_message():
    return {
        "mensagem": None,
        "a": 5,
        "b": 7,
        "expected_msg": "Chamada da função soma"
    }


# Caso 3: Exceção na função
def case_exception():
    return {
        "mensagem": None,
        "a": 1,
        "b": 0,
        "raises": ZeroDivisionError
    }


@pytest.mark.parametrize(
    "case_func",
    [case_custom_message, case_default_message]
)
def test_log_json_success(case_func):
    params = case_func()
    mensagem = params["mensagem"]
    a = params["a"]
    b = params["b"]
    expected_msg = params["expected_msg"]

    with patch(
        "logs_library.decorator.configurar_logger"
    ) as mock_config_logger:
        mock_logger = MagicMock()
        mock_config_logger.return_value = mock_logger

        @log_json(mensagem=mensagem)
        def soma(x, y):
            return x + y

        result = soma(a, b)
        assert result == a + b

        # Verifica se o logger foi chamado com a mensagem correta
        mock_logger.info.assert_any_call(
            expected_msg,
            extra={
                "input_args": (a, b),
                "input_kwargs": {}
            }
        )
        mock_logger.info.assert_any_call(
            "Retorno da função soma",
            extra={"retorno": a + b}
        )


@pytest.mark.parametrize("case_func", [case_exception])
def test_log_json_exception(case_func):
    params = case_func()
    mensagem = params["mensagem"]
    a = params["a"]
    b = params["b"]

    with patch(
        "logs_library.decorator.configurar_logger"
    ) as mock_config_logger:
        mock_logger = MagicMock()
        mock_config_logger.return_value = mock_logger

        @log_json(mensagem=mensagem)
        def divide(x, y):
            return x / y

        with pytest.raises(ZeroDivisionError):
            divide(a, b)

        # Verifica se o logger registrou a exceção
        mock_logger.exception.assert_called_with(
            "Exceção capturada em divide"
        )
