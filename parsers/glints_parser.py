import asyncio
from playwright.async_api import async_playwright


class GlintsParser:
    def __init__(self, portal_name="Glints"):
        self.portal_name = portal_name
        self.base_url = "https://glints.com"

    async def scrape(self, keyword: str):
        results = []
        search_url = f"https://glints.com/id/opportunities/jobs?keyword={keyword.replace(' ', '%20')}"

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

                # Tutup popup jika muncul
                for selector in [
                    "button[aria-label='Close']",
                    "button[aria-label='close']",
                    "button:has-text('Nanti saja')",
                    "button:has-text('Tidak, Terima Kasih')",
                ]:
                    try:
                        btn = await page.query_selector(selector)
                        if btn:
                            await btn.click()
                            await asyncio.sleep(1)
                            break
                    except Exception:
                        pass

                # Scroll agar lazy loading aktif
                for _ in range(4):
                    await page.mouse.wheel(0, 1200)
                    await asyncio.sleep(2)

                # Ambil link lowongan
                links = await page.query_selector_all("a[href*='/id/opportunities/jobs/'], a[href*='/opportunities/jobs/']")
                seen = set()

                for link_el in links:
                    try:
                        href = await link_el.get_attribute("href")
                        if not href:
                            continue

                        if href.startswith("/"):
                            href = self.base_url + href

                        if href in seen:
                            continue
                        seen.add(href)

                        text = await link_el.inner_text()
                        lines = [line.strip() for line in text.splitlines() if line.strip()]

                        if len(lines) == 0:
                            continue

                        title = lines[0]
                        company = lines[1] if len(lines) > 1 else "Tidak tersedia"
                        lokasi = "Indonesia"

                        results.append({
                            "judul_posisi": title,
                            "nama_perusahaan": company,
                            "lokasi": lokasi,
                            "pendidikan": "",
                            "link_lowongan": href,
                            "portal_sumber": self.portal_name
                        })

                        if len(results) >= 20:
                            break

                    except Exception:
                        continue

                print(f"[{self.portal_name}] Total data: {len(results)}")
                await browser.close()
                return results

            except Exception as e:
                print(f"[ERROR] {self.portal_name}: {e}")
                await browser.close()
                return []
