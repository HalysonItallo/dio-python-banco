from abc import ABC, abstractmethod
from datetime import date


class OperationError(Exception):
    pass


class LimitExceeded(Exception):
    pass


class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    @property
    def transacoes(self) -> list:
        return self._transacoes


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def __str__(self) -> str:
        return "Deposito"

    def registrar(self, conta):
        foi_depositado = conta.depositar(self.valor)
        if not foi_depositado:
            raise OperationError("\nValor não pode ser depositado\n")


class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor
        self._qtd_saques: int = 0
        self._LIMITE_SAQUE: int = 3

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta):
        if self._qtd_saques < self._LIMITE_SAQUE:
            foi_sacado = conta.sacar(self.valor)
            if foi_sacado:
                self._qtd_saques += 1
            else:
                raise OperationError("\nValor não pode ser sacado\n")
        else:
            raise LimitExceeded(
                f"\nQuantidade limite de {self._LIMITE_SAQUE} saques atingidos\n"
            )

    def __str__(self) -> str:
        return "Saque"


class Conta:
    def __init__(
        self,
        saldo: float,
        numero: int,
        agencia: str,
        cliente,
        historico,
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
        cliente,
        historico,
    ):
        return cls(0.0, numero, agencia, cliente, historico)

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def historico(self) -> int:
        return self._historico

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


class PessoaFisica:
    def __init__(self, cpf: str, nome: str, data_nascimento: date) -> None:
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

        super().__init__()


class Cliente(PessoaFisica):
    def __init__(self, endereco: str, *args, **kwargs) -> None:
        self._endereco = endereco
        self._contas = []
        super().__init__(*args, **kwargs)

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def contas(self) -> int:
        return len(self._contas)

    def realizar_trasacao(self, numero_conta: int, transacao):
        conta = self._pegar_conta_pelo_numero(numero_conta)
        if conta:
            transacao.registrar(conta)
            conta.historico.adicionar_transacao(transacao)

    def adicionar_conta(self, conta) -> None:
        self._contas.append(conta)

    def visualizar_extrato(self, numero_conta: int) -> None:
        conta = self._pegar_conta_pelo_numero(numero_conta)

        print("\n************Extrato************")
        if len(conta.historico.transacoes) == 0:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in conta.historico.transacoes:
                print(f"Operação de {str(transacao)} no valor de R$ {transacao.valor}")
        print(f"\nSeu saldo atual R$ {conta.saldo}\n")

    def _pegar_conta_pelo_numero(self, numero_conta: int):
        for conta in self._contas:
            if conta.numero == numero_conta:
                return conta

        raise OperationError(
            f"Não foi possível encontrar a conta de número {numero_conta}."
        )


class Main:
    def __init__(self) -> None:
        self._cliente = None

    def cadastrar_cliente(self):
        nome = input("Digite seu nome\n>> ")
        cpf = input("Digite seu cpf. OBS: somente número.\n>> ")

        if len(cpf) != 11:
            raise OperationError("O CPF está inválido.")

        data_nascimento = input("Digite sua data de nascimento. Ex: dd/mm/yyyy\n>> ")

        if not (
            len(data_nascimento.split("/")[0]) == 2
            and len(data_nascimento.split("/")[1]) == 2
            and len(data_nascimento.split("/")[2]) == 4
        ):
            raise OperationError("A data de nascimento está inválida.")

        logradouro = input("Digite seu logradouro.\n>> ")
        bairro = input("Digite seu bairro.\n>> ")
        cidade = input("Digite sua cidade.\n>> ")
        sigla_estado = input("Digite a sigla do seu estado. Ex: SP\n>> ")

        usuario = {
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "endereco": f"{logradouro} - {bairro} - {cidade}/{sigla_estado}",
        }

        cliente = Cliente(**usuario)
        self._cliente = cliente

        print(f"Novo usuário com o cpf {cliente.cpf} foi cadastrado sucesso!!!")

    def cadastrar_conta_bancaria(self):
        historico = Historico()

        conta = {
            "numero": self._cliente.contas + 1,
            "agencia": "0001",
            "cliente": self._cliente,
            "historico": historico,
        }

        conta = Conta.nova_conta(**conta)

        self._cliente.adicionar_conta(conta)

        print(f"Conta com o número {self._cliente.contas} criada com sucesso!!!")

    def run(self):
        print("************Bem vindo ao banco************")
        menu = (
            "Selecione qual a operação desejada?\n"
            "1 - Saque\n"
            "2 - Deposito\n"
            "3 - Extrato\n"
            "4 - Criar usuário\n"
            "5 - Criar conta bancária\n"
            "6 - Sair\n"
            ">> "
        )
        try:
            operacao = int(input(menu))
        except ValueError:
            print("\nO valor da operação dever ser um número inteiro!!!\n")
            operacao = int(input(menu))

        while operacao != 6:
            match operacao:
                case 1:
                    try:
                        if self._cliente is not None:
                            valor = float(input("Qual o valor à sacar?\n>> "))
                            numero_conta = int(input("Qual o número da conta? "))
                            sacar = Saque(valor)
                            self._cliente.realizar_trasacao(numero_conta, sacar)
                            print("\nValor sacado com sucesso !!!\n")
                        else:
                            raise OperationError("\nPrecisa de um usuário cadastrado\n")
                    except OperationError as e:
                        print(str(e))
                    except ValueError:
                        print("\nO valor de saque dever ser um número inteiro!!!\n")
                    except LimitExceeded as error:
                        print(str(error))
                case 2:
                    try:
                        if self._cliente is not None:
                            valor = float(input("Qual o valor à depositar?\n>> "))
                            numero_conta = int(input("Qual o número da conta? "))
                            depositar = Deposito(valor)
                            self._cliente.realizar_trasacao(numero_conta, depositar)
                            print("\nSeu depositado com sucesso\n")

                        else:
                            raise OperationError("\nPrecisa de um usuário cadastrado\n")
                    except OperationError as e:
                        print(str(e))
                    except ValueError:
                        print("\nO valor de deposito dever ser um número inteiro!!!\n")
                case 3:
                    try:
                        if self._cliente is not None:
                            numero_conta = int(input("Qual o número da conta?\n"))
                            self._cliente.visualizar_extrato(numero_conta)
                        else:
                            raise OperationError("\nPrecisa de um usuário cadastrado\n")
                    except OperationError as e:
                        print(str(e))
                case 4:
                    try:
                        self.cadastrar_cliente()
                    except OperationError as e:
                        print(str(e))
                case 5:
                    try:
                        if self._cliente is not None:
                            self.cadastrar_conta_bancaria()
                        else:
                            raise OperationError("\nPrecisa de um usuário cadastrado\n")
                    except OperationError as e:
                        print(str(e))
                case 6:
                    break
                case _:
                    print("Operação inválida")

            try:
                operacao = int(input(menu))
            except ValueError:
                print("\nO valor da operação dever ser um número inteiro\n")


if __name__ == "__main__":
    main = Main()
    main.run()
