
import os

import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def get_connection():
    """Create and return a SQL Server database connection."""

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER")
    trusted_connection = os.getenv("DB_TRUSTED_CONNECTION")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection={trusted_connection};"
        "TrustServerCertificate=yes;"
    )

    connection = pyodbc.connect(connection_string)

    return connection
