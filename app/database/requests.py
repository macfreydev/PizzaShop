from app.database.db import async_session
from app.database.models import User, Pizza
from sqlalchemy import select, update, delete, desc


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()



async def add_pizza():
    async with async_session() as session:
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


pizzas = [
    {
        "name": "Peri Peri",
        "price": 12,
        "about": "Spicy Peri Peri chicken, onions, and signature sauce.",
        "image": "media/images/peri_peri.jpg",
        "size": "Medium",
        "onsale": True
    }, 
    {
        "name": "Vegetarian",
        "price": 10,
        "about": "Loaded with fresh vegetables and mozzarella cheese.",
        "image": "media/images/vegetarian.jpg",
        "size": "Large",
        "onsale": False
    },
    {
        "name": "Pepperoni",
        "price": 11,
        "about": "Classic pizza topped with delicious pepperoni slices.",
        "image": "media/images/pepperoni.jpg",
        "size": "Medium",
        "onsale": False
    },
    {
        "name": "Beef & Onion",
        "price": 13,
        "about": "Savory beef with caramelized onions and cheese.",
        "image": "media/images/beef_onion.jpg",
        "size": "Large",
        "onsale": False
    },
    {
        "name": "Barbecue",
        "price": 12,
        "about": "BBQ chicken, red onions, and mozzarella cheese.",
        "image": "media/images/barbecue.jpg",
        "size": "Medium",
        "onsale": True
    },
    {
        "name": "Chicken",
        "price": 11,
        "about": "Grilled chicken with cheese and tomato base.",
        "image": "media/media/images/chicken.jpg",
        "size": "Medium",
        "onsale": False
    },
    {
        "name": "Brightush",  # signature pizza
        "price": 14,
        "about": "House special with secret ingredients and a unique taste.",
        "image": "media/images/brightush.jpg",
        "size": "Large",
        "onsale": True
    },
    {
        "name": "Hawaiian",
        "price": 11,
        "about": "Classic ham and pineapple combination with mozzarella.",
        "image": "media/images/hawaiian.jpg",
        "size": "Medium",
        "onsale": False
    },
    {
        "name": "Buffalo",
        "price": 13,
        "about": "Spicy buffalo chicken with ranch drizzle and cheese.",
        "image": "media/images/buffalo.jpg",
        "size": "Large",
        "onsale": True
    },
    {
        "name": "Chicken & Mushroom",
        "price": 12,
        "about": "Grilled chicken with fresh mushrooms and mozzarella.",
        "image": "media/images/chicken_mushroom.jpg",
        "size": "Medium",
        "onsale": False
    },
    {
        "name": "Margherita",
        "price": 9,
        "about": "Classic tomato, mozzarella, and fresh basil.",
        "image": "media/images/margherita.jpg",
        "size": "Small",
        "onsale": False
    }
]



