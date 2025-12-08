import mysql.connector
from mysql.connector import Error
from getpass import getpass
import hashlib
import bcrypt
import os 

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db"
        )
        return connection
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

#def list_users(connection):
    #try:
        #cursor = connection.cursor()
        #cursor.execute("SELECT id, username, created_at, is_active FROM users")
        #users = cursor.fetchall()
        
        #if not users:
            #print("Aucun utilisateur trouvé.")
            #return
            
        #print("\nListe des utilisateurs:")
        #print("-" * 60)
        #print(f"{'ID':<5} | {'Nom d\'utilisateur':<20} | {'Date de création':<20} | {'Statut'}")
        #print("-" * 60)
        #for user in users:
            #status = "Actif" if user[3] else "Inactif"
            #print(f"{user[0]:<5} | {user[1]:<20} | {str(user[2]):<20} | {status}")
        #print("-" * 60)
        
    #except Error as e:
        #print(f"Erreur lors de la récupération des utilisateurs: {e}")
    #finally:
        #if 'cursor' in locals():
            #cursor.close()

def login_user(connection):
    try:
        username = input("Nom d'utilisateur: ")
        password = getpass("Mot de passe: ")
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            print(f"\nConnexion réussie ! Bienvenue, {user['username']} !")
            return True
        else:
            print("\nErreur: Nom d'utilisateur ou mot de passe incorrect.")
            return False
            
    except Error as e:
        print(f"Erreur lors de la connexion: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()

def add_user(connection):
    try:
        username = input("Nouveau nom d'utilisateur: ")
        password = getpass("Nouveau mot de passe: ")
        
        #Vérifier si l'utilisateur existe déjà
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("Erreur: Ce nom d'utilisateur est déjà pris.")
            return
            
        # Hachage du mot de passe avec bcrypt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed.decode('utf-8'))
        )
        connection.commit()
        print("\nUtilisateur ajouté avec succès!")
        
    except Error as e:
        print(f"Erreur lors de l'ajout de l'utilisateur: {e}")
        connection.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()

def main():
    print("=== Gestion simple d'utilisateurs ===\n")
    
    # Connexion à la base de données
    connection = connect_to_db()
    if not connection:
        return
    
    try:
        while True:
            print("\nOptions:")
            #print("1. Lister les utilisateurs")
            print("1. Inscription")
            print("2. Login")
            print("3. Quitter")
            
            choice = input("\nVotre choix (1-4): ")
            
            if choice == '2':
                login_user(connection)
            elif choice == '1':
                add_user(connection)
            elif choice == '3':
                print("Au revoir!")
                break
            else:
                print("Option non valide. Veuillez réessayer.")
                
    finally:
        if connection.is_connected():
            connection.close()
            print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
