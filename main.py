import asyncio
import os
import random
import pandas as pd

from parsers.glints_parser import GlintsParser
from parsers.jobstreet_parser import JobstreetParser


async def main():
    keywords = [
        "Admin SMK",
        "Operator Produksi",
        "Staff Gudang",
        "SMA",
        "SMK",
        "D3",
        "S1"
    ]

    parsers = [
        GlintsParser("Glints"),
        JobstreetParser("Jobstreet")
    ]

    all_data = []

    print("=== MEMULAI SCRAPING 2 PORTAL ===")

    for parser in parsers:
        for keyword in keywords:
            print(f"\n--- {parser.portal_name} | Keyword: {keyword} ---")
            data = await parser.scrape(keyword)

            if data:
                all_data.extend(data)
                print(f"[BERHASIL] {len(data)} data ditemukan.")
            else:
                print("[INFO] Tidak ada data ditemukan.")

            await asyncio.sleep(random.uniform(3, 7))

    if all_data:
        df = pd.DataFrame(all_data)
        df = df.drop_duplicates(subset=["link_lowongan"])

        os.makedirs("data/raw", exist_ok=True)
        output_path = "data/raw/master_raw_data.csv"
        df.to_csv(output_path, index=False, encoding="utf-8-sig")

        print("\n=== SELESAI ===")
        print(f"Total data bersih: {len(df)}")
        print(f"File disimpan di: {output_path}")
    else:
        print("\n[PERINGATAN] Tidak ada data yang berhasil diambil.")


if __name__ == "__main__":
    asyncio.run(main())
