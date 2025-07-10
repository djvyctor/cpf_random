from brutils import is_valid_cpf
from faker import Faker

fake = Faker('pt_BR')

def linha():
    print("-" * 60)

def gerar_cpf():
    cpf = fake.cpf()
    print(f"CPF: {cpf}")

def verificar_cpf():
    cpf = input("Digite o CPF para verificar: \n")
    if is_valid_cpf(cpf):
        print("CPF validado!")
    else:
        print("CPF inválido!")

while True:
    linha()
    opcao = input("Digite (1) para gerar CPF, ou (2) para verificar CPF: \n")
    linha()
    if opcao == "1":
        gerar_cpf()
    elif opcao == "2":
        verificar_cpf()
    else:
        print("Opção inválida")
        break