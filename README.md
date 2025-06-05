<<<<<<< HEAD
# Organização de palestras de uma conferência

Você está planejando uma grande conferencia de programação e recebeu diversas propostas de palestras, mas você está com problemas para organizá-las de acordo com as restrições de tempo do dia - existem tantas possibilidades! Então, você decide escrever um programa para fazer isso por você.

1. A conferencia tem várias tracks, cada qual tendo uma sessão pela manhã e outra pela tarde.
2. Cada sessão contém várias palestras.
3. Sessões pela manhã começam às 9h e devem terminar às 12h, para o almoço.
4. Sessões pela tarde começam às 13h e devem terminar a tempo de realizar o evento de networking.
5. O evento de networking deve começar depois das 16h, mas antes das 17h.
6. Nenhum dos nomes das palestras possui números.
7. A duração de todas as palestras são fornecidas em minutos ou definidas como lightning (palestras de 5 minutos).
8. Os palestrantes serão bastante pontuais, então não há a necessidade de intervalos entre as palestras.

Observe que, dependendo de como você decida completar esse problema, sua solução pode trazer as palestras em ordem ou combinação diferentes dentro das tracks. Isso é aceitável; você não precisa replicar, exatamente, o resultado fornecido como exemplo de solução.
Mas o resultado produzido deverá atender às regras especificadas.

## Dados a serem usados para teste:
Diminuindo tempo de execução de testes em aplicações Rails enterprise 60min

Reinventando a roda em ASP clássico 45min

Apresentando Lua para as massas 30min

Erros de Ruby oriundos de versões erradas de gems 45min

Erros comuns em Ruby 45min

Rails para usuários de Django lightning

Trabalho remoto: prós e cons 60min

Desenvolvimento orientado a gambiarras 45min

Aplicações isomórficas: o futuro (que talvez nunca chegaremos) 30min

Codifique menos, Escreva mais! 30min

Programação em par 45min

A mágica do Rails: como ser mais produtivo 60min

Ruby on Rails: Por que devemos deixá-lo para trás 60min

Clojure engoliu Scala: migrando minha aplicação 45min

Ensinando programação nas grotas de Maceió 30min

Ruby vs. Clojure para desenvolvimento backend 30min

Manutenção de aplicações legadas em Ruby on Rails 60min

Um mundo sem StackOverflow 30min

Otimizando CSS em aplicações Rails 30min


## Modelo do resultado esperado após execução da organização: 

#### Track A:
09:00 Diminuindo tempo de execução de testes em aplicações Rails enterprise 60min

10:00 Reinventando a roda em ASP clássico 45min

10:45 Apresentando Lua para as massas 30min

11:15 Erros de Ruby oriundos de versões erradas de gems 45min

12:00 Almoço

13:00 Ruby on Rails: Por que devemos deixá-lo para trás 60min

14:00 Erros comuns em Ruby 45min

14:45 Programação em par 45min

15:30 Ensinando programação nas grotas de Maceió 30min

16:00 Ruby vs. Clojure para desenvolvimento backend 30min

16:30 Otimizando CSS em aplicações Rails 30min

17:00 Evento de Networking

#### Track B:
09:00 Trabalho remoto: prós e cons 60min

10:00 A mágica do Rails: como ser mais produtivo 60min

11:00 Aplicações isomórficas: o futuro (que talvez nunca chegaremos) 30min

11:30 Codifique menos, Escreva mais! 30min

12:00 Almoço

13:00 Desenvolvimento orientado a gambiarras 45min

13:45 Clojure engoliu Scala: migrando minha aplicação 45min

14:30 Um mundo sem StackOverflow 30min

15:00 Manutenção de aplicações legadas em Ruby on Rails 60min

16:00 Rails para usuários de Django lightning

17:00 Evento de Networking

## Instruções
Você deve produzir uma solução para o problema acima utilizando **qualquer linguagem de programação**.
No diretório raiz do repositório, você encontrará o arquivo ***proposals.txt***, que contém a lista de palestras que deverão ser organizadas. Seu programa deverá ser capaz de ler este arquivo e processar cada uma das palestras, para que o resultado seja exibido no formato especificado no exemplo exibido acima.

Espera-se que você encaminhe um código que acredite ser de qualidade, um código que funcione e que tenha sido evoluído no decorrer de seu desenvolvimento.

Obs:

Na hora de executar o código, será testada outra entrada semelhante, para comprovação da solução.

Outro requisito é o envio dos testes que você produziu para verificar sua solução. Independente de serem feitos antes ou depois de criada a implementação, queremos ter a chance de observar sua habilidade em produzi-los e verificar as regras do problema.
=======
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

## Formato de entrada

**Nome da Palestra XXmin** ou **Nome da Palestra lightning**
>>>>>>> f87fa6a (Implementa algoritmo e atualiza ReadMe)
