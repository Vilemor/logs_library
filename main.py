from logs_library.decorator import log_json

@log_json(mensagem="Executando soma")
def soma(a, b):
    return a + b

@log_json(mensagem="Executando divisão")
def divide(a, b):
    return a / b

if __name__ == "__main__":
    soma(2, 3)  # O log_json já registra a mensagem e o resultado
    try:
        divide(4, 0)  # O log_json já registra a exceção
    except ZeroDivisionError:
        pass  # O erro já foi logado pelo decorator