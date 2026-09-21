from database.db_connection import get_connection

def insert_item(title, category, public_description, campus, building, room, storage_bin, hidden_specifications, date_found, image_path=None):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed. Check your .env configuration."

    query = """
        INSERT INTO items (
            title, category, public_description, campus,
            building, room, storage_bin, hidden_specifications, date_found, image_path
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        title.strip(),
        category.strip(),
        public_description.strip(),
        campus.strip(),
        building.strip(),
        room.strip() if room else None,
        storage_bin.strip(),
        hidden_specifications.strip(),
        date_found.strip(),
        image_path
    )
    

    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        return True, "Item recorded successfully!"
    except Exception as err:
        conn.rollback()
        return False, f"Failed to insert item: {err}"
    finally:
        conn.close()