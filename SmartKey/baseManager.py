import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import (
    contextmanager,
) 


Base = declarative_base()

engine = db.create_engine("sqlite:///lista_korisnika.db")

Session = sessionmaker()
Session.configure(bind=engine)

users = db.Table(
    "users",
    Base.metadata,
    db.Column("id_num", db.Integer),
    db.Column("ime", db.String),
    db.Column("prezime", db.String),
    db.Column("pin", db.Integer),
    db.Column("aktivan", db.Boolean)
)

class Korisnik(Base):
    __tablename__ = users

    id_num = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String, nullable=False)
    prezime = db.Column(db.String, nullable=False)
    pin = db.Column(db.Integer, nullable=False)
    aktivan = db.Column(db.Boolean, nullable=False)


@contextmanager
def get_db():
    session = Session()

    try:
        yield session
    finally:
        session.close()


def delete_db():
    try:
        with get_db() as session:
            for table in reversed(Base.metadata.sorted_tables):
                session.execute(table.delete())

            session.commit()
            session.close()
    
    except Exception:
        session.rollback()

def add_user(id_num, ime, prezime, pin, aktivan):
    global complete_check
    
    try:
        complete_check = 0

        with get_db() as session:

            korisnik = (
                session.query(Korisnik).filter(db.or_(Korisnik.id_num == id_num, Korisnik.ime == ime, Korisnik.pin == pin)).one_or_none()
            )
        
            if korisnik is None:
                korisnik = Korisnik(id_num=id_num, ime=ime, prezime=prezime, pin=pin, aktivan=aktivan) 
        
                session.add(korisnik)
                session.commit()
            else:
                complete_check += 1
                    
            session.close()

    except Exception:
        session.rollback()

    return complete_check
        
def delete_user(user_id):

    try:
        with get_db() as session:

            session.execute(
                db.delete(users)
                .where(users.c.id_num == user_id)
                )

            session.commit()
            session.close()

    except Exception:
        session.rollback()

def update_user(user_id, ime, prezime, pin, aktivan):

    try:
        with get_db() as session:

            session.execute(
                db.update(users)
                .where(users.c.id_num == user_id)
                .values(ime=ime, prezime=prezime, pin=pin, aktivan=aktivan)
            )

            session.commit()
            session.close()

    except Exception:
        session.rollback()

def create_admin():

        add_user(
            id_num=0,
            ime="Admin",
            prezime="Adminski",
            pin=8888,
            aktivan=True
        )

if __name__ == "__main__":
    Base.metadata.create_all(engine)





