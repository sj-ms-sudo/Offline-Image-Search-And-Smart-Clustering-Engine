import sqlite3
from PIL import Image
from pathlib import Path
import os
import numpy as np
from collections import defaultdict
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    print("DB:", os.path.abspath(DB_PATH))
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            filename TEXT NOT NULL,
            width INTEGER,
            height INTEGER,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_id INTEGER NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            confidence REAL,
            FOREIGN KEY (image_id)
                REFERENCES images(id)
                ON DELETE CASCADE
        )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            face_id INTEGER NOT NULL,
            embedding_path TEXT NOT NULL,
            FOREIGN KEY (face_id)
                REFERENCES faces(id)
                ON DELETE CASCADE
            )
            """)

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clusters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cluster_id INTEGER NOT NULL,
                    image_path TEXT NOT NULL,
                    x INTEGER,
                    y INTEGER,
                    width INTEGER,
                    height INTEGER
                    )""")
        conn.commit()
        return "Database initialized , tables created successfully"
    except Exception as e:
        return f"Error creating database {e}"
    finally:
        conn.close()
        
def save_image_to_database(image):
    print("DB:", os.path.abspath(DB_PATH))
    if isinstance(image,tuple):
        image = image[0]
    image = Path(image).resolve()
    print(image.name,"Image name")
    print(image)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        Img = Image.open(image)
        width,height = Img.size
        cursor.execute("""
                       INSERT INTO images
                       (path,filename,width,height)
                       VALUES(?,?,?,?)
                       """,(str(image),image.name,width,height))
        
    except Exception as e:
        print(f"{image} failed")
        print(e)
        conn.close()
        return None
    conn.commit()
    image_id = cursor.lastrowid
    conn.close()        
    return image_id

def save_faces_to_database(face,image_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor=conn.cursor()
        x1, y1, x2, y2 = face.bbox
        x1 = int(x1)
        y1 = int(y1)
        width = int(x2) - x1
        height = int(y2) -  y1
        confidence = float(face.det_score)
        cursor.execute("""
                       INSERT INTO faces
                       (image_id,x,y,width,height,confidence)
                       VALUES(?,?,?,?,?,?)
                       """,(image_id,x1,y1,width,height,confidence))
        
    except Exception as e:
        print(f"{image_id} Failed")
        print(e)
        conn.close()
        return None
    conn.commit()
    face_id = cursor.lastrowid
    conn.close()
    return face_id

def save_embeddings_to_database(face_id,Embedding):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO embeddings
                       (face_id,embedding_path)
                       VALUES (?,?)
                       """,(face_id,str(Embedding)))
    except Exception as e:
        print(f"{face_id } with {Embedding } failed")
        print(e)
        conn.close()
        return None
    conn.commit()
    conn.close()

def print_a_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
    "SELECT embedding_path FROM embeddings WHERE face_id=?",
    (41,)
)

    path = cursor.fetchone()[0]

    embedding = np.load(path)
    print(embedding)
    
def show_nearest_images(indices):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    image_arr = []

    try:
        for embedding_id in indices[0]:
            if embedding_id == -1:
                continue
            embedding_id = int(embedding_id)+1
            cursor.execute(
                """
                SELECT images.path, images.filename ,faces.x,faces.y,faces.width,faces.height
                FROM images
                JOIN faces ON images.id = faces.image_id
                JOIN embeddings ON faces.id = embeddings.face_id
                WHERE embeddings.id = ?
                """,
                (embedding_id,)
            )

            row = cursor.fetchone()

            if row:
                image_arr.append(row)

        return image_arr

    finally:
        conn.close()

def get_image_path_by_embeddings(index):
    adjusted_id = int(index)+1
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                       SELECT images.path, faces.x, faces.y, faces.width, faces.height FROM images JOIN faces ON images.id = faces.image_id
                       JOIN embeddings ON faces.id = embeddings.face_id
                       WHERE embeddings.id = ?
                       """,(adjusted_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row
    return None

def add_cluster_to_database(cluster_id, face_data):
    try:
        path, x, y, w, h = face_data
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO clusters
                       (cluster_id, image_path, x, y, width, height)
                       VALUES(?,?,?,?,?,?)
                       """, (int(cluster_id), path, x, y, w, h))
    except Exception as e:
        print(f"Failed to add cluster {cluster_id}: {e}")
    finally:
        conn.commit()
        conn.close()

def get_images_by_cluster(cluster_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT image_path, x, y, width, height FROM clusters WHERE cluster_id = ?", (cluster_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_clusters():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clusters")
    conn.commit()
    conn.close()
    print("Old clusters cleared from database")

def show_cluster_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clusters")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def get_stats_from_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    image_count = cursor.execute("SELECT COUNT (*) FROM images").fetchone()[0]
    face_count = cursor.execute("SELECT COUNT (*) FROM faces").fetchone()[0]
    cluster_count = cursor.execute("SELECT COUNT (*) FROM (SELECT DISTINCT cluster_id FROM clusters)").fetchone()[0]
    indexed_vector_count = cursor.execute("SELECT COUNT (*) FROM clusters").fetchone()[0]
    return{
        "image_count":image_count,
        "face_count":face_count,
        "cluster_count":cluster_count,
        "indexed_vector_count":indexed_vector_count
    
    }

def drop_database_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS images")
    cursor.execute("DROP TABLE IF EXISTS faces")
    cursor.execute("DROP TABLE IF EXISTS embeddings")
    cursor.execute("DROP TABLE IF EXISTS clusters")
    conn.commit()
    conn.close()
    return
def get_all_clusters_from_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT image_path, cluster_id
    FROM (
        SELECT
            image_path,
            cluster_id,
            ROW_NUMBER() OVER (
                PARTITION BY cluster_id
                ORDER BY id
            ) AS rn
        FROM clusters
    )
    WHERE rn <= 4
    """)
    rows = cursor.fetchall()
    conn.close()
    clusters = defaultdict(list)
    for image_path,cluster_id in rows:
        clusters[cluster_id].append(image_path)
    return dict(clusters)
if __name__ == "__main__":
    show_cluster_table()

    print("Database initialized")