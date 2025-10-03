import mysql.connector
from mysql.connector import Error
from config import Config
import time
import sys

class MySQLManager:
    def __init__(self):
        self.connection = None
        self.config = Config.get_mysql_connection_string()
    
    def connect(self):
        """Établir la connexion à MySQL"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("✅ Connexion à MySQL établie avec succès")
                return True
        except Error as e:
            print(f"❌ Erreur de connexion: {e}")
            return False
    
    def disconnect(self):
        """Fermer la connexion"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Connexion MySQL fermée")
    
    def create_sample_table(self):
        """Créer une table d'exemple si elle n'existe pas"""
        try:
            cursor = self.connection.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            self.connection.commit()
            print("✅ Table 'users' créée ou déjà existante")
        except Error as e:
            print(f"❌ Erreur création table: {e}")
    
    def insert_sample_data(self):
        """Insérer des données d'exemple"""
        try:
            cursor = self.connection.cursor()
            
            # Données d'exemple
            users = [
                ('Alice Dupont', 'alice@email.com'),
                ('Bob Martin', 'bob@email.com'),
                ('Charlie Brown', 'charlie@email.com')
            ]
            
            insert_query = "INSERT IGNORE INTO users (name, email) VALUES (%s, %s)"
            cursor.executemany(insert_query, users)
            self.connection.commit()
            print(f"✅ {cursor.rowcount} utilisateurs insérés")
        except Error as e:
            print(f"❌ Erreur insertion données: {e}")
    
    def query_data(self):
        """Exécuter une requête SELECT"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users ORDER BY created_at DESC"
            cursor.execute(query)
            
            results = cursor.fetchall()
            
            print("\n📊 Résultats de la requête:")
            print("-" * 50)
            for row in results:
                print(f"ID: {row['id']}, Nom: {row['name']}, Email: {row['email']}, Créé le: {row['created_at']}")
            print("-" * 50)
            print(f"Total: {len(results)} utilisateurs trouvés")
            
            return results
        except Error as e:
            print(f"❌ Erreur requête: {e}")
            return []
    
    def get_database_info(self):
        """Obtenir des informations sur la base de données"""
        try:
            cursor = self.connection.cursor()
            
            # Version MySQL
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"🗄️  Version MySQL: {version[0]}")
            
            # Bases de données disponibles
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("📁 Bases de données disponibles:")
            for db in databases:
                print(f"  - {db[0]}")
                
        except Error as e:
            print(f"❌ Erreur info base de données: {e}")

def main():
    print("🚀 Démarrage du prototype MySQL Northflank")
    
    # Créer l'instance MySQL
    db_manager = MySQLManager()
    
    # Tentative de connexion avec retry
    max_retries = 5
    for attempt in range(max_retries):
        print(f"Tentative de connexion {attempt + 1}/{max_retries}...")
        if db_manager.connect():
            break
        if attempt < max_retries - 1:
            print("Attente 5 secondes avant réessai...")
            time.sleep(5)
    else:
        print("❌ Échec de connexion après plusieurs tentatives")
        sys.exit(1)
    
    try:
        # Opérations de base de données
        db_manager.get_database_info()
        db_manager.create_sample_table()
        db_manager.insert_sample_data()
        db_manager.query_data()
        
        # Garder le service actif pour les tests
        print("\n🔄 Service actif - Appuyez sur Ctrl+C pour arrêter")
        while True:
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé")
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    main()
