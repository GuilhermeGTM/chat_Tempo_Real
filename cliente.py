import socket
import threading
from tkinter import *
import tkinter
from tkinter import simpledialog

# Classe principal do cliente de chat
class Chat:
    def __init__(self):
        # Define IP e porta do servidor
        HOST = '127.0.0.1'
        PORT = 55555

        # Cria o socket do cliente e conecta ao servidor
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        # Cria uma janela oculta para usar como base dos diálogos
        login = Tk()
        login.withdraw()

        # Flags de controle
        self.janela_carregada = False
        self.ativo = True

        # Solicita nome e sala ao usuário via diálogos
        self.nome = simpledialog.askstring('Nome', 'Digite seu nome!', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar!', parent=login)

        # Inicia uma thread para escutar mensagens do servidor
        thread = threading.Thread(target=self.conecta)
        thread.start()

        # Inicia a interface gráfica
        self.janela()

    # Método que cria a janela principal do chat
    def janela(self):
        self.root = Tk()
        self.root.geometry("500x500")  # Define tamanho da janela
        self.root.title('Chat')        # Título da janela

        # Caixa onde as mensagens recebidas serão exibidas
        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=450, height=300)

        # Campo onde o usuário digita a mensagem
        self.envia_mensagem = Entry(self.root)
        self.envia_mensagem.place(relx=0.05, rely=0.7, width=300, height=20)

        # Botão para enviar a mensagem
        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviarMensagem)
        self.btn_enviar.place(relx=0.7, rely=0.7, width=100, height=20)

        # Define ação ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

        # Inicia o loop da interface gráfica
        self.root.mainloop()

    # Método chamado ao fechar a janela
    def fechar(self):
        self.root.destroy()     # Fecha a janela
        self.client.close()     # Fecha a conexão com o servidor

    # Método que escuta mensagens do servidor
    def conecta(self):
        while True:
            recebido = self.client.recv(1024)  # Recebe dados do servidor
            if recebido == b'SALA':
                # Se o servidor pedir a sala, envia sala e nome
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    # Exibe a mensagem recebida na caixa de texto
                    self.caixa_texto.insert('end', recebido.decode())
                except:
                    pass  # Ignora erros (ex: janela ainda não carregada)

    # Método que envia a mensagem digitada para o servidor
    def enviarMensagem(self):
        mensagem = self.envia_mensagem.get()  # Pega o texto digitado
        self.client.send(mensagem.encode())   # Envia ao servidor

# Instancia a classe e inicia o chat
chat = Chat()
