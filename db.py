import psycopg2
from sqlalchemy import create_engine
import os
import pandas as pd

def get_db_engine():
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)
    return engine



def format_dataframe(df):
    # Format price with dollar sign
    df['price'] = df['price'].apply(lambda x: f"${x:.2f}")
    # Replace rating strings with star emojis
    rating_conversion = {
        'One': '⭐',
        'Two': '⭐⭐',
        'Three': '⭐⭐⭐',
        'Four': '⭐⭐⭐⭐',
        'Five': '⭐⭐⭐⭐⭐'
    }
    df['rating'] = df['rating'].map(rating_conversion)
    # Display in-stock with a green check mark
    df['in_stock'] = df['in_stock'].apply(lambda x: '✔️' if x else 'Out of stock')
    return df



class Database:
    def __init__(self, url):
        self.conn = psycopg2.connect(url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255),
                    price REAL,
                    rating VARCHAR(10),
                    in_stock BOOLEAN
                );
            ''')
            self.conn.commit()

    def insert_book(self, book):
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO books (title, price, rating, in_stock)
                VALUES (%s, %s, %s, %s)
            ''', (book['title'], book['price'], book['rating'], book['in_stock']))
            self.conn.commit()
