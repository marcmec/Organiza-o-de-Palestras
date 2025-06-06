# Comecei criando a classe "Palestra" para armazenar o titulo e a duração. Depois fiz mais 4 funções:  
# 1- Ler o arquivo que contém as palestras e a duração, instanciando o objeto da classe "Palestra" e adicionando em uma lista. 
# 2- Será responsável por armazenar as sessões em uma lista que serão adicionadas nas trilhas, com base na duração. 
# 3- Irá preencher a sessão da manhã com palestras até atingir 180 minutos (LIMITE_MIN) e a da tarde até 240 minutos (TARDE_MAX), 
# sendo que as palestras serão ordenadas da mais longa para a mais curta. 
# 4- Mostra o cronograma das trilhas, começando às 09:00, com pausa para o almoço às 12:00 e retomada às 13:00. Ao fim da tarde, 
# um evento de networking ocorre após as 16:00.

from datetime import timedelta, datetime 

LIMITE_MIN = 180  #  3 horas (180 minutos)
TARDE_MAX = 240   #  4 horas (240 minutos)

class Palestra:
    def __init__(self, titulo, duracao):
        self.titulo = titulo
        self.duracao = 5 if duracao == 'lightning' else int(duracao.replace('min', ''))

    def __str__(self):
        return f"{self.titulo} {self.duracao}min"

def ler_palestras(caminho_arquivo):
    palestras = [] 
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            # Separa o título da palestra da duração (divide pela última ocorrência de espaço)
            titulo, duracao = linha.strip().rsplit(' ', 1)
            palestras.append(Palestra(titulo, duracao))  # Adiciona objeto Palestra à lista
    return palestras 

def agendar_sessao(palestras, tempo_limite):
    sessao = []  
    total = 0    # Tempo total acumulado na sessão
    i = 0        # Índice da palestra atual
    while i < len(palestras):  # Enquanto houver palestras
        palestra = palestras[i]
        if total + palestra.duracao <= tempo_limite:
            # Se a palestra couber na sessão, adiciona
            sessao.append(palestra)
            total += palestra.duracao
            palestras.pop(i)  # Remove a palestra da lista original
        else:
            i += 1  # Senão, tenta a próxima palestra
    return sessao

def agendar_trilhas(palestras):
    trilhas = []      
    id_trilha = 1     # Contador para nomear as trilhas como A, B
    palestras.sort(key=lambda p: -p.duracao)  # Ordena as palestras da mais longa para a mais curta
    while palestras:
        manha = agendar_sessao(palestras, LIMITE_MIN)  
        tarde = agendar_sessao(palestras, TARDE_MAX)  
        trilhas.append((f"Trilha {chr(64 + id_trilha)}", manha, tarde))  # Adiciona trilha com nome
        id_trilha += 1  # Próxima trilha será B
    return trilhas 

def imprimir_agenda(trilhas):
    for nome_trilha, manha, tarde in trilhas:
        print(f"{nome_trilha}:")  # Nome da trilha (ex: Trilha A)
        
        horario_atual = datetime.strptime("09:00", "%H:%M")  # Começa às 09:00 da manhã
        for palestra in manha:
            # Imprime cada palestra da manhã com seu horário
            print(f"{horario_atual.strftime('%H:%M')} {palestra}")
            horario_atual += timedelta(minutes=palestra.duracao)  # Avança o relógio

        print("12:00 Almoço") 

        horario_atual = datetime.strptime("13:00", "%H:%M") 
        for palestra in tarde:
            # Imprime cada palestra da tarde com seu horário
            print(f"{horario_atual.strftime('%H:%M')} {palestra}")
            horario_atual += timedelta(minutes=palestra.duracao) # Avança o relógio

        # Se a sessão da tarde acabar antes das 16h, espera até 16h para o networking
        if horario_atual.time() < datetime.strptime("16:00", "%H:%M").time():
            horario_atual = datetime.strptime("16:00", "%H:%M")

        print(f"{horario_atual.strftime('%H:%M')} Evento de Networking\n") 

if __name__ == "__main__":
    palestras = ler_palestras("proposals.txt")
    trilhas = agendar_trilhas(palestras)        
    imprimir_agenda(trilhas)                   