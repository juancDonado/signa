class Config:
    # Para Docker (puerto 5433) - coincidiendo con docker-compose.yml
    SQLALCHEMY_DATABASE_URI = "postgresql://signa:signa_pass@localhost:5433/signa_db"
    
    # Para PostgreSQL local (puerto 5432)
    # SQLALCHEMY_DATABASE_URI = "postgresql://signa:signa_db@localhost:5432/signa_db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False