import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """)
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS dogs")
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
        conn.commit()
        self.id = cursor.lastrowid  
        conn.close()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, data):
        id, name, breed = data
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dogs")
        data = cursor.fetchall()
        conn.close()
        return [cls.new_from_db(row) for row in data]

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dogs WHERE name=?", (name,))
        data = cursor.fetchone()
        conn.close()
        if data:
            return cls.new_from_db(data)
        return None

    @classmethod
    def find_by_id(cls, id):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dogs WHERE id=?", (id,))
        data = cursor.fetchone()
        conn.close()
        if data:
            return cls.new_from_db(data)
        return None

    def update(self):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE dogs SET name=? WHERE id=?", (self.name, self.id))
        conn.commit()
        conn.close()
