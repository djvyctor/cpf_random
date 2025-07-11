from brutils import generate_cpf

def gerar_cpfs_validos(qtd, arquivo="cpfs_validos.txt"):
    cpfs_gerados = set()
    with open(arquivo, "a") as f:
        while len(cpfs_gerados) < qtd:
            cpf = generate_cpf()
            if cpf not in cpfs_gerados:
                cpfs_gerados.add(cpf)
                f.write(cpf + "\n")
                print(f"CPF válido gerado: {cpf}")

    print(f"\n{qtd} CPFs válidos gerados e salvos em '{arquivo}'")

gerar_cpfs_validos(1)