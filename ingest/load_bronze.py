# Imports
import pandas as pd
import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# --- Importing modules -------------------------------------------------------
from extract import extract_clientes, extract_taxa_cambio, extract_transacoes

# --- Logging config ----------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Enviroment variables ----------------------------------------------------
load_dotenv()
DB_URL = os.getenv("DB_URL")

# --- Database connection -----------------------------------------------------

def get_connection():
    try:
        logging.info("Getting database connection")
        engine = create_engine(DB_URL)
        logging.info("Database connected!")
        return engine
    except Exception as e:
        logging.error("Database connection failed")

# --- Create database schema --------------------------------------------------
def create_schema(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze;"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver;"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold;"))
            conn.commit()  # ← confirma as alterações
        logging.info("Schemas criados com sucesso!")
    except Exception as e:
        logging.error(f"Failed to create database schemas: {e}")
    


# --- Load module -------------------------------------------------------------

def load_data():
    try:
        # getting connection
        engine = get_connection()
        
        # creating schemas
        create_schema(engine)
                
        # getting data
        df_transacoes = extract_transacoes()
        df_clientes = extract_clientes()
        df_taxa_cambio = extract_taxa_cambio()

        # loading data
        df_transacoes.to_sql(
            "transacoes_raw",
            engine,
            schema = "bronze",
            if_exists = "replace",
            index = False
        )

        df_clientes.to_sql(
            "clientes_raw",
            engine,
            schema = "bronze",
            if_exists = "replace",
            index = False
        )

        df_taxa_cambio.to_sql(
            "taxas_cambio_raw",
            engine,
            schema = "bronze",
            if_exists = "replace",
            index = False
        )
        logging.info("Data loaded to the database sucessfully!")
    except Exception as e:
        logging.error(f"Failed loading to database: {e}")


if __name__ == "__main__":
    load_data()