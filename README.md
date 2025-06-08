# Organizador de Palestras 

## O que precisa:

- Python 3.6 (ou superior) instalado.

## Windows:

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

4. **Para desativar o ambiente virtual:**
   ```cmd
   deactivate
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

3. **Ativar ambiente virtual:**
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
5. **Executar teste:**
   ```bash
   python3 organizer-test.py proposals.txt
   ```

## No Linux

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

4. **Para desativar o ambiente virtual:**
   ```bash
   deactivate
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

3. **Ativar ambiente virtual:**
   ```bash
   source venv/bin/activate
   ```

4. **Executar a aplicação com o arquivo de exemplo:**
   ```bash
   python3 main.py proposals.txt
   ```

5. **Executar teste:**
   ```bash
   python3 organizer-test.py proposals.txt
   ```

## Formato de entrada

*Nome da Palestra XXmin* ou *Nome da Palestra lightning*
