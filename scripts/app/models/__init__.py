from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
migrate = Migrate()


class Base(db.Model):
    """ Model that contains base database models. """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save_to_db(self):
        """ Saving into db """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, **kwargs):
        """  Updating into db """
        for key, value in kwargs.items():
            setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_from_db(self):
        """ Deleting from database """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        """ Find by id """
        return cls.query.filter_by(id=id).first()


class User(Base):
    __tablename__ = 'user'
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_disabled = db.Column(db.Boolean, default=False)
    user_info = db.relationship("UserInfo", cascade="delete", back_populates="user")
    clients = db.relationship("Client", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        """ Return the user data """
        return {
            "id": self.id,
            "email": self.email,
            "is_disabled": self.is_disabled,
        }

    def set_password(self, password):
        """ Setting password for user """
        self.password = generate_password_hash(password)

    def set_email_lower(self, email):
        """Setting the lowercase email"""
        self.email = email.lower()

    def check_password(self, password):
        """ Checking password for user """
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_email(cls, email):
        """ Find user by email address """
        email_lower = email.lower()
        return cls.query.filter_by(email=email_lower).first()

    @staticmethod
    def exists(email):
        """ Check if user exists """
        email_lower = email.lower()
        user = User.find_by_email(email_lower)
        if user:
            return True
        return False


class UserInfo(Base):
    __tablename__='user_info'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship("User", back_populates="user_info")

    def serialize(self):
        """ Return the user data """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "user_id": self.user_id,
        }
    
    def set_names(self, first_name, last_name):
        """ Set the first and last names with capitalized first letters. """
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()

    @classmethod
    def find_by_user_id(cls, user_id):
        """ Find by user_id """
        return cls.query.filter_by(user_id=user_id).first()


class Client(Base):
    __tablename__ = 'client'
    rut = db.Column(db.String(50), unique=True, nullable=False)
    razon_social = db.Column(db.String(255), nullable=False)
    actividad_economica = db.Column(db.String(255), nullable=False)
    n_adherente = db.Column(db.Integer, nullable=True)
    n_works = db.Column(db.Integer, nullable=True)
    is_disabled = db.Column(db.Boolean, default=False)
    centers = db.relationship("Center", back_populates="client", cascade="all, delete-orphan")
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="clients")

    def serialize(self):
        """ Return the client data """
        return {
            "id": self.id,
            "rut": self.rut,
            "razon_social": self.razon_social,
            "actividad_economica": self.actividad_economica,
            "n_adherente": self.n_adherente,
            "n_works": self.n_works,
            "is_disabled": self.is_disabled,
            "user_id": self.user_id,
        }

    def set_rut(self, rut):
        """Set the rut attribute, removing periods and hyphens"""
        cleaned_rut = rut.replace('.', '').replace('-', '')
        self.rut = cleaned_rut.lower()

    @classmethod
    def find_by_user_id(cls, user_id):
        """ Find by user_id """
        return cls.query.filter_by(user_id=user_id).all()


class Center(Base):
    __tablename__ = 'center'
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    comuna = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    n_works = db.Column(db.Integer, nullable=True)
    is_disabled = db.Column(db.Boolean, default=False)
    client_id = db.Column(db.Integer,  db.ForeignKey('client.id'), nullable=False)
    client = db.relationship("Client", back_populates="centers")

    def serialize(self):
        """ Return the center data """
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "comuna": self.comuna,
            "region": self.region,
            "n_works": self.n_works,
            "is_disabled": self.is_disabled,
            "client_id": self.client_id
        }

    @classmethod
    def find_by_client_id(cls, client_id):
        """ Find by user_id """
        return cls.query.filter_by(client_id=client_id).all()
