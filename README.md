# 🖥️ Sistema de Cadastro e Agendamento de Biometria

Um aplicativo desktop desenvolvido em Python para gerenciar o cadastro e o agendamento de biometrias. Focado em simplicidade e performace, o sistema utiliza um banco de dados local (dispensando instalações complexas de servidores) e permite a exportação de relatórios diários formatados diretamente para Excel.

---

## ✨ Funcionalidades

- **Interface Moderna:** Construída com CustomTkinter, oferecendo um visual Dark Mode limpo, intuitivo e responsivo.
- **Validação e Máscaras:** Campos de entrada com formatação automática em tempo real para Datas (DD/MM/YYYY), Horas (HH:MM) e Telefones, além de controle rigoroso de cursor para excelente UX.
- **Banco de Dados Portátil:** Utiliza SQLite embutido. O arquivo '.db' é gerado e estruturado automaticamente na primeira execução do software.
- **Filtros de Relátorios:** Busca dinâmica de cadastros no sistema, permitindo filtrar os agendamentos por Mês e Ano.
- **Exportação para Excel:** Geração de Planilhas '.xlsx' já estilizadas (cabeçalhos, larguras de colunas ajustadas) e ordenadas cronologicamente pelo horario de atendimento, prontas para impressão e uso operacional do setor.
- **Reset Simples:** Para zerar o banco de dados, basta deletar o arquivo 'cadastro_biometria.db' com o sistema fechado, e um novo será criado no próximo uso.

---

## 🛠️ Tecnologias Utilizadas

- **[Python 3.x](https://www.python.org/)** - Linguagem base do projeto.
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Biblioteca para a construção da Interface Gráfica (GUI).
- **[SQLite3](https://docs.python.org/3/library/sqlite3.html)** - Banco de dados relacional leve e nativo.
- **[OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)** - Manipulação, formatação e exportação de arquivos nativos do Microsoft Excel.
- **[PyInstaller](https://pyinstaller.org/en/stable/)** - Empacotamento do projeto em um executável (`.exe`) independente para distribuição em ambientes Windows.

---

## 📁 Arquitetura do Projeto

O código foi cuidadosamente modularizado seguindo boas práticas de separação de responsabilidades, facilitando a manutenção e a escalabilidade:

```text
cadastro_de_vigilantes/
├── database.py   # Lida exclusivamente com as queries, inicialização e conexão SQLite
├── gui.py        # Contém a construção da interface gráfica e lógica de interação (frontend)
└── main.py       # Ponto de entrada que inicializa o banco e chama a aplicação

```

## 🚀 Como Executar o Projeto (Ambiente de Desenvolvimento)

Pré-requisitos

Certifique-se de ter o Python 3.x instalado em sua máquina e o Git para clonar o repositório.

1. Clonar o repositório
   Bash

git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
cd SEU_REPOSITORIO

2. Criar ambiente virtual e instalar dependências

Recomenda-se o uso de um ambiente virtual (venv) para isolar os pacotes do projeto.

No Linux / macOS:
Bash

python3 -m venv venv
source venv/bin/activate
pip install customtkinter openpyxl

No Windows:
PowerShell

python -m venv venv
.\venv\Scripts\activate
pip install customtkinter openpyxl

3. Rodar a aplicação

Com o ambiente ativado e as dependências instaladas, basta executar:
Bash

python main.py

## 📦 Como Compilar para Produção (Windows .exe)

Para gerar um arquivo executável único que roda nativamente no Windows sem precisar de nenhuma instalação prévia de Python ou bibliotecas na máquina do usuário final:

    Abra o terminal (PowerShell/CMD) no Windows, dentro da pasta raiz do projeto.

    Certifique-se de ter o PyInstaller instalado executando pip install pyinstaller.

    Execute o comando de compilação:

PowerShell

python -m PyInstaller --noconsole --onefile main.py

    Aguarde a finalização. O executável pronto para uso estará disponível dentro da pasta dist/ gerada no diretório. Basta movê-lo para a máquina desejada ou enviá-lo via nuvem/pendrive.

## 👤 Autor

Abiner Costa

    LinkedIn: [https://www.linkedin.com/in/abiner-costa-b861bb259/]

    GitHub: @abinercosta-cl
