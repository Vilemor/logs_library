from abc import ABC, abstractmethod
from typing import Callable, Any
import logging


class BaseLogDecorator(ABC):
    """Classe base para decorators versionados."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    @abstractmethod
    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        ...
