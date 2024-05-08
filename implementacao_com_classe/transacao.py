from abc import ABC, abstractmethod

from .conta import Conta


class Transacao(ABC):
    @abstractmethod
    def registrar(conta: Conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def __str__() -> str:
        return "Deposito"


class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def __str__() -> str:
        return "Saque"
