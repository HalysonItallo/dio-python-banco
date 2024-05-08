from .transacao import Transacao


class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(transacao)

    @property
    def transacoes(self) -> list[Transacao]:
        return self._transacoes
