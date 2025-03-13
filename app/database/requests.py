from app.database.models import async_session
from app.database.models import User, Pizza
from sqlalchemy import select, insert, delete, update


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner  


@connection
async def set_user(session, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    
    if not user:
        session.add(User(tg_id=tg_id))
        await session.commit()


# did this to fill the database but instead of the path to phototos you need to do that functiojn to get urls, i already have it in the user file.
pizzas = [
    {
        "name": "Peri Peri",
        "price": 12,
        "about": "Spicy Peri Peri chicken, onions, and signature sauce.",
        "image": "AgACAgIAAxkBAANZZ9F80c3CCizmBYlW-2KHsqDxlfcAAq7uMRuSg5BKkNIaS77nqi8BAAMCAAN4AAM2BA",
        "size": "Medium",
        "onsale": True
    }, 
    {
        "name": "Vegetarian",
        "price": 10,
        "about": "Loaded with fresh vegetables and mozzarella cheese.",
        "image": "AgACAgIAAxkBAANbZ9F80VJA_UM-DsJbTjZr8YXxN6sAAq_uMRuSg5BKOBB9SNOI2UwBAAMCAAN4AAM2BA",
        "size": "Large",
        "onsale": False
    },
    {
        "name": "Pepperoni",
        "price": 11,
        "about": "Classic pizza topped with delicious pepperoni slices.",
        "image": "AgACAgIAAxkBAANXZ9F80bbBIO62R0PT_0w1dpNCiugAAqvuMRuSg5BKKBmFx9Nr2_ABAAMCAAN4AAM2BA",
        "size": "Medium",
        "onsale": False
    },
    {
        "name": "Beef & Onion",
        "price": 13,
        "about": "Savory beef with caramelized onions and cheese.",
        "image": "AgACAgIAAxkBAANdZ9F80aG8Xw8869l_WIVBAiWdtwsAArDuMRuSg5BKup5pZfrJJeUBAAMCAAN4AAM2BA",
        "size": "Large",
        "onsale": False
    },
    {
        "name": "Barbecue",
        "price": 12,
        "about": "BBQ chicken, red onions, and mozzarella cheese.",
        "image": "AgACAgIAAxkBAANeZ9F80SxWpTPIEQeKIu1OrQb3bN0AArPuMRuSg5BKJlZCizBs7HoBAAMCAAN4AAM2BA",
        "size": "Medium",
        "onsale": True
    },
    {
        "name": "Chicken",
        "price": 11,
        "about": "Grilled chicken with cheese and tomato base.",
        "image": "AgACAgIAAxkBAANeZ9F80SxWpTPIEQeKIu1OrQb3bN0AArPuMRuSg5BKJlZCizBs7HoBAAMCAAN4AAM2BA",
        "size": "Medium",
        "onsale": False
    },
    {
        "name": "Brightush",  # signature pizza
        "price": 14,
        "about": "House special with secret ingredients and a unique taste.",
        "image": "AgACAgIAAxkBAANaZ9F80RT6LiMG01LmnSohLUN3IBgAAq3uMRuSg5BKSOQlLCq6CFUBAAMCAAN4AAM2BA",
        "size": "Large",
        "onsale": True
    },
    {
        "name": "Hawaiian",
        "price": 11,
        "about": "Classic ham and pineapple combination with mozzarella.",
        "image": "AgACAgIAAxkBAANgZ9F80UZ_3RjNBqPJohsvSsbwZqMAArXuMRuSg5BKGi4kweJZj5oBAAMCAAN4AAM2BA",
        "size": "Medium",
        "onsale": False
    },
    {
        "name": "Buffalo",
        "price": 13,
        "about": "Spicy buffalo chicken with ranch drizzle and cheese.",
        "image": "AgACAgIAAxkBAANgZ9F80UZ_3RjNBqPJohsvSsbwZqMAArXuMRuSg5BKGi4kweJZj5oBAAMCAAN4AAM2BA",
        "size": "Large",
        "onsale": True
    },
    {
        "name": "Chicken & Mushroom",
        "price": 12,
        "about": "Grilled chicken with fresh mushrooms and mozzarella.",
        "image": "AgACAgIAAxkBAANYZ9F80dnsIaX3M9FWSy1YwuvYKAgAAqzuMRuSg5BK1m7R0oJI06ABAAMCAAN4AAM2BA",
        "size": "Medium",
        "onsale": False
    },
    {
        "name": "Margherita",
        "price": 9,
        "about": "Classic tomato, mozzarella, and fresh basil.",
        "image": "AgACAgIAAxkBAANfZ9F80UzZErrvennpgd1wpa7QWvYAArLuMRuSg5BKzGObLHijU1oBAAMCAAN4AAM2BA",
        "size": "Small",
        "onsale": False
    }
]


@connection
async def add_pizza(session):
    for pizza in pizzas:
        async with session.begin():
            new_pizza = Pizza(
                name=pizza["name"],
                price=pizza["price"],
                about=pizza["about"],
                image=pizza["image"],
                size=pizza["size"],
                onsale=pizza["onsale"]
            )
            session.add(new_pizza)
        await session.flush()
    await session.commit()
