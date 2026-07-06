import asyncio
from playwright.async_api import async_playwright


class JobstreetParser:
    def __init__(self, portal_name="Jobstreet"):
        self.portal_name = portal_name
        self.base_url = "https://id.jobstreet.com"

    async def scrape(self, keyword: str):
        results = []
        slug_keyword = keyword.replace(" ", "-")
        search_url = f"https://id.jobstreet.com/id/{slug_keyword}-jobs"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            )
            page = await context.new_page()
            page.set_default_timeout(60000)

            try:
                print(f"[{self.portal_name}] Membuka: {search_url}")
                await page.goto(search_url, wait_until="domcontentloaded")
                await asyncio.sleep(5)

                for _ in range(3):
                    await page.mouse.wheel(0, 1000)
                    await asyncio.sleep(2)

                # Selector Jobstreet yang umum dipakai
                job_cards = await page.query_selector_all("article[data-automation='normalJobCard']")

                # Fallback jika selector berubah
                if not job_cards:
                    job_cards = await page.query_selector_all("article")

                seen = set()

                for card in job_cards[:25]:
                    try:
                        title_el = await card.query_selector("a[data-automation='jobTitle']")
                        company_el = await card.query_selector("a[data-automation='jobCompany']")
                        location_el = await card.query_selector("[data-automation='jobLocation']")

                        if not title_el:
                            title_el = await card.query_selector("a[href*='/job/']")

                        if not title_el:
                            continue

                        title = (await title_el.inner_text()).strip()
                        href = await title_el.get_attribute("href")

                        if not href:
                            continue

                        if href.startswith("/"):
                            href = self.base_url + href

                        if href in seen:
                            continue
                        seen.add(href)

                        company = "Tidak tersedia"
                        if company_el:
                            company = (await company_el.inner_text()).strip()

                        lokasi = "Indonesia"
                        if location_el:
                            lokasi = (await location_el.inner_text()).strip()

                        results.append({
                            "judul_posisi": title,
                            "nama_perusahaan": company,
                            "lokasi": lokasi,
                            "pendidikan": "",
                            "link_lowongan": href,
                            "portal_sumber": self.portal_name
                        })

                    except Exception:
                        continue

                print(f"[{self.portal_name}] Total data: {len(results)}")
                await browser.close()
                return results

            except Exception as e:
                print(f"[ERROR] {self.portal_name}: {e}")
                await browser.close()
                return []
