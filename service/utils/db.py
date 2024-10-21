import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection function
def connect_db():
    return psycopg2.connect(
        dbname='db',
        user='user',
        password='pwd',
        host='localhost',
        port='5432'
    )


# def create_tables():
#     conn = connect_db()
#     print("Current connection details:")
#     print(f"dbname: {conn.get_dsn_parameters()['dbname']}")
#     print(f"user: {conn.get_dsn_parameters()['user']}")
#     print(f"host: {conn.get_dsn_parameters()['host']}")
#     print(f"port: {conn.get_dsn_parameters()['port']}")
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
#                 user_id SERIAL PRIMARY KEY,
#                 username VARCHAR(255) UNIQUE NOT NULL,
#                 password VARCHAR(255) NOT NULL);""")
#             cursor.execute("""CREATE TABLE IF NOT EXISTS Conversations (
#                 conversation_id SERIAL PRIMARY KEY,
#                 user_id SERIAL REFERENCES Users(user_id),
#                 start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#                 last_activity_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
#             );""")
#             cursor.execute("""CREATE TABLE IF NOT EXISTS Messages (
#                 message_id SERIAL PRIMARY KEY,
#                 conversation_id SERIAL REFERENCES Conversations(conversation_id),
#                 sender_type VARCHAR(4) CHECK (sender_type IN ('User', 'AI')),
#                 content TEXT NOT NULL,
#                 timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
#             );""")
#             conn.commit()
#     finally:
#         conn.close()

def delete_table(table_name):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE " + table_name)
            conn.commit()
    finally:
        conn.close()

# Function to add a new user
def get_all_users():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * from Users""")
            print(cursor)
            table = cursor.fetchall()
            print(table)
            conn.commit()
            return table
    finally:
        conn.close()

# Function to add a new user
def add_user(username, plain_password):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id", (username, plain_password))
            user_id = cursor.fetchone()[0]
            conn.commit()
            return user_id
    finally:
        conn.close()

# Function to authenticate a user
def authenticate_user(username, plain_password):
    conn = connect_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and (plain_password == user['password']):
                print("Authentication successful")
                return True, user['user_id']
            else:
                print("Authentication failed")
                return False, None
    finally:
        conn.close()

# Function to start a new conversation
def start_conversation(user_id):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Conversations (user_id) VALUES (%s) RETURNING conversation_id", (user_id,))
            conversation_id = cursor.fetchone()[0]
            conn.commit()
            return conversation_id
    finally:
        conn.close()

# Function to add a new message
def add_message(conversation_id, sender_type, content):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Messages (conversation_id, sender_type, content) VALUES (%s, %s, %s) RETURNING message_id",
                (conversation_id, sender_type, content)
            )
            message_id = cursor.fetchone()[0]
            cursor.execute(
                "UPDATE Conversations SET last_activity_time = CURRENT_TIMESTAMP WHERE conversation_id = %s",
                (conversation_id,)
            )
            conn.commit()
            return message_id
    finally:
        conn.close()

# Function to get conversation history
def get_conversation_history(conversation_id):
    conn = connect_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Messages WHERE conversation_id = %s ORDER BY timestamp ASC", (conversation_id,))
            messages = cursor.fetchall()
            return [dict(row) for row in messages]
    finally:
        conn.close()

# Function to get conversation_ids for user_id
def get_conversation_ids_for_user(user_id):
    try:
        conn = connect_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT conversation_id FROM Conversations WHERE user_id = %s", (user_id,))
            conversations = cursor.fetchall()
            
            conversation_ids = [conversation['conversation_id'] for conversation in conversations]
            
            return conversation_ids
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()

