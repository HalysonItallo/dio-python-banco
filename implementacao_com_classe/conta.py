from typing import Self

from .cliente import Cliente
from .historico import Historico


class Conta:
    def __init__(
        self,
        saldo: float,
        numero: int,
        agencia: str,
        cliente: Cliente,
        historico: Historico,
    ) -> None:
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    @property
    def saldo(self) -> float:
        return self._saldo

    @classmethod
    def nova_conta(
        cls,
        numero: int,
        agencia: str,
        cliente: Cliente,
        historico: Historico,
    ) -> Self:
        return cls(0.0, numero, agencia, cliente, historico)

    def sacar(self, valor: float) -> bool:
        if valor < 0 or valor > 500 or (self._saldo - valor) < 0:
            return False

        self._saldo -= valor

        return True

    def depositar(self, valor: float) -> bool:
        if valor < 0:
            return False

        self._saldo += valor

        return True

    def visualizar_extrato(self) -> None:
        print("\n************Extrato************")
        if len(self._historio.transacoes) == 0:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in self._historio.transacoes:
                print(f"Operação de {str(transacao)} no valor de R$ {transacao.valor}")
        print(f"\nSeu saldo atual R$ {self._saldo}\n")
