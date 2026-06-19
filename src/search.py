from playwright.sync_api import Page, TimeoutError
import random
import time
import urllib.parse

def random_wait(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

def search_jobs(page: Page, keywords="developer remote", location="Brazil"):
    print(f"[INFO] Iniciando busca: '{keywords}' em '{location}'")

    encoded_keywords = urllib.parse.quote(keywords)
    encoded_location = urllib.parse.quote(location)
    primary_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_keywords}&location={encoded_location}&f_AL=true"
    fallback_url = f"https://www.linkedin.com/search/results/all/?keywords={encoded_keywords}&origin=GLOBAL_SEARCH_HEADER&f_AL=true"

    try:
        print("[INFO] Tentando URL primária de vagas...")
        page.goto(primary_url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
        
    except TimeoutError:
        print("[WARN] Timeout na URL primária! Acionando o fallback global...")
        try:
            page.goto(fallback_url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(3000)
            jobs_tab = page.locator("button:has-text('Vagas'), button:has-text('Jobs')").first
            if jobs_tab.count() > 0:
                jobs_tab.click()
                page.wait_for_timeout(3000)
        except TimeoutError:
            print("[ERROR] Timeout também no fallback. Tentando seguir com o que já carregou...")

    print("[INFO] Realizando scroll para carregar as vagas...")
    try:
        first_job = page.locator('ul.scaffold-layout__list-container li, .jobs-search-results-list li').first
        if first_job.count() > 0:
            first_job.click()
        
        for _ in range(8):
            page.keyboard.press("PageDown")
            random_wait(1, 2)
    except Exception as e:
        print(f"[WARN] Aviso ao tentar fazer scroll: {e}")

    print("[INFO] Extraindo links das vagas...")
    job_links = page.locator('a[href*="/jobs/view/"], a.job-card-list__title').all()
    
    urls = set()
    for link in job_links:
        try:
            href = link.get_attribute("href")
            if href and "/jobs/view/" in href:
                clean_url = href.split("?")[0] if "?" in href else href
                if "linkedin.com" not in clean_url:
                    clean_url = "https://www.linkedin.com" + clean_url
                urls.add(clean_url)
        except Exception:
            continue

    urls_list = list(urls)
    print(f"[INFO] Encontradas {len(urls_list)} vagas únicas para '{keywords}' em '{location}'")
    
    return urls_list