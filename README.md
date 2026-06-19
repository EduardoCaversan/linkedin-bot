# 🚀 LinkedIn Auto Apply Bot (Powered by AI)

Automação avançada para candidatura em vagas no LinkedIn com **"Easy Apply"**. O bot agora conta com um agente de **Inteligência Artificial (via Groq/Llama 3)** que lê seu currículo e responde a perguntas dinâmicas do formulário automaticamente.

---

## ✅ Funcionalidades de IA e Automação

* **Agente de IA (Cloud):** Responde perguntas de formulário (cidade, experiência, etc.) usando o Llama 3 via API.
* **Leitura Inteligente:** Extrai dados do seu PDF automaticamente para embasar as respostas da IA.
* **Navegação Resiliente:** Utiliza seletores baseados em atributos técnicos (`data-live-test...`) para evitar quebras em atualizações do LinkedIn.
* **Preenchimento Completo:** Lida com dados básicos (email/telefone), upload de currículo e perguntas complexas de formulário.
* **Segurança:** Delays randomizados e limites de candidatura para reduzir riscos.

---

## 📂 Estrutura do Projeto

```text
linkedin-bot/
├── data/
│   ├── applied_jobs.json    # Histórico de vagas
│   └── *.pdf                # Coloque seu CV aqui (detectado automaticamente)
├── src/
│   ├── main.py              # Orquestrador
│   ├── apply.py             # Lógica de automação (Candidatura)
│   ├── ai_helper.py         # Integração com IA (Groq/Llama 3)
│   ├── search.py            # Busca e navegação
│   └── storage.py           # Controle de persistência
├── requirements.txt         # Dependências
└── README.md                # Documentação

```

---

## 🔧 Configuração e Instalação

### 1. Preparação do Ambiente

```bash
python -m venv venv
# Ative: venv\Scripts\activate (Windows) ou source venv/bin/activate (Linux/Mac)
pip install -r requirements.txt
playwright install

```

### 2. Configuração da IA (Groq API)

Para o bot responder as perguntas do formulário:

1. Crie uma conta gratuita em [console.groq.com](https://console.groq.com/).
2. Gere sua **API Key**.
3. Abra o arquivo `src/ai_helper.py` e insira sua chave no campo `api_key`.

### 3. Preparação do Currículo

Coloque seu currículo em PDF dentro da pasta `/data`. O bot encontrará qualquer arquivo `.pdf` nessa pasta automaticamente.

---

## 🚀 Como Executar

```bash
python src/main.py

```

1. **Login Manual:** O navegador abrirá. Faça login na sua conta LinkedIn.
2. **Autorização:** Quando estiver no feed de vagas, volte ao terminal e pressione **ENTER**.
3. **Automação:** O bot iniciará o fluxo de aplicação inteligente, preenchendo as perguntas conforme necessário.

---

## 💡 Melhores Práticas (IA & Bloqueios)

* **Prompt da IA:** Em `src/ai_helper.py`, você pode ajustar o `system prompt` para refinar como a IA responde às empresas (ex: ser mais formal, destacar tecnologias específicas).
* **Limite Diário:** Recomendamos manter entre **20-30 candidaturas por dia**. Exceder isso pode disparar alertas de segurança do LinkedIn.
* **Tratamento de Erros:** O bot está configurado com `networkidle` e `timeout` otimizados para contornar bloqueios temporários de rede (`ERR_ABORTED`). Caso ocorra uma falha de conexão, o bot simplesmente aguardará e seguirá para a próxima vaga.

---

## 🛑 Aviso Legal

Este projeto foi criado para fins **educacionais**. O uso de bots para automação de candidaturas viola os [Termos de Serviço do LinkedIn](https://www.linkedin.com/legal/user-agreement).

* **Risco de conta:** O uso excessivo ou mal configurado pode resultar na suspensão da sua conta.
* **Responsabilidade:** O autor não se responsabiliza pelo uso desta ferramenta. Use com moderação e por sua conta e risco.

---