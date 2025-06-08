# Conference Scheduler

Este projeto organiza automaticamente palestras de uma conferência em várias *tracks*, respeitando regras de tempo para manhã, tarde, almoço e evento de networking.

## 📁 Estrutura

```
conference_scheduler/
├── main.py                # Script principal
├── proposals.txt          # Lista de propostas de palestras
└── tests/
    └── test_scheduler.py  # Testes unitários
```

## ▶️ Como executar

1. Instale o Python (recomenda-se versão 3.8 ou superior).
2. Navegue até a pasta do projeto.
3. Execute o programa principal:

```bash
python main.py
```

O programa lerá o arquivo `proposals.txt` e imprimirá o cronograma organizado das tracks no terminal.

## 🧪 Como executar os testes

Execute os testes com:

```bash
python -m unittest discover tests
```

Os testes verificam se:
- As palestras são corretamente interpretadas a partir do arquivo.
- O agendamento de sessões respeita os limites de tempo.

## 📌 Regras de organização

- **Sessão da manhã:** das 09:00 às 12:00 (180 minutos)
- **Almoço:** 12:00 fixo
- **Sessão da tarde:** das 13:00 até entre 16:00 e 17:00 (mín. 180, máx. 240 minutos)
- **Networking:** começa após 16:00, até no máximo 17:00
- **Lightning talk:** 5 minutos

## 🧠 Estratégia usada

O código utiliza uma abordagem gulosa para preencher sessões com o maior número possível de palestras respeitando a duração máxima. As palestras são ordenadas da maior para a menor antes de serem alocadas.

## 📄 Exemplo de entrada

Veja `proposals.txt` para um exemplo de entrada.

## 📤 Contato

Este projeto foi feito como parte de um exercício de programação com foco em organização e testes.
