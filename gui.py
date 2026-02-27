import customtkinter as ctk
from tkinter import messagebox, StringVar
import database

class InterfaceCadastro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Cadastro - Biometria")
        # Aumentamos a altura da janela para caber as novas labels
        self.geometry("400x650")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.criar_variaveis()
        self.criar_widgets()

    def criar_variaveis(self):
        """Cria as variáveis que vão monitorar a digitação para aplicar as máscaras."""
        self.var_nome = StringVar()
        self.var_data_nasc = StringVar()
        self.var_contato = StringVar()
        self.var_data_bio = StringVar()
        self.var_hora_bio = StringVar()

        # Atrela as funções de máscara às variáveis
        self.var_data_nasc.trace_add("write", lambda *args: self.mascara_data(self.var_data_nasc))
        self.var_data_bio.trace_add("write", lambda *args: self.mascara_data(self.var_data_bio))
        self.var_hora_bio.trace_add("write", lambda *args: self.mascara_hora(self.var_hora_bio))
        self.var_contato.trace_add("write", lambda *args: self.mascara_telefone(self.var_contato))

    def criar_widgets(self):
        """Desenha os elementos na tela com labels explicativas."""
        ctk.CTkLabel(self, text="Novo Cadastro", font=("Roboto", 24, "bold")).pack(pady=(20, 15))

        # --- Campo: Nome Completo ---
        # anchor="w" alinha o texto à esquerda. padx=50 alinha perfeitamente com a caixa de 300px
        ctk.CTkLabel(self, text="NOME COMPLETO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        # pady=(0, 15) significa 0 de espaço em cima (para ficar colado na label) e 15 embaixo
        ctk.CTkEntry(self, textvariable=self.var_nome, width=300).pack(pady=(0, 15))

        # --- Campo: Data de Nascimento ---
        ctk.CTkLabel(self, text="DATA DE NASCIMENTO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        ctk.CTkEntry(self, textvariable=self.var_data_nasc, placeholder_text="DD/MM/YYYY", width=300).pack(pady=(0, 15))

        # --- Campo: Contato ---
        ctk.CTkLabel(self, text="NÚMERO PARA CONTATO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        ctk.CTkEntry(self, textvariable=self.var_contato, placeholder_text="(DD) 9XXXX-XXXX", width=300).pack(pady=(0, 15))

        # --- Campo: Data da Biometria ---
        ctk.CTkLabel(self, text="DATA DA BIOMETRIA", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        ctk.CTkEntry(self, textvariable=self.var_data_bio, placeholder_text="DD/MM/YYYY", width=300).pack(pady=(0, 15))

        # --- Campo: Horário da Biometria ---
        ctk.CTkLabel(self, text="HORÁRIO DA BIOMETRIA", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        ctk.CTkEntry(self, textvariable=self.var_hora_bio, placeholder_text="HH:MM", width=300).pack(pady=(0, 20))

        # --- Botão Salvar ---
        ctk.CTkButton(self, text="Cadastrar", command=self.processar_salvamento, width=300, fg_color="green", hover_color="darkgreen").pack(pady=10)

    # --- Funções de Máscara ---
    def mascara_data(self, var):
        texto = ''.join(filter(str.isdigit, var.get()))
        if len(texto) > 2: texto = texto[:2] + '/' + texto[2:]
        if len(texto) > 5: texto = texto[:5] + '/' + texto[5:]
        var.set(texto[:10])

    def mascara_hora(self, var):
        texto = ''.join(filter(str.isdigit, var.get()))
        if len(texto) > 2: texto = texto[:2] + ':' + texto[2:]
        var.set(texto[:5])

    def mascara_telefone(self, var):
        texto = ''.join(filter(str.isdigit, var.get()))
        formatado = ""
        if len(texto) > 0: formatado += f"({texto[:2]}"
        if len(texto) > 2: formatado += f") {texto[2:7]}"
        if len(texto) > 7: formatado += f"-{texto[7:11]}"
        var.set(formatado)

    # --- Lógica de Salvamento ---
    def processar_salvamento(self):
        nome = self.var_nome.get()
        data_nasc = self.var_data_nasc.get()
        contato = self.var_contato.get()
        data_bio = self.var_data_bio.get()
        hora_bio = self.var_hora_bio.get()

        if not nome or not data_nasc:
            messagebox.showwarning("Aviso", "Os campos Nome e Data de Nascimento são obrigatórios!")
            return

        try:
            database.salvar_cadastro(nome, data_nasc, contato, data_bio, hora_bio)
            messagebox.showinfo("Sucesso", f"Cadastro de {nome} salvo com sucesso!")
            
            # Limpa os campos após salvar
            for var in [self.var_nome, self.var_data_nasc, self.var_contato, self.var_data_bio, self.var_hora_bio]:
                var.set("")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar:\n{e}")