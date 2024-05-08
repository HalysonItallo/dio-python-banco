from datetime import date

from .conta import Conta
from .transacao import Transacao


class PessoaFisica:
    def __init__(self, cpf: str, nome: str, data_nascimento: date) -> None:
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento


class Cliente(PessoaFisica):
    def __init__(self, endereco: str, contas: list[Conta]) -> None:
        self._endereco = endereco
        self._contas = contas

    @property
    def cpf(self) -> str:
        return self.cpf

    def realizar_trasacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta) -> None:
        self._contas.append(conta)
