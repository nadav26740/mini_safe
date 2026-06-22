import sqlite3
from typing import Optional

# "const-like" names
TABLE_DATA_STORE = "data_store"
TABLE_METADATA = "metadata"

COLUMN_NAME = "name"
COLUMN_VALUE = "data"

ROW_DB_NAME = "db_name"
ROW_DB_VERSION = "db_version"
ROW_DB_PASSWORD_HASH = "salty_password"

DEFAULT_DB_VERSION = "0.1"
DEFAULT_DB_NAME = "mini_cryptodata.db"

class DataDB:
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def Connect(self) -> None:
        """Connect to the SQLite database."""
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path)

    def Close(self) -> None:
        """Close the database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def Table_Exists(self, table_name: str) -> bool:
        """Check whether a table exists."""
        if self.is_connected() is False:
            raise RuntimeError("Database is not connected.")

        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table'
            AND name = ?
            """,
            (table_name,),
        )

        return cursor.fetchone() is not None

    def verify_tables(self) -> bool:
        """Verify that the required tables exist."""
        return self.Table_Exists(TABLE_DATA_STORE) and self.Table_Exists(TABLE_METADATA)

    def Create_DB(
        self,
        salty_password: bytes,
        db_name: str = DEFAULT_DB_NAME,
        db_version: str = DEFAULT_DB_VERSION,
    ) -> None:
        """
        Creates:
            - data_store(name TEXT PRIMARY KEY, data BLOB)
            - metadata(db_name TEXT, db_version TEXT)
        """

        if self.is_connected() is False:
            raise RuntimeError("Database is not connected.")

        cursor = self._conn.cursor()

        # Main data table
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_DATA_STORE} (
                {COLUMN_NAME} TEXT PRIMARY KEY,
                {COLUMN_VALUE} BLOB NOT NULL
            )
            """
        )

        # Metadata table
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_METADATA} (
                {COLUMN_NAME} TEXT NOT NULL,
                {COLUMN_VALUE} TEXT NOT NULL
            )
            """
        )

        # Keep exactly one metadata row
        cursor.execute(f"DELETE FROM {TABLE_METADATA}")

        cursor.executemany(
            f"""
            INSERT INTO {TABLE_METADATA}
            (
                {COLUMN_NAME},
                {COLUMN_VALUE}
            )
            VALUES (?, ?)
            """,
            [
                (ROW_DB_NAME, db_name),
                (ROW_DB_VERSION, db_version),
                (ROW_DB_PASSWORD_HASH, salty_password.hex())
            ],
        )

        self._conn.commit()

    def Get_All_names_in_DB(self) -> list[str]:
        """Return all names from the data table."""
        
        if self.is_connected() is False:
            raise RuntimeError("Database is not connected.")
        
        cursor = self._conn.cursor()
        
        cursor.execute(
            f"""
            SELECT {COLUMN_NAME}
            FROM {TABLE_DATA_STORE}
            """
        )
        
        return [row[0] for row in cursor.fetchall()]

    def Get_data(self, name: str) -> Optional[str]:
        """Return data by name or None if not found."""
        
        if self.is_connected() is False:
            raise RuntimeError("Database is not connected.")
        
        cursor = self._conn.cursor()
        
        cursor.execute(
            f"""
            SELECT {COLUMN_VALUE}
            FROM {TABLE_DATA_STORE}
            WHERE {COLUMN_NAME} = ?
            """,
            (name,),
        )
        
        row = cursor.fetchone()
        
        return row[0] if row else None

    def Save_data(self, name: str, data: bytes) -> None:
        """Insert or update data."""
        
        if self.is_connected() is False:
            raise RuntimeError("Database is not connected.")
        
        cursor = self._conn.cursor()
        
        cursor.execute(
            f"""
            INSERT INTO {TABLE_DATA_STORE}
            (
                {COLUMN_NAME},
                {COLUMN_VALUE}
            )
            VALUES (?, ?)
            ON CONFLICT({COLUMN_NAME})
            DO UPDATE SET
                {COLUMN_VALUE} = excluded.{COLUMN_VALUE}
            """,
            (name, data),
        )

        self._conn.commit()

    def Get_Metadata(self) -> Optional[dict]:

        """Get database metadata."""

        if self.is_connected() is False:
            raise RuntimeError("Database is not connected.")

        cursor = self._conn.cursor()

        cursor.execute(
            f"""
            SELECT
                {COLUMN_NAME},
                {COLUMN_VALUE}
            FROM {TABLE_METADATA}
            """
        )

        rows = cursor.fetchall()

        if rows is None:
            return None

        output = dict()
        for row in rows:
            output[row[0]] = row[1]

        return output

    def is_connected(self) -> bool:
        """Check if the database connection is active."""
        return self._conn is not None    

    def delete_data(self, name) -> None:
        cursor = self._conn.cursor()
        
        cursor.execute(
            f"""
            DELETE FROM {TABLE_DATA_STORE}
            WHERE {COLUMN_NAME} = ?
        """,
        (name,)
        )

        self._conn.commit()