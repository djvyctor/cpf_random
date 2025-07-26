import customtkinter as ctk
from brutils import generate_cpf
import threading
import time
from tkinter import messagebox
import pyperclip

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GeradorCPFApp:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("🆔 Gerador de CPF Válido - Versão Moderna")
        self.janela.geometry("500x650")
        self.janela.resizable(False, False)

        self.centralizar_janela()

        try:
            self.janela.iconbitmap("icon.ico")
        except:
            pass

        self.criar_interface()

    def centralizar_janela(self):
        self.janela.update_idletasks()
        largura = self.janela.winfo_width()
        altura = self.janela.winfo_height()
        pos_x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        pos_y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def criar_interface(self):
        self.frame_principal = ctk.CTkFrame(self.janela, corner_radius=15)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="🆔 Gerador de CPF Válido",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.titulo.pack(pady=(30, 10))

        self.subtitulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gere CPFs válidos para testes e desenvolvimento",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        self.subtitulo.pack(pady=(0, 30))

        self.frame_entrada = ctk.CTkFrame(self.frame_principal, corner_radius=10)
        self.frame_entrada.pack(fill="x", padx=30, pady=(0, 20))

        self.label_quantidade = ctk.CTkLabel(
            self.frame_entrada,
            text="📊 Quantos CPFs você deseja gerar?",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.label_quantidade.pack(pady=(20, 10))

        self.entry_quantidade = ctk.CTkEntry(
            self.frame_entrada,
            placeholder_text="Digite um número (máx: 1000)",
            font=ctk.CTkFont(size=14),
            height=40,
            width=300
        )
        self.entry_quantidade.pack(pady=(0, 10))

        self.frame_botoes = ctk.CTkFrame(self.frame_entrada, fg_color="transparent")
        self.frame_botoes.pack(pady=(10, 20))

        self.botao_gerar = ctk.CTkButton(
            self.frame_botoes,
            text="🎲 Gerar CPFs",
            command=self.gerar_cpfs_thread,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=150,
            corner_radius=10
        )
        self.botao_gerar.pack(side="left", padx=(0, 10))

        self.botao_limpar = ctk.CTkButton(
            self.frame_botoes,
            text="🗑️ Limpar",
            command=self.limpar_resultado,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=120,
            corner_radius=10,
            fg_color="gray40",
            hover_color="gray30"
        )
        self.botao_limpar.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(
            self.frame_principal,
            width=400,
            height=8
        )
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)

        self.label_status = ctk.CTkLabel(
            self.frame_principal,
            text="Pronto para gerar CPFs",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.label_status.pack(pady=(0, 10))

        self.frame_resultado = ctk.CTkFrame(self.frame_principal, corner_radius=10)
        self.frame_resultado.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        self.label_resultado = ctk.CTkLabel(
            self.frame_resultado,
            text="📋 CPFs Gerados:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.label_resultado.pack(pady=(20, 10), anchor="w", padx=20)

        self.textbox_resultado = ctk.CTkTextbox(
            self.frame_resultado,
            font=ctk.CTkFont(family="Courier", size=12),
            corner_radius=8,
            height=200
        )
        self.textbox_resultado.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.frame_acoes = ctk.CTkFrame(self.frame_resultado, fg_color="transparent")
        self.frame_acoes.pack(fill="x", padx=20, pady=(0, 20))

        self.botao_copiar = ctk.CTkButton(
            self.frame_acoes,
            text="📋 Copiar Todos",
            command=self.copiar_cpfs,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=140,
            corner_radius=8,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.botao_copiar.pack(side="left", padx=(0, 10))

        self.botao_salvar = ctk.CTkButton(
            self.frame_acoes,
            text="💾 Salvar em Arquivo",
            command=self.salvar_arquivo,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=160,
            corner_radius=8,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.botao_salvar.pack(side="left")

        self.label_contador = ctk.CTkLabel(
            self.frame_acoes,
            text="CPFs: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray60"
        )
        self.label_contador.pack(side="right", padx=(10, 0))

        self.entry_quantidade.bind("<Return>", lambda event: self.gerar_cpfs_thread())

    def gerar_cpfs_thread(self):
        threading.Thread(target=self.gerar_cpfs, daemon=True).start()

    def gerar_cpfs(self):
        try:
            # Validar entrada
            texto_quantidade = self.entry_quantidade.get().strip()
            if not texto_quantidade:
                self.mostrar_erro("Por favor, digite uma quantidade.")
                return

            qtd = int(texto_quantidade)

            if qtd <= 0:
                self.mostrar_erro("A quantidade deve ser maior que zero.")
                return

            if qtd > 1000:
                self.mostrar_erro("Limite máximo: 1000 CPFs por vez.")
                return

            self.botao_gerar.configure(state="disabled", text="⏳ Gerando...")
            self.label_status.configure(text="Gerando CPFs...")
            self.progress_bar.set(0)

            cpfs = set()
            total_gerados = 0

            while len(cpfs) < qtd:
                cpf = generate_cpf()
                if cpf not in cpfs:
                    cpfs.add(cpf)
                    total_gerados += 1

                    progresso = total_gerados / qtd
                    self.progress_bar.set(progresso)
                    self.label_status.configure(text=f"Gerando CPFs... {total_gerados}/{qtd}")

                    if qtd > 50:
                        time.sleep(0.01)

            self.textbox_resultado.delete("1.0", "end")
            cpfs_ordenados = sorted(cpfs)

            for i, cpf in enumerate(cpfs_ordenados):
                self.textbox_resultado.insert("end", f"{i + 1:3d}. {cpf}\n")

            self.label_contador.configure(text=f"CPFs: {len(cpfs)}")

            self.progress_bar.set(1)
            self.label_status.configure(text=f"✅ {len(cpfs)} CPFs gerados com sucesso!")
            self.botao_gerar.configure(state="normal", text="🎲 Gerar CPFs")

        except ValueError:
            self.mostrar_erro("Digite um número válido.")
            self.botao_gerar.configure(state="normal", text="🎲 Gerar CPFs")
            self.progress_bar.set(0)
            self.label_status.configure(text="Erro na geração")
        except Exception as e:
            self.mostrar_erro(f"Erro inesperado: {str(e)}")
            self.botao_gerar.configure(state="normal", text="🎲 Gerar CPFs")
            self.progress_bar.set(0)
            self.label_status.configure(text="Erro na geração")

    def copiar_cpfs(self):
        conteudo = self.textbox_resultado.get("1.0", "end").strip()
        if not conteudo:
            self.mostrar_erro("Nenhum CPF para copiar.")
            return

        try:
            linhas = conteudo.split('\n')
            cpfs = []
            for linha in linhas:
                if linha.strip() and '. ' in linha:
                    cpf = linha.split('. ')[1].strip()
                    cpfs.append(cpf)

            cpfs_texto = '\n'.join(cpfs)
            pyperclip.copy(cpfs_texto)

            self.label_status.configure(text="📋 CPFs copiados para a área de transferência!")

            cor_original = self.botao_copiar.cget("fg_color")
            self.botao_copiar.configure(fg_color="darkgreen")
            self.janela.after(1000, lambda: self.botao_copiar.configure(fg_color=cor_original))

        except Exception as e:
            self.mostrar_erro(f"Erro ao copiar: {str(e)}")

    def salvar_arquivo(self):
        conteudo = self.textbox_resultado.get("1.0", "end").strip()
        if not conteudo:
            self.mostrar_erro("Nenhum CPF para salvar.")
            return

        try:
            from tkinter import filedialog
            arquivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
                title="Salvar CPFs"
            )

            if arquivo:
                linhas = conteudo.split('\n')
                cpfs = []
                for linha in linhas:
                    if linha.strip() and '. ' in linha:
                        cpf = linha.split('. ')[1].strip()
                        cpfs.append(cpf)

                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(cpfs))

                self.label_status.configure(text=f"💾 CPFs salvos em: {arquivo}")

                cor_original = self.botao_salvar.cget("fg_color")
                self.botao_salvar.configure(fg_color="darkorange")
                self.janela.after(1000, lambda: self.botao_salvar.configure(fg_color=cor_original))

        except Exception as e:
            self.mostrar_erro(f"Erro ao salvar: {str(e)}")

    def limpar_resultado(self):
        self.textbox_resultado.delete("1.0", "end")
        self.label_contador.configure(text="CPFs: 0")
        self.progress_bar.set(0)
        self.label_status.configure(text="Resultado limpo")
        self.entry_quantidade.delete(0, "end")

    def mostrar_erro(self, mensagem):
        self.label_status.configure(text=f"❌ {mensagem}")
        messagebox.showerror("Erro", mensagem)

    def executar(self):
        self.janela.mainloop()


try:
    import pyperclip
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    import pyperclip

if __name__ == "__main__":
    app = GeradorCPFApp()
    app.executar()
