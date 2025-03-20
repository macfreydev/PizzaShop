from app.database.db import async_session
from app.database.models import User, Pizza, Admin, Cart, Review, Rating
from sqlalchemy import func, select, delete
from app.database.data import pizzas, reviews_start

def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner  # returns the inner function

# User requests

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

# Pizza requests
async def add_pizzas():
    async with async_session() as session:
        existing = await session.scalar(select(Pizza))
        if existing:
            pass
            
        for pizza in pizzas:
            new_pizza = Pizza(
                name=pizza["name"],
                price=pizza["price"],
                about=pizza["about"],
                image=pizza["image"],
                onsale=pizza["onsale"]
            )
            session.add(new_pizza)
        await session.commit() 


async def get_all_pizzas():
    async with async_session() as session:
        result = await session.execute(select(Pizza))
        return result.scalars().all()

  
async def get_pizza(id: int):
    async with async_session() as session:
        result = await session.scalar(
            select(Pizza).where(Pizza.id == id)
        )
        return result
    
async def delete_pizza(pizza_id: int):
    async with async_session() as session:
        pizza = await session.get(Pizza, pizza_id)
        if pizza:
            await session.delete(pizza)
            await session.commit()
            return True
        return False
    
async def add_pizza(data: dict):
    async with async_session() as session:
        new_pizza = Pizza(**data)
        session.add(new_pizza)
        await session.commit()


#Cart requests
async def add_to_cart(user_id: int, pizza_id: int, _size: int, _quantity: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        pizza = await session.scalar(select(Pizza).where(Pizza.id == pizza_id))
        if not user or not pizza:
            return False
        else:
            session.add(Cart(user_id=user.id, pizza_id=pizza.id, size=_size, quantity=_quantity))
            await session.commit()
            return True

async def add_quantity(cart_id: int):
    async with async_session() as session:
        cart_item = await session.get(Cart, cart_id)
        if cart_item:
            cart_item.quantity += 1
            await session.commit()
            return True
        return False
    
    
async def remove_quantity(cart_id: int):
    async with async_session() as session:
        cart_item = await session.get(Cart, cart_id)
        if cart_item:
            cart_item.quantity -= 1
            await session.commit()
            return True
        return False
    

async def delete_cart_item(cart_id: int): 
    async with async_session() as session:
        query = delete(Cart).where(Cart.id == cart_id)
        result = await session.execute(query)  
        await session.commit()

        if result.rowcount == 0:  # If no rows were deleted, the item wasn't in the cart
            return False
        return True
    
async def get_cart(user_id: int):
    async with async_session() as session:
       user = await session.scalar(select(User).where(User.tg_id == user_id))
       return await session.scalars(select(Cart).where(Cart.user_id == user.id))
        

async def check_cart(user_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        cart = await session.scalar(select(Cart).where(Cart.user_id == user.id))
        
        if not cart:
            return False 
        return True
    
# Reviews 
async def add_reviews():
    async with async_session() as session:
        for review_data in reviews_start:
            
            review = Review(**review_data)
            session.add(review)
        await session.commit()

async def get_reviews(pizza_id: int):
    async with async_session() as session:
        return (await session.execute(select(Review).where(Review.pizza_id == pizza_id))).scalars().all()
    
async def get_all_reviews():
    async with async_session() as session:
        return (await session.execute(select(Review))).scalars().all()

async def add_review(data : dict):
    async with async_session() as session:
        new_review = Review(**data)
        session.add(new_review)
        await session.commit()


async def delete_pizza_reviews(pizza_id: int):
    async with async_session() as session:
        reviews = await session.scalars(select(Review).where(Review.pizza_id == pizza_id))
        for review in reviews:
            if review:
                await session.delete(review)
            await session.commit()
            return True
        return False



async def count_reviews(pizza_id: int):
    async with async_session() as session:
        result = await session.scalar(select(func.count(Review.id)).where(Review.pizza_id == pizza_id))
        return result if result is not None else 0

async def delete_user_reviews(user_id: int):
    async with async_session() as session:
        reviews = await session.scalars(select(Review).where(Review.pizza_id == user_id))
        for review in reviews:
            if review:
                await session.delete(review)
            await session.commit()
            return True
        return False


# Admin requests
async def add_admin(user_id: int):
    async with async_session() as session:
        session.add(Admin(user_id=user_id))
        await session.commit()

async def get_admin(user_id: int):
    async with async_session() as session:
        result = await session.scalar(
            select(Admin).where(Admin.user_id == user_id)
        )
        return result
    
async def get_all_admins():
    async with async_session() as session:
        result = await session.execute(
            select(Admin, User)
            .join(User, User.id == Admin.user_id)
        )
        
        admin_users = result.fetchall()
        return [user.tg_id for _, user in admin_users]


