import sqlite3


class Database:
    def __init__(self,path : str):
        self.path = path

    def create_table(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                
                CREATE TABLE IF NOT EXISTS survey_result (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone_number VARCHAR(12),
                food_rating INTEGER,
                cleanliness_rating INTEGER,
                extra_comments TEXT,
                time_data DATA
                )
                """)
            conn.commit()

    def create_table_new_recipe(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """

                CREATE TABLE IF NOT EXISTS recipe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe TEXT,
                image VARCHAR(20),
                price INTEGER,
                category VARCHAR(15)
                )
                """)
            conn.commit()

    def save_survey(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    INSERT INTO survey_result (name, phone_number,food_rating,cleanliness_rating,extra_comments,time_data)
                    VALUES (?, ?, ?, ?, ?,?)
                """,
                (data["name"], data["phone_number"], data["food_rating"], data["cleanliness_rating"], data["extra_comments"], data["time_data"])
            )


    def save_recipe(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    INSERT INTO recipe (recipe, image,price, category) 
                    VALUES (?, ?, ?, ?)
                   
                """,
                (data["recipe"], data["image"], data["price"],data["category"])
            )