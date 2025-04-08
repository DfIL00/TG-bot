from core.database import Database

if __name__ == "__main__":
    db = Database()
    print("Database created successfully!")
    db.close()