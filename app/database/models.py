from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    points: Mapped[int] = mapped_column(default=0)


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_main: Mapped[bool] = mapped_column(default=False)


class Pizza(Base):
    __tablename__ = "pizzas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer, default=0)
    about: Mapped[str] = mapped_column(String(560))
    image: Mapped[str] = mapped_column(String(255))
    size: Mapped[str] = mapped_column(String(100))
    onsale: Mapped[bool] = mapped_column(default=False)


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pizza_id: Mapped[int] = mapped_column(ForeignKey("pizzas.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    size: Mapped[int] = mapped_column(Integer)


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pizza_id: Mapped[int] = mapped_column(ForeignKey("pizzas.id"))
    user_name: Mapped[str] = mapped_column(String(30))
    text: Mapped[str] = mapped_column(String(560), default="")
    rating: Mapped[int] = mapped_column(Integer, default=0)


class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    pizza_id: Mapped[int] = mapped_column(ForeignKey("pizzas.id"))
    rating: Mapped[int] = mapped_column(Integer, default=0)
