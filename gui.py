import customtkinter as ctk
from tkinter import messagebox, StringVar
import database

class JanelaRelatorio(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Relatório de Biometrias")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Garante que a janela fique no topo
        self.attributes("-topmost", True)
        
        self.var_filtro_data = StringVar()
        self.var_filtro_data.trace_add("write", lambda *args: self.mascara_data(self.var_filtro_data))

        self.criar_widgets()
        # Carrega todos os dados logo que a janela abre
        self.carregar_dados()

    def criar_widgets(self):
        # Frame do topo (Filtros)
        frame_topo = ctk.CTkFrame(self)
        frame_topo.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_topo, text="Filtrar por Data da Biometria:", font=("Roboto", 14, "bold")).pack(pady=5)
        
        # Campo de busca e botão lado a lado
        frame_busca = ctk.CTkFrame(frame_topo, fg_color="transparent")
        frame_busca.pack(pady=5)
        
        ctk.CTkEntry(frame_busca, textvariable=self.var_filtro_data, placeholder_text="DD/MM/YYYY", width=200).pack(side="left", padx=10)
        ctk.CTkButton(frame_busca, text="Buscar", command=self.carregar_dados, width=100).pack(side="left")

        # Frame rolável para exibir os resultados (estilo lista/cards)
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Cadastros Encontrados")
        self.scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def mascara_data(self, var):
        texto = ''.join(filter(str.isdigit, var.get()))
        if len(texto) > 2: texto = texto[:2] + '/' + texto[2:]
        if len(texto) > 5: texto = texto[:5] + '/' + texto[5:]
        var.set(texto[:10])

    def carregar_dados(self):
        # Limpa o frame antes de adicionar novos resultados
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        data_filtro = self.var_filtro_data.get()
        resultados = database.buscar_por_data_biometria(data_filtro)

        if not resultados:
            ctk.CTkLabel(self.scroll_frame, text="Nenhum cadastro encontrado para esta data.", text_color="gray").pack(pady=20)
            return

        # Cria um "card" para cada registro encontrado
        for linha in resultados:
            # linha: (id, nome, data_nasc, contato, data_bio, hora_bio)
            id_cad, nome, data_nasc, contato, data_bio, hora_bio = linha
            
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
            card.pack(pady=5, padx=5, fill="x")
            
            # Textos dentro do card
            texto_card = f"Nome: {nome} | Contato: {contato}\nData Biometria: {data_bio} às {hora_bio}"
            
            ctk.CTkLabel(card, text=texto_card, font=("Roboto", 13), justify="left").pack(pady=10, padx=10, anchor="w")


class InterfaceCadastro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Cadastro - Biometria")
        self.geometry("400x720") # Aumentei um pouco para caber o novo botão
        self.resizable(False, False)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.criar_variaveis()
        self.criar_widgets()

    def criar_variaveis(self):
        self.var_nome = StringVar()
        self.var_data_nasc = StringVar()
        self.var_contato = StringVar()
        self.var_data_bio = StringVar()
        self.var_hora_bio = StringVar()

        self.var_data_nasc.trace_add("write", lambda *args: self.mascara_data(self.var_data_nasc))
        self.var_data_bio.trace_add("write", lambda *args: self.mascara_data(self.var_data_bio))
        self.var_hora_bio.trace_add("write", lambda *args: self.mascara_hora(self.var_hora_bio))
        self.var_contato.trace_add("write", lambda *args: self.mascara_telefone(self.var_contato))

    def criar_widgets(self):
        ctk.CTkLabel(self, text="Novo Cadastro", font=("Roboto", 24, "bold")).pack(pady=(20, 15))

        ctk.CTkLabel(self, text="NOME COMPLETO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        ctk.CTkEntry(self, textvariable=self.var_nome, width=300).pack(pady=(0, 15))

        ctk.CTkLabel(self, text="DATA DE NASCIMENTO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        ctk.CTkEntry(self, textvariable=self.var_data_nasc, placeholder_text="DD/MM/YYYY", width=300).pack(pady=(0, 15))

        ctk.CTkLabel(self, text="NÚMERO PARA CONTATO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        ctk.CTkEntry(self, textvariable=self.var_contato, placeholder_text="(DD) 9XXXX-XXXX", width=300).pack(pady=(0, 15))

        ctk.CTkLabel(self, text="DATA DA BIOMETRIA", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        ctk.CTkEntry(self, textvariable=self.var_data_bio, placeholder_text="DD/MM/YYYY", width=300).pack(pady=(0, 15))

        ctk.CTkLabel(self, text="HORÁRIO DA BIOMETRIA", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        ctk.CTkEntry(self, textvariable=self.var_hora_bio, placeholder_text="HH:MM", width=300).pack(pady=(0, 20))

        # Botão Cadastrar
        ctk.CTkButton(self, text="Cadastrar", command=self.processar_salvamento, width=300, fg_color="green", hover_color="darkgreen").pack(pady=5)
        
        # NOVO: Botão para abrir o Relatório
        ctk.CTkButton(self, text="Ver Relatórios", command=self.abrir_relatorios, width=300, fg_color="#1f538d", hover_color="#14375e").pack(pady=10)

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
            
            for var in [self.var_nome, self.var_data_nasc, self.var_contato, self.var_data_bio, self.var_hora_bio]:
                var.set("")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar:\n{e}")

    # Abre a nova janela
    def abrir_relatorios(self):
        JanelaRelatorio(self)