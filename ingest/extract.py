# Imports
import pandas as pd
import logging
import requests
import os
from dotenv import load_dotenv


# --- logging config ----------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- API KEY ------------------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("API_KEY")
# --- Extract Local files ------------------------------------------------------------

def extract_transacoes():
    try:
        logging.info("Starting transactions data extraction...")
        df = pd.read_csv("data/raw/transacoes_banco_angola.csv")
        logging.info("Data extracted sucessfully!")
        return df
    except Exception as e:
        logging.error(f"Data extraction failed: {e}")

def extract_clientes():
    try:
        logging.info("Staring clients data extraction...")
        df = pd.read_csv("data/raw/clientes_banco_angola.csv")
        logging.info("Data extracted sucessfully!")
        return df
    except Exception as e:
        logging.error(f"Data exctraction failed: {e}")

def extract_taxa_cambio():
    try:
        logging.info("Starting exchange rate data extraction...")
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD")
        data = response.json()

        # Changing json to dataframe
        taxas = data["conversion_rates"]
        data_atualizacao = pd.to_datetime(data["time_last_update_utc"])

        linhas = []
        for moeda, taxa in taxas.items():
            linhas.append({
                "moeda_base": data["base_code"],
                "moeda_destino": moeda,
                "taxa": taxa,
                "data": str(data_atualizacao)
            })

        df = pd.DataFrame(linhas)
        logging.info(f"Data extracted successfully! {len(df)} exchange rates")
        return df
    except Exception as e:
        logging.error(f"Data extraction from API failed: {e}")


if __name__ == "__main__":
    df_transacoes = extract_transacoes()
    df_clientes = extract_clientes()
    taxa_cambio_data = extract_taxa_cambio()

    logging.info("Data information")
    print(df_transacoes.head())
    print(df_clientes.head())
    print(taxa_cambio_data)