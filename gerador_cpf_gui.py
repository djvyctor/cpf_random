import tkinter as tk
from brutils import generate_cpf

def gerar_cpfs():
    try:
        qtd = int(entry.get())
        if qtd <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        if qtd > 1000:
            resultado.delete('1.0', tk.END)
            resultado.insert(tk.END, "Limite máximo: 1000 CPFs.")
            return

        cpfs = set()
        while len(cpfs) < qtd:
            cpfs.add(generate_cpf())

        resultado.delete('1.0', tk.END)
        for cpf in sorted(cpfs):
            resultado.insert(tk.END, cpf + '\n')

    except ValueError:
        resultado.delete('1.0', tk.END)
        resultado.insert(tk.END, "Digite um número válido acima de 0.")

def copiar_cpfs():
    cpfs_texto = resultado.get("1.0", tk.END).strip()
    if cpfs_texto:
        janela.clipboard_clear()
        janela.clipboard_append(cpfs_texto)
        resultado.insert(tk.END, "\nCPFs copiados.")

janela = tk.Tk()
janela.title("Gerador de CPF Válido")
janela.geometry("320x400")
janela.resizable(False, False)

tk.Label(janela, text="Quantos CPFs você quer gerar?").pack(pady=5)
entry = tk.Entry(janela)
entry.pack(pady=5)

tk.Button(janela, text="Gerar", command=gerar_cpfs).pack(pady=5)

resultado = tk.Text(janela, height=15, width=35)
resultado.pack(pady=10)

tk.Button(janela, text="Copiar", command=copiar_cpfs).pack(pady=5)

janela.mainloop()
