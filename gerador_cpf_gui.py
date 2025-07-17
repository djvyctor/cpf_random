import tkinter as tk
from brutils import generate_cpf

def gerar_cpfs():
    try:
        qtd = int(entry.get())
        cpfs = set()
        while len(cpfs) < qtd:
            cpfs.add(generate_cpf())

        resultado.delete('1.0', tk.END)
        for cpf in cpfs:
            resultado.insert(tk.END, cpf + '\n')
    except ValueError:
        resultado.delete('1.0', tk.END)
        resultado.insert(tk.END, "Digite um número válido!")

janela = tk.Tk()
janela.title("Gerador de CPF Válido")
janela.geometry("300x350")
janela.resizable(False, False)

tk.Label(janela, text="Quantos CPFs você quer gerar?").pack(pady=5)
entry = tk.Entry(janela)
entry.pack(pady=5)

tk.Button(janela, text="Gerar", command=gerar_cpfs).pack(pady=5)

resultado = tk.Text(janela, height=15, width=30)
resultado.pack(pady=10)

janela.mainloop()
