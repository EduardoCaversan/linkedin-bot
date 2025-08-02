# 🚀 LinkedIn Auto Apply Bot (100% Open Source)

Automação para candidatar automaticamente em vagas no LinkedIn com **"Candidate-se facilmente" (Easy Apply)**.  
Agora com busca mais profunda, preenchimento automático e múltiplos filtros específicos para perfil Fullstack / .NET / Angular.

---

## ✅ Funcionalidades

- Busca automática de vagas com filtros específicos para seu perfil.
- Faz scroll na página para carregar mais resultados.
- Candidatura automática em vagas com **"Easy Apply"**.
- Preenchimento automático de telefone e e-mail.
- Upload automático do seu currículo PDF.
- Controle de limite diário de candidaturas.
- Evita repetir candidaturas em vagas já aplicadas.

---

## 📂 Estrutura do Projeto

```

linkedin-bot/
├── src/
│   ├── main.py                      # Arquivo principal (com seus filtros prontos)
│   ├── apply.py                     # Lógica da candidatura automática
│   ├── search.py                    # Busca com scroll e delays humanos
│   ├── storage.py                   # Controle via JSON
├── data/
│   ├── applied\_jobs.json            # Histórico de vagas aplicadas
│   ├── SeuCv.pdf  # Seu CV para upload automático
├── requirements.txt                 # Dependências Python
├── README.md                        # Documentação do projeto

````

---

## 📋 Pré-requisitos

- **Python 3.11+**
- Google Chrome ou Chromium instalado.

---

## 🔧 Instalação

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install
````

---

## 🚀 Como Executar

```bash
python src/main.py
```

### Passos:

1️⃣ O navegador será aberto no LinkedIn.
2️⃣ Faça login manualmente na sua conta.
3️⃣ Quando estiver na página inicial de vagas, **volte ao terminal e pressione ENTER.**
4️⃣ O bot irá:

* Buscar vagas de acordo com os filtros.
* Navegar nas vagas e aplicar automaticamente quando possível.
* Registrar tudo em `applied_jobs.json`.

---

## 🎯 Filtros utilizados (personalizados para seu perfil)

* backend .NET Core (Brasil)
* fullstack .NET + Angular (Remoto)
* frontend Angular (Remoto)
* developer Azure cloud (Brasil)
* software engineer remote (Remoto)

---

## 🛑 Recomendações de Uso

| Limite diário | Motivo                        |
| ------------- | ----------------------------- |
| 20-50         | Evitar bloqueios do LinkedIn  |
| Horário       | 9h-18h (horário comercial)    |
| Delays        | Randomizados, já configurados |

---

## 📄 Controle via JSON

O arquivo `data/applied_jobs.json` armazena histórico e controle diário:

```json
{
    "jobs_applied": [],
    "applications_today": 0,
    "last_run_date": ""
}
```

---

## 📎 Currículo

Certifique-se de ter o arquivo de currículo como no modelo abaixo:

```
/data/SeuCv.pdf
```

Ele será anexado automaticamente nas vagas que pedirem upload de currículo.

---

## ❗ Aviso Legal

Esta automação é **educacional**. Usar bots viola os **Termos de Uso do LinkedIn** e pode resultar no bloqueio da conta.
Use por sua conta e risco.

---