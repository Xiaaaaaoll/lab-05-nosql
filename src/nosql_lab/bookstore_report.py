#!/usr/bin/env python3
"""Print a bookstore inventory report from MongoDB Atlas.

For each author in a list, print the author's name followed by the title and
publication year of every book that lists that author in ``author_ids``.
"""

import logging
import os

from pymongo import MongoClient

# Credentials come from the environment, never hardcoded
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Authors to report on: author_002 and author_003 come from authors.json,
# author_004 was added in Case Study 1, step 7
AUTHOR_IDS = ["author_002", "author_003", "author_004"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def print_report(authors, books, author_ids):
    """Print each author's name and their linked books.

    Args:
        authors: The ``authors`` collection.
        books: The ``books`` collection.
        author_ids: List of author ``_id`` values to include.
    """
    # Number of authors in the list that exist in the collection
    count = authors.count_documents({"_id": {"$in": author_ids}})
    print(f"Authors: {count}")

    for author in authors.find({"_id": {"$in": author_ids}}).sort("_id"):
        print(f"\n{author['name']}")
        # Join: every book whose author_ids contains this author's _id
        for book in books.find({"author_ids": author["_id"]}).sort("published_year"):
            print(f"  {book['title']} ({book['published_year']})")


def main():
    """Connect to MongoDB Atlas and print the bookstore report."""
    try:
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        # Force a round trip so connection problems surface here
        client.admin.command("ping")
        logger.info("Connected to MongoDB Atlas")

        db = client["bookstore"]
        print_report(db["authors"], db["books"], AUTHOR_IDS)

        client.close()
        logger.info("Connection closed")
    except Exception as e:
        logger.error(f"MongoDB error: {e}")


if __name__ == "__main__":
    main()
