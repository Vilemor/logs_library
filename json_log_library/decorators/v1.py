import time
import functools
from typing import Callable, Any
from .base import BaseLogDecorator


class LogExecucaoV1(BaseLogDecorator):

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            inicio = time.perf_counter()

            self.logger.info(
                f"Iniciando execução da função {func.__name__}"
            )

            try:
                resultado = func(*args, **kwargs)

                tempo_execucao = round(time.perf_counter() - inicio, 6)

                self.logger.info(
                    f"Função {func.__name__} executada com sucesso",
                    extra={"tempo_execucao": tempo_execucao}
                )

                return resultado

            except Exception:
                tempo_execucao = round(time.perf_counter() - inicio, 6)

                self.logger.error(
                    f"Erro ao executar função {func.__name__}",
                    extra={"tempo_execucao": tempo_execucao},
                    exc_info=True
                )

                raise

        return wrapper