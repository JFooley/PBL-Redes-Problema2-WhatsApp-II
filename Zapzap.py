import socket
import threading
import os
import pickle
import time

# Dados
conversa = set()
membros = []
pkgCache = [] # Cache temporário de pacotes

# Constantes
DTGSIZE = 1024
SYNCTIME = 3

# Tipos de mensagens
MSG = "mensage"
SYN = "sync"
CSP = "chatSyncPart"

# Informações do usuário
myIP = input("Insira seu endereço IP e porta: ")
HOST = myIP.split(':')[0]
PORT = int(myIP.split(':')[1])

# Informações do grupo
membrosSTR = input("Insira os membros: ")
membros = [(memberHost, int(memberPort)) for memberHost, memberPort in (item.split(':') for item in membrosSTR.split())]

# OBJ mensagem
class Mensagem:
    def __init__(self, user, texto, timestamp):
        self.user = user
        self.texto = texto
        self.timestamp = timestamp

    # Dois objetos Mensagem são considerados iguais se tiverem o mesmo timestamp e user
    def __eq__(self, other):
        if isinstance(other, Mensagem):
            return self.timestamp == other.timestamp and self.user == other.user
        return False
    
    # Hash baseado no timestamp e User para garantir unicidade no conjunto
    def __hash__(self):
        return hash((self.timestamp, self.user))

# OBJ Relógio de Lamport
class LamportClock:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

    def update(self, received_time):
        with self.lock:
            self.value = max(self.value, received_time) + 1
            return self.value

# Envia pacotes
def send_message(sock, clock, message, membros, type):
    lamport_time = 0
    
    if type == SYN:
        lamport_time = clock.increment()
    elif type == MSG:
        lamport_time = clock.increment()
        mensagem = Mensagem((HOST, PORT), message, lamport_time)
        conversa.update([mensagem])

    data = pickle.dumps((message, lamport_time, type))
    for pairAdress in membros:
        sock.sendto(data, pairAdress)
        
# Recebe pacotes
def listner(sock, clock):
    while True:
        try:
            pacote = sock.recvfrom(1024)
            message, received_time, type = pickle.loads(pacote[0])
            if type == MSG or type == SYN:
                clock.update(received_time)
            pkgCache.append(pacote)
        except:
            pass

# Trata os pacotes recebidos
def pkgSort(sock, clock):
    while True:
        if len(pkgCache) != 0:
            data, adress = pkgCache.pop() # Tupla contendo Data e ClientAdress (nessa ordem)
            message, received_time, type = pickle.loads(data) # Interpreta o Data

            if type == MSG:
                mensagem = Mensagem(adress, message, received_time)
                conversa.update([mensagem])
                printSort()

            elif type == SYN and (message == 'first' or message == 'syncRequest'):
                send_message(sock, clock, None, membros, SYN) # Mensagme para sincronizar o relógio
                sendChat(sock, clock, adress)

            elif type == CSP:
                messageOBJ = pickle.loads(message)
                conversa.update([messageOBJ])

# Envia a sua conversa
def sendChat(sock, clock, adress):
    for mensagemOBJ in conversa:
        lamport_time = 0
        partMessage = pickle.dumps(mensagemOBJ)
        data = pickle.dumps((partMessage, lamport_time, CSP))
        sock.sendto(data, adress)

# A cada X segundos realiza uma sincronização
def eventualSync(sock, clock):
    while True:
        send_message(sock, clock, 'syncRequest', membros, SYN)
        time.sleep(SYNCTIME)

# Ordena as mensagens
def consensusSort(conversaList):
    if bool(conversaList):
        conversaList.sort(key=lambda x: (x.timestamp, x.user))

# Mostra as mensagens em ordem
def printSort():
    conversaList = list(conversa)
    consensusSort(conversaList)

    os.system('cls')
    for msg in conversaList:
        msg: Mensagem
        print(f'{msg.user[0]}:{msg.user[1]}: {msg.texto}')        
        # print(f'{msg.user[0]}:{msg.user[1]} - {msg.timestamp}: {msg.texto}')
    
    del conversaList

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    clock = LamportClock()

    # Threads
    receive_thread = threading.Thread(target=listner, args=(sock, clock), daemon=True)
    receive_thread.start()

    pkgsort_thread = threading.Thread(target=pkgSort, args=(sock, clock), daemon=True)
    pkgsort_thread.start()

    eventualSync_thread = threading.Thread(target=eventualSync, args=(sock, clock), daemon=True)
    eventualSync_thread.start()

    # First message
    send_message(sock, clock, 'first', membros, SYN)
    while True:
        message = input()
        send_message(sock, clock, message, membros, MSG)
        printSort()

if __name__ == "__main__":
    main()