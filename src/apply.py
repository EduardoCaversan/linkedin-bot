from playwright.sync_api import Page
import random
import time
import os
import re
from ai_helper import answer_question_with_ai

MOBILE_NUMBER = "+55 (00) 00000-0000"
EMAIL = "email@gmail.com"

def random_wait(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

def fill_basic_form(page: Page):
    """Preenche e-mail e telefone."""
    try:
        phone = page.locator("input[id*='phone'], input[name*='phone']")
        if phone.count() > 0 and phone.first.is_visible() and phone.first.input_value() == "":
            phone.first.fill(MOBILE_NUMBER)
        email = page.locator("input[type='email'], input[id*='email']")
        if email.count() > 0 and email.first.is_visible() and email.first.input_value() == "":
            email.first.fill(EMAIL)
    except: pass

def upload_cv_if_needed(page: Page):
    """Anexa o PDF da pasta data."""
    try:
        file_input = page.locator("input[type='file']")
        if file_input.count() > 0 and file_input.first.is_visible():
            from ai_helper import CV_PATH
            file_input.first.set_input_files(CV_PATH)
            random_wait(2, 3)
    except: pass

def fill_dynamic_questions(page: Page):
    """Usa a IA para responder perguntas dinâmicas do LinkedIn."""
    form_elements = page.locator(".fb-dash-form-element, .jobs-easy-apply-form-element")
    for i in range(form_elements.count()):
        element = form_elements.nth(i)
        label = element.locator("label").first
        input_box = element.locator("input.artdeco-text-input--input, textarea")
        
        if label.count() > 0 and input_box.count() > 0:
            question = label.inner_text()
            if input_box.first.input_value().strip() == "":
                print(f"[IA] Respondendo: {question.strip()}")
                answer = answer_question_with_ai(question)
                input_box.first.fill(answer)
                random_wait(1, 2)

def try_apply(page: Page):
    try:
        random_wait(3, 5)
        
        for step in range(12):
            fill_basic_form(page)
            upload_cv_if_needed(page)
            fill_dynamic_questions(page)
            
            random_wait(2, 3)
            
            btn_submit = page.locator("button[data-live-test-easy-apply-submit-button]")
            btn_review = page.locator("button[data-live-test-easy-apply-review-button]")
            btn_next = page.locator("button[data-easy-apply-next-button]")

            
            if btn_submit.count() > 0 and btn_submit.first.is_visible():
                print("[INFO] Botão ENVIAR detectado. Clicando...")
                btn_submit.first.click(force=True)
                random_wait(4, 6)
                if page.locator("text=Concluído").count() > 0 or page.locator("text=Done").count() > 0:
                    print("[INFO] Vaga enviada com sucesso!")
                    return True
                continue

            if btn_review.count() > 0 and btn_review.first.is_visible():
                print("[INFO] Botão REVISAR detectado. Clicando...")
                btn_review.first.click(force=True)
                random_wait(2, 3)
                continue

            if btn_next.count() > 0 and btn_next.first.is_visible():
                print("[INFO] Botão AVANÇAR detectado. Clicando...")
                btn_next.first.click(force=True)
                random_wait(2, 3)
                continue
            
            print("[INFO] Fim da navegação ou botões não visíveis.")
            break
        
        return False
    except Exception as e:
        print(f"[WARN] Erro no fluxo: {e}")
        return False