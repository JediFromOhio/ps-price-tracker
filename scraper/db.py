import os

import psycopg2
from dotenv import load_dotenv

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


def get_last_price(conn, product_id):
    query = """
        SELECT current_price FROM price_history
        WHERE product_id = %s
        ORDER BY checked_at DESC
        LIMIT 1
    """
    with conn.cursor() as cur:
        cur.execute(query, (product_id,))
        row = cur.fetchone()
    
    return row[0] if row else None
