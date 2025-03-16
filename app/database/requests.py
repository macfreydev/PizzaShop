from app.database.db import async_session
from app.database.models import User, Pizza, Admin, Cart
from sqlalchemy import select
from app.database.data import pizzas

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
                size=pizza["size"],
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
        cart_item = await session.get(Cart, cart_id)
        if cart_item:
            session.delete(cart_item)
            await session.commit()
            return True
        return False

async def get_cart(user_id: int):
    async with async_session() as session:
       return await session.scalars(select(Cart).where(Cart.user_id == user_id))
        

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


