import sqlite3

CONN = sqlite3.connect(":memory:")  # Use in-memory database for testing
CURSOR = CONN.cursor()
