import os
import time

print("🚀 APPLICATION NORTHFLANK - DÉMARRAGE")
print("=" * 50)

# Affiche TOUTES les variables d'environnement
print("📋 VARIABLES D'ENVIRONNEMENT:")
for key, value in sorted(os.environ.items()):
    print(f"   {key}: {value}")

print("=" * 50)

# Vérifie spécifiquement MySQL
mysql_vars = ['MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']
print("🔎 VARIABLES MYSQL:")
for var in mysql_vars:
    value = os.getenv(var)
    if value:
        print(f"   ✅ {var}: {'*' * 8 if 'PASSWORD' in var else value}")
    else:
        print(f"   ❌ {var}: NON DÉFINIE")

print("=" * 50)
print("🟢 SERVICE ACTIF - EN ATTENTE...")

# Garde le service vivant
counter = 0
while True:
    print(f"❤️  Heartbeat {counter} - Service en cours d'exécution")
    counter += 1
    time.sleep(10)
