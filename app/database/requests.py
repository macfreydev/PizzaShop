import logging
from functools import wraps

from sqlalchemy import delete, func, select

from app.database.data import reviews_start
from app.database.db import async_session
from app.database.exceptions import DatabaseError
from app.database.models import Admin, Cart, Pizza, Review, User

logger = logging.getLogger(__name__)


def connection(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        try:
            async with async_session() as session:
                return await func(session, *args, **kwargs)
        except Exception as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            raise DatabaseError(f"Failed in {func.__name__}: {str(e)}")

    return inner


# User requests


@connection
async def set_user(session, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        session.add(User(tg_id=tg_id))
        await session.commit()
    return True


@connection
async def add_pizzas(session):
    result = await session.execute(select(func.count()).select_from(Pizza))
    count = result.scalar()

    if count > 0:
        return True

    from app.database.data import pizzas

    for pizza_data in pizzas:
        if "size" not in pizza_data or pizza_data["size"] is None:
            pizza_data["size"] = "Medium"

        pizza = Pizza(
            name=pizza_data["name"],
            price=pizza_data["price"],
            about=pizza_data["about"],
            image=pizza_data["image"],
            size=pizza_data["size"],
            onsale=pizza_data["onsale"],
        )
        session.add(pizza)

    await session.commit()
    return True


@connection
async def get_all_pizzas(session):
    result = await session.execute(select(Pizza))
    return result.scalars().all()


@connection
async def get_pizza(session, pizza_id: int):
    result = await session.scalar(select(Pizza).where(Pizza.id == pizza_id))
    return result


@connection
async def delete_pizza(session, pizza_id: int):
    pizza = await session.get(Pizza, pizza_id)
    if pizza:
        await session.delete(pizza)
        await session.commit()
        return True
    return False


@connection
async def add_pizza(session, data: dict):
    new_pizza = Pizza(**data)
    session.add(new_pizza)
    await session.commit()
    return True


# Cart requests
@connection
async def add_to_cart(session, user_id: int, pizza_id: int, _size: int, _quantity: int):
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    pizza = await session.scalar(select(Pizza).where(Pizza.id == pizza_id))
    if not user or not pizza:
        return False

    session.add(
        Cart(user_id=user.id, pizza_id=pizza.id, size=_size, quantity=_quantity)
    )
    await session.commit()
    return True


@connection
async def add_quantity(session, cart_id: int):
    cart_item = await session.get(Cart, cart_id)
    if cart_item:
        cart_item.quantity += 1
        await session.commit()
        return True
    return False


@connection
async def remove_quantity(session, cart_id: int):
    cart_item = await session.get(Cart, cart_id)
    if cart_item:
        cart_item.quantity -= 1
        await session.commit()
        return True
    return False


@connection
async def delete_cart_item(session, cart_id: int):
    query = delete(Cart).where(Cart.id == cart_id)
    result = await session.execute(query)
    await session.commit()

    if result.rowcount == 0:
        return False
    return True


@connection
async def get_cart(session, user_id: int):
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    if user:
        return await session.scalars(select(Cart).where(Cart.user_id == user.id))
    return None


@connection
async def check_cart(session, user_id: int):
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    if user:
        cart = await session.scalar(select(Cart).where(Cart.user_id == user.id))
        return bool(cart)
    return False


# Reviews
@connection
async def add_reviews(session):
    for review_data in reviews_start:
        review = Review(**review_data)
        session.add(review)
    await session.commit()
    return True


@connection
async def get_reviews(session, pizza_id: int):
    result = await session.execute(select(Review).where(Review.pizza_id == pizza_id))
    return result.scalars().all()


@connection
async def get_all_reviews(session):
    result = await session.execute(select(Review))
    return result.scalars().all()


@connection
async def add_review(session, data: dict):
    new_review = Review(**data)
    session.add(new_review)
    await session.commit()
    return True


@connection
async def delete_pizza_reviews(session, pizza_id: int):
    reviews = await session.scalars(select(Review).where(Review.pizza_id == pizza_id))
    for review in reviews:
        if review:
            await session.delete(review)
    await session.commit()
    return True


@connection
async def count_reviews(session, pizza_id: int):
    result = await session.scalar(
        select(func.count(Review.id)).where(Review.pizza_id == pizza_id)
    )
    return result if result is not None else 0


@connection
async def delete_user_reviews(session, user_id: int):
    reviews = await session.scalars(select(Review).where(Review.user_id == user_id))
    for review in reviews:
        if review:
            await session.delete(review)
    await session.commit()
    return True


# Admin requests
@connection
async def add_admin(session, user_id: int):
    session.add(Admin(user_id=user_id))
    await session.commit()
    return True


@connection
async def get_admin(session, user_id: int):
    result = await session.scalar(select(Admin).where(Admin.user_id == user_id))
    return result


@connection
async def get_all_admins(session):
    result = await session.execute(
        select(Admin, User).join(User, User.id == Admin.user_id)
    )
    admin_users = result.fetchall()
    return [user.tg_id for _, user in admin_users]


@connection
async def update_pizza_property(session, pizza_id: int, property_name: str, value):
    pizza = await session.get(Pizza, pizza_id)
    if not pizza:
        return False

    setattr(pizza, property_name, value)
    await session.commit()
    return True


@connection
async def add_new_pizza(session, name, price, about, image, size, onsale):
    pizza = Pizza(
        name=name, price=price, about=about, image=image, size=size, onsale=onsale
    )
    session.add(pizza)
    await session.commit()
    return True
