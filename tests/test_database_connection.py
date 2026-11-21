from src.ingestion.database import get_connection


def test_database_connection():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT DB_NAME()")

    database_name = cursor.fetchone()[0]

    print(f"Successfully connected to: {database_name}")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    test_database_connection()
