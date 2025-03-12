from app.database.db import async_session
from app.database.models import User, Pizza
from sqlalchemy import select, update, delete, desc
from app.database.data import pizzas


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()



async def add_pizza():
    async with async_session() as session:
        existing = await session.scalar(select(Pizza))
        if existing:
            return
            
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


