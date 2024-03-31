from typing import TypedDict


class Usuario(TypedDict):
    nome: str
    data_nascimento: str
    cpf: str
    endereco: str


class Conta(TypedDict):
    agencia: str
    numero_conta: int
    cpf_usuario: str


Extrato = list[tuple[str, float]]
Usuarios = list[Usuario]


class OperationError(Exception):
    pass


def sacar(*, saque: float, saldo: float, extrato: Extrato) -> float:
    if saque < 0:
        raise OperationError("\n Valor de saque não pode ser negativo \n")

    if saque > 500:
        raise OperationError("\n O valor do saque não pode ser maior que R$500,00. \n")

    if (saldo - saque) < 0:
        raise OperationError("\n Você não tem saldo suficiente \n")

    saldo -= saque

    extrato.append(
        (
            "Saque",
            saque,
        ),
    )

    return saldo


def depositar(deposito: float, saldo: float, extrato: Extrato, /) -> float:
    if deposito < 0:
        raise OperationError("\n Valor de deposito não pode ser negativo \n")

    saldo += deposito

    extrato.append(
        (
            "Depósito",
            deposito,
        ),
    )

    return saldo


def visualizar_extrato(saldo: float, /, *, extrato: Extrato) -> None:
    print("\n************Extrato************")
    if len(extrato) == 0:
        print("Não foram realizadas movimentações.")
    else:
        for operacao, valor in extrato:
            print(f"Operação de {operacao} no valor de R$ {valor:.2f}")
    print(f"\nSeu saldo atual R$ {saldo}\n")


def se_existe_usuario(usuarios: Usuarios, cpf: str) -> bool:
    for usuario in usuarios:
        if cpf == usuario["cpf"]:
            return True
    return False


def montar_usuario() -> Usuario:
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

    usuario: Usuario = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": f"{logradouro} - {bairro} - {cidade}/{sigla_estado}",
    }

    return usuario


def cadastrar_usuario(usuarios: Usuarios, novo_usuario: Usuario):
    if se_existe_usuario(usuarios, novo_usuario["cpf"]):
        raise OperationError("CPF já cadastrado!!!")

    usuarios.append(novo_usuario)

    print("Novo usuário cadastrado com sucesso!!!")
    print(f"\n - Nome: {novo_usuario["nome"]}")
    print(f" - CPF: {novo_usuario['cpf']}")
    print(f" - Data de nascimento: {novo_usuario["data_nascimento"]}")
    print(f" - Endereço: {novo_usuario["endereco"]}\n")


def cadastrar_conta_bancaria(contas: list[Conta], usuarios: Usuarios):
    cpf = input("Digite o cpf para criar a conta. OBS: somente número.\n>> ")

    if len(cpf) != 11:
        raise OperationError("\nO CPF está inválido.\n")

    if not se_existe_usuario(usuarios, cpf):
        raise OperationError("\nUsuário não cadastrado.\n")

    conta: Conta = {
        "agencia": "0001",
        "numero_conta": len(contas) + 1,
        "cpf_usuario": cpf,
    }

    contas.append(conta)

    print("Conta criada com sucesso!!!")
    print(f"\n - Agência: {conta["agencia"]}")
    print(f" - Número da conta: {conta['numero_conta']}")
    print(f" - CPF do dono da conta: {conta["cpf_usuario"]}\n")


def main():
    saldo: float = 0.0
    extrato: Extrato = []
    qtd_saques: int = 0
    LIMITE_SAQUE: int = 3
    usuarios: Usuarios = []
    contas: list[Conta] = []

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
                if qtd_saques < LIMITE_SAQUE:
                    try:
                        saque = float(input("Qual o valor à sacar?\n>> "))
                        saldo = sacar(saque=saque, saldo=saldo, extrato=extrato)
                        print(f"\nSeu novo saldo: {saldo:.2f}\n")
                        qtd_saques += 1
                    except OperationError as e:
                        print(str(e))
                    except ValueError:
                        print("\nO valor de saque dever ser um número inteiro!!!\n")
                else:
                    print(f"\nQuantidade limite de {LIMITE_SAQUE} saques atingidos\n")
            case 2:
                try:
                    deposito = float(input("Qual o valor à depositar?\n>> "))
                    saldo = depositar(deposito, saldo, extrato)
                    print(f"\nSeu novo saldo: {saldo:.2f}\n")
                except OperationError as e:
                    print(str(e))
                except ValueError:
                    print("\nO valor de deposito dever ser um número inteiro!!!\n")
            case 3:
                visualizar_extrato(saldo, extrato=extrato)
            case 4:
                try:
                    novo_usuario = montar_usuario()
                    cadastrar_usuario(usuarios, novo_usuario)
                except OperationError as e:
                    print(str(e))
            case 5:
                try:
                    cadastrar_conta_bancaria(contas, usuarios)
                except OperationError as e:
                    print(str(e))
            case 6:
                break
            case _:
                print("Operação inválida")

        try:
            operacao = int(input(menu))
        except ValueError:
            print("O valor da operação dever ser um número inteiro")


if __name__ == "__main__":
    main()
