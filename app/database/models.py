from sqlalchemy import ForeignKey, String, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=True)
    
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    points: Mapped[int] = mapped_column(default=0)



class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    is_main: Mapped[bool] = mapped_column(default=False)


class Pizza(Base):
    __tablename__ = 'pizzas'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer, default=0)
    about: Mapped[str] = mapped_column(String(560))
    image: Mapped[str] = mapped_column(String(255))
    size: Mapped[str] = mapped_column(String(15))
    onsale: Mapped[bool] = mapped_column(default=False)


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    pizza_id: Mapped[int] = mapped_column(ForeignKey('pizzas.id'))
    quantity: Mapped[int] = mapped_column(default=1)


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id')) 
    pizza_id: Mapped[int] = mapped_column(ForeignKey('pizzas.id'))
    text: Mapped[str] = mapped_column(String(560))
    rating: Mapped[int] = mapped_column(Integer, default=0)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)