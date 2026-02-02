from db.database import engine, Base
import db.models  # IMPORTANT: ensures models are registered

def init_db():
    Base.metadata.create_all(bind=engine)
