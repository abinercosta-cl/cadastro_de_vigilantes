from database import inicializar_banco
from gui import InterfaceCadastro

def iniciar_aplicativo():
    # 1. Garante que o banco de dados e as tabelas existam
    print("Inicializando banco de dados local...")
    inicializar_banco()
    
    # 2. Inicializa e roda a interface gráfica
    print("Iniciando a interface gráfica...")
    app = InterfaceCadastro()
    app.mainloop()

if __name__ == "__main__":
    iniciar_aplicativo()