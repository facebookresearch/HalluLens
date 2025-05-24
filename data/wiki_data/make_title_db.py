# Copyright (c) Meta Platforms, Inc. and affiliates.

# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
from tasks.longwiki.retrieval import DocDB
import sqlite3
import argparse

def get_titles_all(db):
    # get all titles only
    cursor = db.connection.cursor()
    cursor.execute("SELECT title FROM documents")
    results = cursor.fetchall()
    results_title = [r[0] for r in results]
    cursor.close()
    return results_title

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki_db_path", type=str, default="data/wiki_data/.cache/enwiki-20230401.db")
    args = parser.parse_args()

    db_path=args.wiki_db_path
    db_title_path=db_path.replace(".db", "-title.db")
    db_data_path=db_path.replace(".db", ".jsonl")        
    db = DocDB(db_path=db_path, data_path=db_data_path)

    # Step 1: Get all titles
    titles = get_titles_all(db)

    # Step 2: Create an SQLite database connection
    conn = sqlite3.connect(db_title_path)
    cursor_ = conn.cursor()

    # Step 3: Create a table to store the titles
    cursor_.execute('''
    CREATE TABLE IF NOT EXISTS titles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_name TEXT NOT NULL
    );
    ''')

    # Step 4: Insert data from the list into the table
    cursor_.executemany('''
    INSERT INTO titles (title_name) VALUES (?)
    ''', [(title,) for title in titles])  # Tuple format for each title

    # Commit the changes and close the connection
    conn.commit()

    # Step 5: Verify the data by selecting and printing
    cursor_.execute("SELECT * FROM titles")
    i = 0
    for row in cursor_.fetchall():
        print(row)
        i +=1
        if i > 10:
            break

    # Close the connection
    conn.close()
