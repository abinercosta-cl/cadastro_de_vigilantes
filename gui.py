import customtkinter as ctk
from tkinter import messagebox, StringVar, filedialog
import database
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import os

class JanelaRelatorio(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Relatório de Biometrias")
        self.geometry("500x750") 
        self.resizable(False, False)
        # Mantém a janela no topo inicialmente
        self.attributes("-topmost", True)
        
        self.var_data_export = StringVar()
        
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        ctk.CTkLabel(self, text="Novo Cadastro", font=("Roboto", 24, "bold")).pack(pady=(20, 15))

        ctk.CTkLabel(self, text="NOME COMPLETO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        self.entry_nome = ctk.CTkEntry(self, textvariable=self.var_nome, width=300)
        self.entry_nome.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="DATA DE NASCIMENTO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        self.entry_data_nasc = ctk.CTkEntry(self, textvariable=self.var_data_nasc, placeholder_text="DD/MM/YYYY", width=300)
        self.entry_data_nasc.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="NÚMERO PARA CONTATO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        self.entry_contato = ctk.CTkEntry(self, textvariable=self.var_contato, placeholder_text="(DD) 9XXXX-XXXX", width=300)
        self.entry_contato.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="DATA DA BIOMETRIA", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        self.entry_data_bio = ctk.CTkEntry(self, textvariable=self.var_data_bio, placeholder_text="DD/MM/YYYY", width=300)
        self.entry_data_bio.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="HORÁRIO DA BIOMETRIA", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        self.entry_hora_bio = ctk.CTkEntry(self, textvariable=self.var_hora_bio, placeholder_text="HH:MM", width=300)
        self.entry_hora_bio.pack(pady=(0, 20))

        ctk.CTkButton(self, text="Cadastrar", command=self.processar_salvamento, width=300, fg_color="green", hover_color="darkgreen").pack(pady=5)
        ctk.CTkButton(self, text="Limpar Campos", command=self.limpar_campos, width=300, fg_color="#555555", hover_color="#333333").pack(pady=5)
        ctk.CTkButton(self, text="Ver Relatórios", command=self.abrir_relatorios, width=300, fg_color="#1f538d", hover_color="#14375e").pack(pady=10)

        self.var_data_nasc.trace_add("write", lambda *args: self.mascara_data(self.var_data_nasc, self.entry_data_nasc))
        self.var_data_bio.trace_add("write", lambda *args: self.mascara_data(self.var_data_bio, self.entry_data_bio))
        self.var_hora_bio.trace_add("write", lambda *args: self.mascara_hora(self.var_hora_bio, self.entry_hora_bio))
        self.var_contato.trace_add("write", lambda *args: self.mascara_telefone(self.var_contato, self.entry_contato))
    def mascara_data(self, var, widget):
        texto = ''.join(filter(str.isdigit, var.get()))[:8]
        formatado = ""
        if len(texto) > 0: formatado += texto[:2]
        if len(texto) > 2: formatado += '/' + texto[2:4]
        if len(texto) > 4: formatado += '/' + texto[4:]
        
        var.set(formatado)
        widget.after(1, lambda: widget.icursor("end"))

    def carregar_dados(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        mes_selecionado = self.combo_mes.get()
        ano_selecionado = self.combo_ano.get()
        
        resultados = database.buscar_por_mes_ano(mes_selecionado, ano_selecionado)

        if not resultados:
            ctk.CTkLabel(self.scroll_frame, text="Nenhum cadastro encontrado para este período.", text_color="gray").pack(pady=20)
            return

        for linha in resultados:
            id_cad, nome, data_nasc, contato, data_bio, hora_bio = linha
            
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
            card.pack(pady=5, padx=5, fill="x")
            
            texto_card = f"Nome: {nome} | Contato: {contato}\nData Biometria: {data_bio} às {hora_bio}"
            ctk.CTkLabel(card, text=texto_card, font=("Roboto", 13), justify="left").pack(pady=10, padx=10, anchor="w")

    # --- LÓGICA CORRIGIDA PARA A JANELA DE SALVAR ---
    def gerar_excel(self):
        data_escolhida = self.var_data_export.get()
        
        if len(data_escolhida) != 10:
            messagebox.showwarning("Aviso", "Digite uma data válida completa (DD/MM/YYYY) para exportar.")
            return
            
        resultados = database.buscar_por_data_exata(data_escolhida)
        
        if not resultados:
            messagebox.showinfo("Sem Agendamentos", f"Nenhuma biometria marcada para {data_escolhida}.")
            return
            
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Agenda Biometria"
            
            headers = ["ID", "Nome Completo", "Data de Nasc.", "Contato", "Data Biometria", "Horário"]
            ws.append(headers)
            
            fill_header = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
            font_header = Font(color="FFFFFF", bold=True)
            
            for col in range(1, len(headers) + 1):
                celula = ws.cell(row=1, column=col)
                celula.fill = fill_header
                celula.font = font_header
                celula.alignment = Alignment(horizontal="center")
                
            for linha in resultados:
                ws.append(linha)
                
            ws.column_dimensions["A"].width = 5   
            ws.column_dimensions["B"].width = 35  
            ws.column_dimensions["C"].width = 15  
            ws.column_dimensions["D"].width = 20  
            ws.column_dimensions["E"].width = 15  
            ws.column_dimensions["F"].width = 10  
            
            for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=6):
                for cell in row:
                    if cell.column != 2: 
                        cell.alignment = Alignment(horizontal="center")
            
            nome_sugerido = f"Agenda_Biometria_{data_escolhida.replace('/', '-')}.xlsx"
            
            # 1. Tira o bloqueio do topmost antes de abrir a janela
            self.attributes("-topmost", False)
            
            # 2. Abre a janela de salvar usando parent=self
            caminho_arquivo = filedialog.asksaveasfilename(
                parent=self,
                defaultextension=".xlsx",
                initialfile=nome_sugerido,
                title="Salvar Planilha Como",
                filetypes=[("Planilha do Excel", "*.xlsx"), ("Todos os Arquivos", "*.*")]
            )
            
            # 3. Devolve o bloqueio do topmost logo que a janela de salvar fechar
            self.attributes("-topmost", True)
            
            if not caminho_arquivo:
                return 
                
            wb.save(caminho_arquivo)
            messagebox.showinfo("Sucesso", f"Planilha salva com sucesso em:\n{caminho_arquivo}")
            
        except Exception as e:
            # Em caso de erro, também precisamos garantir que o topmost volte ao normal
            self.attributes("-topmost", True)
            messagebox.showerror("Erro", f"Erro ao gerar Excel:\n{e}")


class InterfaceCadastro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Cadastro - Biometria")
        self.geometry("400x750") 
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

    def criar_widgets(self):
        ctk.CTkLabel(self, text="Novo Cadastro", font=("Roboto", 24, "bold")).pack(pady=(20, 15))

        ctk.CTkLabel(self, text="NOME COMPLETO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        self.entry_nome = ctk.CTkEntry(self, textvariable=self.var_nome, width=300)
        self.entry_nome.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="DATA DE NASCIMENTO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        self.entry_data_nasc = ctk.CTkEntry(self, textvariable=self.var_data_nasc, placeholder_text="DD/MM/YYYY", width=300)
        self.entry_data_nasc.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="NÚMERO PARA CONTATO", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        self.entry_contato = ctk.CTkEntry(self, textvariable=self.var_contato, placeholder_text="(DD) 9XXXX-XXXX", width=300)
        self.entry_contato.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="DATA DA BIOMETRIA", font=("Roboto", 12, "bold")).pack(anchor="w", padx=50)
        self.entry_data_bio = ctk.CTkEntry(self, textvariable=self.var_data_bio, placeholder_text="DD/MM/YYYY", width=300)
        self.entry