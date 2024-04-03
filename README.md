# Bot Telegram - Harry Mason Server

Este é um bot do telegram para facilitar algumas instruções para meu HomeLab.

Abaixo estão as instruções de como criar e configurar um ambiente virtual (venv) do Python, instalar dependências a partir de um arquivo `requirements.txt`, configurar variáveis de ambiente e iniciar o projeto.

## Configuração do Ambiente Virtual (venv)

Um ambiente virtual do Python é uma ferramenta que permite criar ambientes Python isolados, tornando mais fácil gerenciar dependências de projetos. Siga os passos abaixo para criar e configurar um ambiente virtual:

1. **Criação do Ambiente Virtual**:

```bash
python -m venv venv
```

2. **Ativação do Ambiente Virtual**:

- No Windows:
  - CMD
  ```bash
  venv\Scripts\activate.bat
  ```
  - PowerShell
  ```bash
  venv\Scripts\Activate.ps1
  ```
- No Linux/MacOS:

```bash
source venv/bin/activate
```

## Instalação de Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalar todas as dependências, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Configuração de Variáveis de Ambiente

Este projeto requer a configuração de algumas variáveis de ambiente. Elas podem ser configuradas da seguinte forma:

- `TELEGRAM_BOT_TOKEN`: Token de acesso do seu bot do Telegram.
- `TELEGRAM_CHAT_ID`: ID do chat do Telegram onde as mensagens serão enviadas.
- `WAKE_ON_LAN_MACS`: Endereços MAC dos dispositivos que serão acionados com o comando Wake-on-LAN.
- `IP_HOME_SERVER`: Endereço IP do dispositivo que será verificado status.

Por exemplo, para configurar as variáveis de ambiente no Windows, você pode usar o comando:

```bash
set TELEGRAM_BOT_TOKEN=12345678:XXXXXXXXXXX
set TELEGRAM_CHAT_ID=1234
set WAKE_ON_LAN_MACS=00:11:22:33:44:55,AA:BB:CC:DD:EE:FF
set IP_HOME_SERVER=192.168.0.10
```

E no Linux/MacOS:

```bash
export TELEGRAM_BOT_TOKEN=12345678:XXXXXXXXXXX
export TELEGRAM_CHAT_ID=1234
export WAKE_ON_LAN_MACS=00:11:22:33:44:55,AA:BB:CC:DD:EE:FF
export IP_HOME_SERVER=192.168.0.10
```

## Configuração de Variáveis de Ambiente usando .env

Você também pode configurar as variáveis de ambiente utilizando um arquivo `.env`. Para isso, siga os passos abaixo:

1. Crie um arquivo chamado `.env` na raiz do projeto.
2. Copie o conteúdo do arquivo `.env.example` fornecido.
3. Preencha as variáveis de ambiente com seus valores correspondentes no arquivo `.env`.

## Iniciando o Projeto

Após configurar o ambiente virtual, instalar as dependências e configurar as variáveis de ambiente, você pode iniciar o projeto executando o seguinte comando:

```bash
python bot-telegram.py
```

Isso iniciará o seu bot do Telegram e estará pronto para uso. Certifique-se de que o bot está configurado corretamente no Telegram e tem permissões adequadas para funcionar conforme esperado.
