## Como usar a aplicação

### Pré-requisitos
- Python 3.6 ou superior instalado no sistema

### Configuração do ambiente virtual (recomendado)

#### No Linux

1. **Criar ambiente virtual:**
   ```bash
   python3 -m venv venv
   ```

2. **Ativar ambiente virtual:**
   ```bash
   source venv/bin/activate
   ```

3. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Para desativar o ambiente virtual (quando terminar):**
   ```bash
   deactivate
   ```

#### No Windows

1. **Criar ambiente virtual:**
   ```cmd
   python -m venv venv
   ```
   ou
   ```cmd
   py -m venv venv
   ```

2. **Ativar ambiente virtual:**
   ```cmd
   venv\Scripts\activate
   ```

3. **Instalar dependências:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Para desativar o ambiente virtual (quando terminar):**
   ```cmd
   deactivate
   ```

### Estrutura do projeto
```
├── main.py               # arquivo principal para executar a aplicação
├── models.py             # classes Talk, Session, Track
├── organizer.py          # classe ConferenceOrganizer
├── test_organizer.py     # testes unitários
├── proposals.txt         # arquivo com as palestras de exemplo
├── requirements.txt      # dependências do projeto
└── README.md            # este arquivo
```

### Como executar no Linux

1. **Verificar se Python está instalado:**
   ```bash
   python3 --version
   ```

2. **Navegar até o diretório do projeto:**
   ```bash
   cd /caminho/para/Organiza-o-de-Palestras
   ```

3. **Ativar ambiente virtual (se configurado):**
   ```bash
   source venv/bin/activate
   ```

4. **Executar a aplicação com o arquivo de exemplo:**
   ```bash
   python3 main.py proposals.txt
   ```

5. **Executar os testes:**
   ```bash
   python3 test_organizer.py
   ```
   ou
   ```bash
   pytest -v
   ```

### Como executar no Windows

1. **Verificar se Python está instalado:**
   ```cmd
   python --version
   ```
   ou
   ```cmd
   py --version
   ```

2. **Navegar até o diretório do projeto:**
   ```cmd
   cd C:\caminho\para\Organiza-o-de-Palestras
   ```

3. **Ativar ambiente virtual (se configurado):**
   ```cmd
   venv\Scripts\activate
   ```

4. **Executar a aplicação com o arquivo de exemplo:**
   ```cmd
   python main.py proposals.txt
   ```
   ou
   ```cmd
   py main.py proposals.txt
   ```

5. **Executar os testes:**
   ```cmd
   python test_organizer.py
   ```
   ou
   ```cmd
   py test_organizer.py
   ```
   ou
   ```bash
   pytest -v
   ```

### Formato do arquivo de entrada

O arquivo de entrada deve conter uma palestra por linha, seguindo o formato:
```
Nome da Palestra XXmin
```
ou
```
Nome da Palestra lightning
```

**Exemplos:**
```
Desenvolvimento orientado a gambiarras 45min
Rails para usuários de Django lightning
Manutenção de aplicações legadas em Ruby on Rails 60min
```

### Saída esperada

A aplicação irá gerar um cronograma organizado por tracks, respeitando as restrições de tempo e exibindo:
- Horários das palestras
- Horário do almoço (12:00)
- Horário do evento de networking (entre 16:00 e 17:00)

### Executando com outros arquivos

Para usar um arquivo diferente de `proposals.txt`, basta substituir o nome do arquivo:

**Linux:**
```bash
python3 main.py meu_arquivo.txt
```

**Windows:**
```cmd
python main.py meu_arquivo.txt
```
