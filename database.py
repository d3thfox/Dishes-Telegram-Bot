import sqlite3



class Database:
    def __init__(self,path : str):
        self.path = path

    def create_table(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                
                CREATE TABLE IF NOT EXISTS review (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone_number VARCHAR(12),
                food_rating INTEGER,
                cleanliness_rating INTEGER,
                extra_comments TEXT,
                time_data DATA,
                user_id INTEGER
                )
                """)
            conn.commit()

    def create_table_new_recipe(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """

                CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                recipe TEXT,
                image VARCHAR(20),
                price FLOAT,
                category VARCHAR(15)
                )
                """)
            conn.commit()

    def save_survey(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    INSERT INTO review (name, phone_number,food_rating,cleanliness_rating,extra_comments,time_data,user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (data["name"], data["phone_number"], data["food_rating"], data["cleanliness_rating"], data["extra_comments"], data["time_data"],data["user_id"])
            )


    def save_recipe(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    INSERT INTO dishes (name, recipe, image, price, category) 
                    VALUES (?, ?, ?, ?, ?)
                   
                """,
                (data["name"], data["recipe"], data["image"], data["price"], data["category"])
            )
    def check_user_id(self, user_id):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM review WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            return user

    def random_rec(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT recipe,image FROM dishes ORDER BY RANDOM() LIMIT 1")
            random_recipe = cursor.fetchone()
            return random_recipe

    def select_catalog(self):
        with sqlite3.connect(self.path) as conn:
            result = conn.execute("SELECT name,price,image FROM dishes")
            result.row_factory = sqlite3.Row
            data = result.fetchall()

            return [dict(row) for row in data]