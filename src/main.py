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
        print("\n⚠️ Faça login manualmente e tecle ENTER quando estiver na tela inicial do feed.\n")
        input("Pressione ENTER para continuar...")

        try:
            page.wait_for_url("https://www.linkedin.com/feed/", timeout=15000)
            print("[INFO] Login confirmado, na página do feed.")
        except TimeoutError:
            print("[WARN] Timeout esperando a página do feed após login. Seguindo mesmo assim...")

        print("[INFO] Navegando para a página de vagas...")
        try:
            page.goto("https://www.linkedin.com/jobs/", wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(3000)
        except TimeoutError:
            print("[WARN] Timeout ao carregar /jobs/. O script tentará continuar.")
            
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

                    clean_job_url = job_url.split("?")[0].rstrip("/")
                    direct_apply_url = f"{clean_job_url}/apply/?openSDUIApplyFlow=true"
                    print(f"[INFO] Acessando vaga (Deep Link): {direct_apply_url}")
                    try:
                        print(f"[INFO] Acessando vaga: {direct_apply_url}")
                        page.goto(direct_apply_url, wait_until="networkidle", timeout=30000)
                    except Exception as e:
                        print(f"[WARN] Erro ao carregar, esperando e tentando novamente... {e}")
                        page.wait_for_timeout(15000) 
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