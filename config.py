import os
import sys
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuration MySQL depuis les variables d'environnement Northflank
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    
    @classmethod
    def validate_config(cls):
        """Valide que toutes les variables MySQL sont présentes"""
        required_vars = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']
        missing = [var for var in required_vars if not getattr(cls, var)]
        
        if missing:
            print("❌ VARIABLES MYSQL MANQUANTES:")
            for var in missing:
                print(f"   - {var}")
            print("\n💡 SOLUTION:")
            print("   1. Allez dans votre service Northflank")
            print("   2. Cliquez sur 'Addons' ou 'Settings' → 'Addons'")
            print("   3. 'Link Addon' → Sélectionnez votre MySQL")
            print("   4. Redéployez")
            return False
        return True
    
    @classmethod
    def get_mysql_connection_string(cls):
        return {
            'host': cls.MYSQL_HOST,
            'port': cls.MYSQL_PORT,
            'user': cls.MYSQL_USER,
            'password': cls.MYSQL_PASSWORD,
            'database': cls.MYSQL_DATABASE
        }
