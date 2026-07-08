import os
import pandas as pd
import mysql.connector

CSV_PATH = "data/raw/master_raw_data.csv"

db_config = {
    "host": "hayabusa.proxy.rlwy.net",
    "port": 56767,
    "user": "root",
    "password": "PGNXILAAJFbyCrNRjtOPFkHTHliBSBgz",
    "database": "railway",
}
df = pd.read_csv(CSV_PATH)
df = df.fillna("")

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

sql = """
INSERT INTO jobs
(judul_posisi, nama_perusahaan, lokasi, pendidikan, link_lowongan, portal_sumber)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(sql, (
        str(row["judul_posisi"]),
        str(row["nama_perusahaan"]),
        str(row["lokasi"]),
        str(row["pendidikan"]),
        str(row["link_lowongan"]),
        str(row["portal_sumber"]),
    ))

conn.commit()
cursor.close()
conn.close()

print(f"Berhasil import {len(df)} data ke MySQL Railway.")