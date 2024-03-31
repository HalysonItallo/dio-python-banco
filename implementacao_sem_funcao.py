def main():
    saldo: float = 0.0
    extrato: str = ""
    qtd_saques: int = 0
    LIMITE_SAQUE: int = 3

    print("************Bem vindo ao banco************")
    menu = (
        "Selecione qual a operação desejada?\n"
        "1 - Saque\n"
        "2 - Deposito\n"
        "3 - Extrato\n"
        "4 - Sair\n"
        ">> "
    )
    try:
        operacao = int(input(menu))
    except ValueError:
        print("\nO valor da operação dever ser um número inteiro!!!\n")
        operacao = int(input(menu))

    while operacao != 4:
        match operacao:
            case 1:
                if qtd_saques < LIMITE_SAQUE:
                    try:
                        saque = float(input("Qual o valor à sacar?\n>> "))

                        if saque < 0:
                            print("\n Valor de saque não pode ser negativo \n")

                        elif saque > 500:
                            print(
                                "\n O valor do saque não pode ser maior que R$500,00. \n"
                            )

                        elif (saldo - saque) < 0:
                            print("\n Você não tem saldo suficiente \n")
                        else:
                            saldo -= saque

                            extrato += "Operação de saque no valor de R$ {saldo:.2f}\n"

                            print(f"\nSeu novo saldo: {saldo:.2f}\n")
                            qtd_saques += 1
                    except ValueError:
                        print("\nO valor de saque dever ser um número inteiro!!!\n")
                else:
                    print(f"\nQuantidade limite de {LIMITE_SAQUE} saques atingidos\n")
            case 2:
                try:
                    deposito = float(input("Qual o valor à depositar?\n>> "))

                    if deposito < 0:
                        print("\n Valor de deposito não pode ser negativo \n")
                    else:
                        saldo += deposito

                        extrato += "Operação de deposito no valor de R$ {saldo:.2f}\n"

                        print(f"\nSeu novo saldo: {saldo:.2f}\n")
                except ValueError:
                    print("\nO valor de deposito dever ser um número inteiro!!!\n")
            case 3:
                print("\n************Extrato************")
                if extrato == "":
                    print("Não foram realizadas movimentações.")
                else:
                    print(extrato, end="\n\n")
            case 4:
                break
            case _:
                print("Operação inválida")

        try:
            operacao = int(input(menu))
        except ValueError:
            print("O valor da operação dever ser um número inteiro")


if __name__ == "__main__":
    main()
