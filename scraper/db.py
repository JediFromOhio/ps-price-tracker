import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def save_price_record(conn, product_id, data):
    query = """
        INSERT INTO price_history
            (product_id, name, currency, base_price, discounted_price, current_price, end_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        product_id,
        data["name"],
        data["currency"],
        data["base_price"],
        data["discounted_price"],
        data["current_price"],
        data["end_time"],
    )

    with conn.cursor() as cur:
        cur.execute(query, values)
    conn.commit()

if __name__ == "__main__":
    conn = get_connection()
    print("Connected:", conn)
    conn.close()