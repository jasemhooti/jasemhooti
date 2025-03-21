from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

from config import DATABASE_FILE

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    balance = Column(Float, default=0.0)
    is_admin = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    # ... سایر فیلدهای مورد نیاز

class VPNPackage(Base):
    __tablename__ = 'vpn_packages'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    size_gb = Column(Integer)
    price = Column(Integer)
    description = Column(String, nullable=True)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    package_id = Column(Integer, ForeignKey('vpn_packages.id'))
    order_date = Column(DateTime, default=datetime.utcnow)
    payment_status = Column(String, default="pending") # pending, paid, confirmed, rejected
    receipt_photo_id = Column(String, nullable=True)
    admin_confirmed = Column(Boolean, default=False)
    admin_confirmation_date = Column(DateTime, nullable=True)
    xui_config_id = Column(String, nullable=True) # ID کانفیگ در پنل X-UI
    # ... سایر فیلدهای مورد نیاز

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="open") # open, closed
    subject = Column(String)
    message = Column(String)
    admin_reply = Column(String, nullable=True)
    replied_at = Column(DateTime, nullable=True)

class DiscountCode(Base):
    __tablename__ = 'discount_codes'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, index=True)
    discount_percentage = Column(Float)
    is_active = Column(Boolean, default=True)
    expiry_date = Column(DateTime, nullable=True)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey('users.id'))
    player2_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    bet_amount = Column(Integer)
    player1_choice = Column(Integer, nullable=True)
    player2_choice = Column(Integer, nullable=True)
    player1_guess = Column(Integer, nullable=True)
    player2_guess = Column(Integer, nullable=True)
    status = Column(String, default="waiting") # waiting, ongoing, finished, abandoned
    winner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

engine = create_engine(f'sqlite:///{DATABASE_FILE}')
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
