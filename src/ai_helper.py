import os
import re
import PyPDF2
from openai import OpenAI
import glob

client = OpenAI(
    api_key="",  # Faça login em https://console.groq.com/ e gere um token de API, adicione-o aqui após isso
    base_url="https://api.groq.com/openai/v1"
)

MINHA_CIDADE = "São Paulo, PR" # Substitua pela sua
MEU_PAIS = "Brasil" # Substitua pelo seu

def get_first_pdf_in_data():
    """Procura automaticamente por qualquer arquivo PDF dentro da pasta /data"""
    data_path = os.path.abspath("./data")
    pdf_files = glob.glob(os.path.join(data_path, "*.pdf"))
    
    if not pdf_files:
        print(f"[ERRO] Nenhum arquivo PDF encontrado na pasta: {data_path}")
        return None
    
    print(f"[INFO] Usando o arquivo: {pdf_files[0]}")
    return pdf_files[0]

def extract_text_from_pdf(pdf_path):
    """Lê o texto do PDF encontrado."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"[ERRO] Não foi possível ler o PDF: {e}")
    return text

CV_PATH = get_first_pdf_in_data()
RESUME_CONTEXT = extract_text_from_pdf(CV_PATH) if CV_PATH else ""

def answer_question_with_ai(question_text):
    prompt = f"""
    Responda a esta pergunta de formulário de emprego.
    Dados pessoais: Localização: {MINHA_CIDADE}, País: {MEU_PAIS}.
    Currículo: {RESUME_CONTEXT}
    
    Pergunta: "{question_text}"
    
    Regras:
    1. Se perguntar sobre cidade/localização, responda: "{MINHA_CIDADE}".
    2. Se perguntar sobre permissão de trabalho no país, responda: "Sim".
    3. Seja curto e direto.
    4. Se perguntar a quantos anos usa alguma tecnologia e você não tiver a informação, responda uma quantidade que faça sentido com a expperiência do currículo, responda apenas o número e pronto!
    5. Sempre que a pergunta for a quantos anos usa alguma coisa, responda apenas com um número simples, como por exemplo: "1" apenas o número e mais absolutamente nada!
    6. Se perguntar sobre pretensão salarial, responda uma estimativa baseada na vaga, apenas os números, mais absolutamente nada!
    7. Se perguntar "Quanto tempo de experiência como xxx?" responda com números decimais, exemplo: "5,6" apenas os números e mais nada!
    """
    """Consulta a i.a via Nuvem (Groq). Super rápido e não pesa no seu PC."""
    try:
        completion = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {"role": "system", "content": f"Você é um assistente de preenchimento de formulários. Use este CV: {RESUME_CONTEXT}"},
                {"role": "user", "content": f"Responda a esta pergunta do LinkedIn de forma curta e direta: {prompt}"}
            ]
        )
        raw_response = completion.choices[0].message.content
        clean_response = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL)
        return clean_response.strip()
    except Exception as e:
        print(f"[ERRO na IA] {e}")
        return ""