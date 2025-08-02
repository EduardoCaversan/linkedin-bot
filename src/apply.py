from playwright.sync_api import Page
import random
import time
import os

MOBILE_NUMBER = "+55 (00) 00000-0000"
EMAIL = "youremail@gmail.com"

def random_wait(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))


def fill_basic_form(page):
    try:
        phone_input = page.locator("input[aria-label='Número de telefone']")
        if phone_input.count() > 0 and phone_input.input_value().strip() == "":
            phone_input.fill(MOBILE_NUMBER)
    except:
        pass

    try:
        email_input = page.locator("input[aria-label='Endereço de email']")
        if email_input.count() > 0 and email_input.input_value().strip() == "":
            email_input.fill(EMAIL)
    except:
        pass


def upload_cv_if_needed(page):
    try:
        file_input = page.locator("input[type='file']")
        if file_input.count() > 0:
            file_input.set_input_files(os.path.abspath("./data/Eduardo_Caversan_Dev_Fullstack.pdf"))
            random_wait(2, 4)
    except:
        pass


def is_application_too_complex(page):
    if page.locator("button:has-text('Avançar')").count() > 0:
        return True
    if page.locator("input[type='file']").count() > 0:
        return False 
    return False


def try_apply(page: Page):
    try:
        easy_apply_button = page.locator("button:has-text('Candidate-se facilmente')")
        if easy_apply_button.count() > 0:
            easy_apply_button.first.click()
            random_wait(2, 4)

            fill_basic_form(page)
            upload_cv_if_needed(page)

            if is_application_too_complex(page):
                print("[INFO] Formulário complexo, pulando.")
                close_button = page.locator("button[aria-label='Fechar']")
                if close_button.count() > 0:
                    close_button.first.click()
                return False

            submit_button = page.locator("button:has-text('Enviar candidatura')")
            if submit_button.count() > 0:
                submit_button.first.click()
                random_wait(2, 4)
                return True
    except Exception as e:
        print(f"[WARN] Erro ao tentar aplicar: {e}")
    return False