import os
import mysql.connector
from mysql.connector import Error
import time

print("🚀 Démarrage application Northflank + MySQL")

# Affiche toutes les variables d'environnement
print("🔍 Variables d'environnement:")
for key, value in sorted(os.environ.items()):
    if 'MYSQL' in key:
        print(f"   {key}: {'*' * 8 if 'PASSWORD' in key else value}")

# Configuration MySQL
config = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

print(f"🔌 Tentative de connexion à MySQL...")
print(f"   Host: {config['host']}")
print(f"   Database: {config['database']}")
print(f"   User: {config['user']}")

try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("✅ CONNEXION MYSQL RÉUSSIE!")
        
        # Créer une table simple
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS demo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insérer une donnée
        cursor.execute("INSERT INTO demo (message) VALUES (%s)", ("Hello Northflank!",))
        connection.commit()
        
        # Lire les données
        cursor.execute("SELECT * FROM demo ORDER BY created_at DESC")
        results = cursor.fetchall()
        
        print("📊 Données dans la table:")
        for row in results:
            print(f"   ID: {row[0]}, Message: {row[1]}, Date: {row[2]}")
        
        connection.close()
        
except Error as e:
    print(f"❌ Erreur MySQL: {e}")
    print("💡 Vérifiez que l'addon MySQL est lié au service")

# Garder le service actif
print("🟢 Service actif - Appuyez sur Ctrl+C pour arrêter")
while True:
    time.sleep(60)
    print("❤️  Service en cours d'exécution...")
