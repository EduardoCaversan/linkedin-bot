from playwright.sync_api import Page, TimeoutError
import random
import time


def random_wait(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))


def find_input(page: Page, selectors: list[str], field_name: str):
    for selector in selectors:
        try:
            input_field = page.locator(selector)
            input_field.wait_for(state="visible", timeout=5000)
            return input_field
        except TimeoutError:
            continue
    print(f"[ERROR] Campo '{field_name}' não encontrado com nenhum seletor conhecido.")
    return None


def search_jobs(page: Page, keywords="developer remote", location="Brazil"):
    print(f"[INFO] Iniciando busca: '{keywords}' em '{location}'")

    search_selectors = [
        "input[aria-label='Pesquisar vagas']",
        "input[aria-label='Pesquisar cargo, competência ou empresa']",
        "input[placeholder*='Pesquisar vagas']",  # fallback por placeholder
        "input[placeholder*='Pesquisar cargo']",   # fallback alternativo
    ]

    location_selectors = [
        "input[aria-label='Pesquisar local']",
        "input[placeholder*='Adicionar local']",  # fallback se o LinkedIn mudar o label
    ]

    search_input = find_input(page, search_selectors, "pesquisa de vagas")
    if not search_input:
        return []

    location_input = find_input(page, location_selectors, "localização")
    if not location_input:
        return []

    # Preenche campos
    search_input.fill("")
    random_wait(0.5, 1.5)
    search_input.fill(keywords)
    random_wait(0.5, 1.5)

    location_input.fill("")
    random_wait(0.5, 1.5)
    location_input.fill(location)
    random_wait(0.5, 1.5)
    location_input.press("Enter")

    random_wait(3, 5)

    # Scroll controlado
    for _ in range(8):
        page.mouse.wheel(0, random.randint(600, 900))
        random_wait(0.5, 1.2)

    # Captura links das vagas (ajustado para o LinkedIn atual)
    job_links = page.locator('a.job-card-list__title').all()
    urls = list({link.get_attribute("href") for link in job_links if link.get_attribute("href")})

    print(f"[INFO] Encontradas {len(urls)} vagas únicas para '{keywords}' em '{location}'")
    return urls