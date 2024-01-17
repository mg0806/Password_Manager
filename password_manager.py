import mysql.connector
from getpass import getpass
from cryptography.fernet import Fernet, InvalidToken

# Function to establish a connection to the MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="manohar0806",
            database="password_manager",
        )

        if connection.is_connected():
            print(f"Connected to the MySQL database '{connection.database}'")
            return connection
        else:
            print("Connection failed.")
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the 'passwords' table if it doesn't exist
def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            website VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            password_encrypted BLOB NOT NULL
        )
    ''')

# Function to generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Function to save the encryption key to a file
def save_key_to_file(key):
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)

# Function to load the encryption key from a file
def load_key_from_file():
    try:
        with open("encryption_key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        return None

# Function to encrypt a password
def encrypt_password(cipher, password):
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password

# Function to decrypt a password
def decrypt_password(cipher, encrypted_password):
    try:
        decrypted_password = cipher.decrypt(encrypted_password).decode()
        print(decrypted_password)
        return decrypted_password
    except InvalidToken:
        print("Invalid token. Could not decrypt the password.")
        return None

# Function to add a new password to the database
def add_password(cursor, website, username, password, cipher):
    encrypted_password = encrypt_password(cipher, password)
    cursor.execute('''
        INSERT INTO passwords (website, username, password_encrypted)
        VALUES (%s, %s, %s)
    ''', (website, username, encrypted_password))

# Function to retrieve a password from the database
def get_password(cursor, website, username, cipher):
    cursor.execute('''
        SELECT password_encrypted FROM passwords
        WHERE website=%s AND username=%s
    ''', (website, username))
    result = cursor.fetchone()
    return result[0] if result else None

# Main function to run the password manager
def main():
    # Connect to the MySQL database
    connection = connect_to_database()

    # Check if the connection is successful
    if connection:
        cursor = connection.cursor()

        # Create the 'passwords' table
        create_table(cursor)

        # Load the encryption key from a file
        key = load_key_from_file()

        if key is None:
            # If the key is not available, generate a new key
            key = generate_key()
            # Save the key to a file for future use
            save_key_to_file(key)

        cipher = Fernet(key)

        print("Welcome to Your Password Manager")

        while True:
            
            print("\n1. Add Password\n2. Retrieve Password\n3. Exit")
            choice = input("Enter your choice (1/2/3): ")

            if choice == '1':
                website = input("Enter the website: ")
                username = input("Enter your username: ")
                password = getpass("Enter your password: ")
                
                add_password(cursor, website, username, password, cipher)
                connection.commit()
                print("Password added successfully!")

            elif choice == '2':
                website = input("Enter the website: ")
                username = input("Enter your username: ")

                encrypted_password = get_password(cursor, website, username, cipher)

                if encrypted_password:
                    decrypted_password = decrypt_password(cipher, encrypted_password)
                    if decrypted_password:
                        print("Retrieved decrypted password:", decrypted_password)
                else:
                    print("Password not found!")

            elif choice == '3':
                break

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        # Close the database connection when exiting
        cursor.close()
        connection.close()
        print("Goodbye!")

if __name__ == "__main__":
    main()
