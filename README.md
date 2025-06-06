## Organizador de Palestras para Conferências

Este projeto é um organizador automático de palestras para conferências, desenvolvido em Python. Ele aloca palestras em sessões matinais e vespertinas, respeitando as restrições de tempo de cada parte do dia e ajustando automaticamente a quantidade de dias necessárias com base na quantidade de palestras fornecidas.

## Objetivo

Automatizar a alocação de palestras em **dias** de conferência, divididas em:
- **Sessão da manhã:** 09:00 às 12:00
- **Sessão da tarde:** 13:00 até no máximo 17:00 (com evento de networking a partir das 16:00)

## 📝 Formato do Arquivo de Entrada

O arquivo `.txt` deve conter uma palestra por linha, com o seguinte formato:
Nome da palestra DURAÇÃO
- Duração deve terminar com `min` ou ser `lightning` (que será tratado como 5 minutos).

## Exemplos válidos:
Escrevendo código limpo 60min
Arquitetura de Software 60min
Big Data e Analytics 60min


## ▶️ Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Abra o terminal na pasta do projeto.
3. Execute:

```bash
python organizador.py
```

4. Quando solicitado, digite o nome do arquivo .txt com as palestras (ex: palestras_teste.txt).

## Exemplo de Saída

Dia 1:
09:00 Escrevendo código limpo 60min
10:00 Testes automatizados com Pytest 45min
...
12:00 Almoço
13:00 API REST com Flask 45min
...
16:00 Evento de Networking

Dia 2:
09:00 Docker e Kubernetes 60min
...
16:00 Evento de Networking

OBS: O número de dias é determinado automaticamente conforme a necessidade para encaixar todas as palestras.










