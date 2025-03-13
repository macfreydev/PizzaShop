from app.database.db import async_session
from app.database.models import User, Pizza, Admin
from sqlalchemy import select
from app.database.data import pizzas



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
