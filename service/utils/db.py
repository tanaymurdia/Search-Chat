import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql, Error

admin_user = 'postgres'  # Typically, the default superuser is 'postgres'
admin_password = 'admin_password' # This one depends on what the admin password is when done the setup
host = 'localhost'
port = '5432'

db_name = 'db'
new_user = 'user'
new_password = 'pwd'

def setup_postgres():
    global admin_user 
    global admin_password
    global host 
    global port
    global db_name
    global new_user
    global new_password

    print(admin_user, admin_password, host, port, db_name, new_user, new_password)

    try:
        # Connect to PostgreSQL as superuser
        super_connection = psycopg2.connect(
            dbname='postgres',
            user=admin_user,
            password=admin_password,
            host=host,
            port=port
        )
        super_connection.autocommit = True
        super_cursor = super_connection.cursor()

        # Create a new database
        super_cursor.execute(sql.SQL(f"CREATE DATABASE {db_name};"))
        print(f"Database '{db_name}' created successfully.")

        # Create a new user
        super_cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(sql.Identifier(new_user)), [new_password])
        print(f"User '{new_user}' created successfully.")

        # Grant all privileges on the new database to the new user
        super_cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {};").format(sql.Identifier(db_name), sql.Identifier(new_user)))
        print(f"Granted all privileges on '{db_name}' to '{new_user}'.")

        # **Important**: Connect to the newly created database to modify schema permissions
        user_connection = psycopg2.connect(
            dbname=db_name,
            user=admin_user,  # Still needs to be a superuser to modify schema permissions
            password=admin_password,
            host=host,
            port=port
        )
        user_connection.autocommit = True
        user_cursor = user_connection.cursor()

        # Grant privileges specifically on the schema
        user_cursor.execute(sql.SQL("GRANT USAGE ON SCHEMA public TO {};").format(sql.Identifier(new_user)))
        user_cursor.execute(sql.SQL("GRANT CREATE ON SCHEMA public TO {};").format(sql.Identifier(new_user)))
        print(f"Granted schema usage and create privileges on 'public' to '{new_user}'.")

    except Error as err:
        print(f"Error: {err}")

    finally:
        # Close the connections
        if super_connection:
            super_cursor.close()
            super_connection.close()
            print("PostgreSQL superuser connection is closed.")
        if user_connection:
            user_cursor.close()
            user_connection.close()
            print("PostgreSQL user connection is closed.")


# Database connection function
def connect_db():
    return psycopg2.connect(
        dbname=db_name,
        user=new_user,
        password=new_password,
        host=host,
        port=port
    )


def create_tables():
    conn = connect_db()
    print("Current connection details:")
    print(f"dbname: {conn.get_dsn_parameters()['dbname']}")
    print(f"user: {conn.get_dsn_parameters()['user']}")
    print(f"host: {conn.get_dsn_parameters()['host']}")
    print(f"port: {conn.get_dsn_parameters()['port']}")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL);""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS Conversations (
                conversation_id SERIAL PRIMARY KEY,
                user_id SERIAL REFERENCES Users(user_id),
                start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_activity_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS Messages (
                message_id SERIAL PRIMARY KEY,
                conversation_id SERIAL REFERENCES Conversations(conversation_id),
                sender_type VARCHAR(4) CHECK (sender_type IN ('User', 'AI')),
                content TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );""")
            conn.commit()
    finally:
        conn.close()

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

