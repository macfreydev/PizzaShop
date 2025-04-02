from app.database.data import reviews_start
from app.database.db import async_session
from app.database.models import Admin, Cart, Pizza, Review, User
from sqlalchemy import delete, func, select


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return inner  # returns the inner function


# User requests


@connection
async def set_user(session, tg_id):
    try:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
    except Exception as e:
        print(f"Error in set_user: {e}")
        return False

    return True


@connection
async def add_pizzas(session):
    try:
        result = await session.execute(select(func.count()).select_from(Pizza))
        count = result.scalar()

        if count > 0:
            return

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
    except Exception as e:
        print(f"Error in add_pizzas: {e}")
        return False

    return True


@connection
async def get_all_pizzas(session):
    try:
        result = await session.execute(select(Pizza))
        return result.scalars().all()
    except Exception as e:
        print(f"Error in get_all_pizzas: {e}")
        return None


@connection
async def get_pizza(session, pizza_id: int):
    try:
        result = await session.scalar(select(Pizza).where(Pizza.id == pizza_id))
        return result
    except Exception as e:
        print(f"Error in get_pizza: {e}")
        return None


@connection
async def delete_pizza(session, pizza_id: int):
    try:
        pizza = await session.get(Pizza, pizza_id)
        if pizza:
            await session.delete(pizza)
            await session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error in delete_pizza: {e}")
        return False


@connection
async def add_pizza(session, data: dict):
    try:
        new_pizza = Pizza(**data)
        session.add(new_pizza)
        await session.commit()
    except Exception as e:
        print(f"Error in add_pizza: {e}")


# Cart requests
@connection
async def add_to_cart(session, user_id: int, pizza_id: int, _size: int, _quantity: int):
    try:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        pizza = await session.scalar(select(Pizza).where(Pizza.id == pizza_id))
        if not user or not pizza:
            return False
        else:
            session.add(
                Cart(user_id=user.id, pizza_id=pizza.id, size=_size, quantity=_quantity)
            )
            await session.commit()
            return True
    except Exception as e:
        print(f"Error in add_to_cart: {e}")
        return False


@connection
async def add_quantity(session, cart_id: int):
    try:
        cart_item = await session.get(Cart, cart_id)
        if cart_item:
            cart_item.quantity += 1
            await session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error in add_quantity: {e}")
        return False


@connection
async def remove_quantity(session, cart_id: int):
    try:
        cart_item = await session.get(Cart, cart_id)
        if cart_item:
            cart_item.quantity -= 1
            await session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error in remove_quantity: {e}")
        return False


@connection
async def delete_cart_item(session, cart_id: int):
    try:
        query = delete(Cart).where(Cart.id == cart_id)
        result = await session.execute(query)
        await session.commit()

        if result.rowcount == 0:
            return False
        return True
    except Exception as e:
        print(f"Error in delete_cart_item: {e}")
        return False


@connection
async def get_cart(session, user_id: int):
    try:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        if user:
            return await session.scalars(select(Cart).where(Cart.user_id == user.id))
        return None
    except Exception as e:
        print(f"Error in get_cart: {e}")
        return None


@connection
async def check_cart(session, user_id: int):
    try:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        if user:
            cart = await session.scalar(select(Cart).where(Cart.user_id == user.id))
            return bool(cart)
        return False
    except Exception as e:
        print(f"Error in check_cart: {e}")
        return False


# Reviews
@connection
async def add_reviews(session):
    try:
        for review_data in reviews_start:  # Add redundent reviews
            review = Review(**review_data)
            session.add(review)
        await session.commit()
    except Exception as e:
        print(f"Error in add_reviews: {e}")


@connection
async def get_reviews(session, pizza_id: int):
    try:
        result = await session.execute(
            select(Review).where(Review.pizza_id == pizza_id)
        )
        return result.scalars().all()
    except Exception as e:
        print(f"Error in get_reviews: {e}")
        return []


@connection
async def get_all_reviews(session):
    try:
        result = await session.execute(select(Review))
        return result.scalars().all()
    except Exception as e:
        print(f"Error in get_all_reviews: {e}")
        return []


@connection
async def add_review(session, data: dict):
    try:
        new_review = Review(**data)
        session.add(new_review)
        await session.commit()
    except Exception as e:
        print(f"Error in add_review: {e}")


@connection
async def delete_pizza_reviews(session, pizza_id: int):
    try:
        reviews = await session.scalars(
            select(Review).where(Review.pizza_id == pizza_id)
        )
        for review in reviews:
            if review:
                await session.delete(review)
        await session.commit()
        return True
    except Exception as e:
        print(f"Error in delete_pizza_reviews: {e}")
        return False


@connection
async def count_reviews(session, pizza_id: int):
    try:
        result = await session.scalar(
            select(func.count(Review.id)).where(Review.pizza_id == pizza_id)
        )
        return result if result is not None else 0
    except Exception as e:
        print(f"Error in count_reviews: {e}")
        return 0


@connection
async def delete_user_reviews(session, user_id: int):
    try:
        reviews = await session.scalars(select(Review).where(Review.user_id == user_id))
        for review in reviews:
            if review:
                await session.delete(review)
        await session.commit()
        return True
    except Exception as e:
        print(f"Error in delete_user_reviews: {e}")
        return False


# Admin requests
async def add_admin(user_id: int):
    async with async_session() as session:
        session.add(Admin(user_id=user_id))
        await session.commit()


async def get_admin(user_id: int):
    async with async_session() as session:
        result = await session.scalar(select(Admin).where(Admin.user_id == user_id))
        return result


async def get_all_admins():
    async with async_session() as session:
        result = await session.execute(
            select(Admin, User).join(User, User.id == Admin.user_id)
        )

        admin_users = result.fetchall()
        return [user.tg_id for _, user in admin_users]


async def update_pizza_property(pizza_id: int, property_name: str, value):
    async with async_session() as session:
        pizza = await session.get(Pizza, pizza_id)
        if not pizza:
            return False

        # Update the specified property
        setattr(pizza, property_name, value)

        await session.commit()
        return True
