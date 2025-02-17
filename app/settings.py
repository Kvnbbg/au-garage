import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration principale pour Flask."""
    
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    
    # Mode Debug sécurisé : Désactivé en production
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    # Protection contre les attaques CSRF
    WTF_CSRF_ENABLED = True

    # Protection contre les cookies malveillants
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Restriction des en-têtes de réponse pour la sécurité
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # Cache statique pour un an
    PREFERRED_URL_SCHEME = "https"

    # Dossiers pour les fichiers statiques et templates
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Journalisation pour la surveillance de l'application
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

    # Config de base pour Google Cloud Storage (si utilisé)
    GOOGLE_CLOUD_STORAGE_BUCKET = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "")

    # CORS (Cross-Origin Resource Sharing) pour API
    CORS_ALLOWED_ORIGINS = ["*"]

    # Base de données (Google Cloud SQL, SQLite, PostgreSQL, etc.)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google reCAPTCHA (si nécessaire)
    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", "")
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", "")

class ProductionConfig(Config):
    """Configuration pour la production."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    """Configuration pour le développement."""
    DEBUG = True

class TestingConfig(Config):
    """Configuration pour les tests."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# Mapping des configurations pour Flask
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
