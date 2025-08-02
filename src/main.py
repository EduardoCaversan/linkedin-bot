from playwright.sync_api import sync_playwright, TimeoutError
from storage import load_data, save_data, reset_daily_limit
from search import search_jobs, random_wait
from apply import try_apply

LIMIT_PER_DAY = 20

def main():
    data = load_data()
    data = reset_daily_limit(data)

    if data["applications_today"] >= LIMIT_PER_DAY:
        print("[INFO] Limite diário atingido. Encerrando.")
        return

    filters = [
        {"keywords": "fullstack developer .NET Angular", "location": "Remote"},
        {"keywords": "backend developer .NET Core", "location": "Brazil"},
        {"keywords": "frontend developer Angular", "location": "Remote"},
        {"keywords": "developer Azure cloud", "location": "Brazil"},
        {"keywords": "software engineer remote", "location": "Remote"},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto("https://www.linkedin.com/login")
        print("\n⚠️ Faça login manualmente e tecle ENTER quando estiver na tela inicial de vagas.\n")
        input("Pressione ENTER para continuar...")

        # Aguarda o redirecionamento automático para o feed após login
        try:
            page.wait_for_url("https://www.linkedin.com/feed/", timeout=15000)
            print("[INFO] Login confirmado, na página do feed.")
        except TimeoutError:
            print("[WARN] Timeout esperando a página do feed após login.")

        # Agora navega para a página de vagas
        page.goto("https://www.linkedin.com/jobs/")
        page.wait_for_load_state("networkidle", timeout=15000)
        print(f"[INFO] Página atual: {page.url}")

        try:
            for f in filters:
                print(f"\n[INFO] Buscando vagas: '{f['keywords']}' em '{f['location']}'")
                job_links = search_jobs(page, keywords=f["keywords"], location=f["location"])

                for job_url in job_links:
                    if data["applications_today"] >= LIMIT_PER_DAY:
                        print("[INFO] Limite diário atingido durante execução.")
                        break

                    if job_url in data["jobs_applied"]:
                        print(f"[INFO] Vaga já aplicada anteriormente: {job_url}")
                        continue

                    print(f"[INFO] Acessando vaga: {job_url}")
                    try:
                        page.goto(job_url)
                        page.wait_for_load_state("networkidle", timeout=10000)
                        random_wait(4, 8)
                    except TimeoutError:
                        print("[WARN] Timeout ao carregar a vaga. Pulando...")
                        continue

                    try:
                        applied = try_apply(page)
                    except Exception as e:
                        print(f"[ERROR] Erro ao tentar aplicar: {e}")
                        applied = False

                    if applied:
                        data["jobs_applied"].append(job_url)
                        data["applications_today"] += 1
                        print(f"[INFO] Candidatado com sucesso em: {job_url}")
                        save_data(data)
                    else:
                        print(f"[INFO] Vaga {job_url} não possui Easy Apply ou foi ignorada.")

                if data["applications_today"] >= LIMIT_PER_DAY:
                    print("[INFO] Limite diário atingido. Finalizando buscas.")
                    break
        finally:
            browser.close()
            save_data(data)

if __name__ == "__main__":
    main()
