from homework__Chaika_Sergii__hw7__flask.application.services.db_cinnection import DBConnection


def create_table():
    with DBConnection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS phones (
                phone_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                contact_name VARCHAR NOT NULL,
                phone_value VARCHAR NOT NULL
            )
        """
        )
