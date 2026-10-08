import sqlite3
from datetime import datetime


DATABASE_NAME = "finance_news.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            description TEXT,

            source TEXT,

            url TEXT UNIQUE,

            published TEXT,

            category TEXT,

            importance INTEGER,

            region TEXT,

            summary TEXT,

            why_it_matters TEXT,

            india_impact TEXT,

            market_impact TEXT,

            what_to_watch TEXT,

            created_at TEXT

        )
    """)

    conn.commit()
    conn.close()


def save_article(article):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO articles (
                title,
                description,
                source,
                url,
                published,
                category,
                importance,
                region,
                summary,
                why_it_matters,
                india_impact,
                market_impact,
                what_to_watch,
                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            article["title"],
            article["description"],
            article["source"],
            article["url"],
            article["published"],
            article["category"],
            article["importance"],
            article["region"],
            article["summary"],
            article["why_it_matters"],
            article["india_impact"],
            article["market_impact"],
            article["what_to_watch"],
            datetime.now().isoformat()

        ))

        conn.commit()

        inserted = True

    except sqlite3.IntegrityError:

        inserted = False

    conn.close()

    return inserted


def get_articles():

    conn = get_connection()

    query = """
        SELECT *
        FROM articles
        ORDER BY importance DESC, published DESC
    """

    df = __import__("pandas").read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


def clear_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM articles"
    )

    conn.commit()
    conn.close()