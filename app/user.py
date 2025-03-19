from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext



import app.keyboards as kb
import app.database.requests as db
from app.states import AddCart


user = Router()

@user.message(CommandStart())
async def start(message: Message):
    await db.set_user(message.from_user.id) # register new user in db - add try catch later on for all db requests
    await message.answer(
        f"""🍕 Welcome {message.from_user.first_name}!
Craving pizza? You’re in the right place!  
✅ Browse the menu  
✅ Customize your pizza  
✅ Place an order and track it in real-time  
All right here. Let's get started! 🍕🔥"""
,reply_markup=kb.menu)
    
@user.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer(
        text="🍕Catalog",
        reply_markup= await kb.catalog_kb() 
        )


@user.callback_query(F.data.startswith("pizza_"))
async def pizza_info(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()
    pizza_id = int(callback.data.split("_")[1])
    await state.update_data(pizza_id=pizza_id)
    pizza = await db.get_pizza(pizza_id)
    await callback.message.answer_photo(
        photo=pizza.image,
        caption=f"{pizza.name}\n{pizza.about}\n{pizza.price} RUB",
        parse_mode='HTML',
        reply_markup= await kb.pizza_kb(pizza_id)
        )


@user.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(AddCart.size)
    await callback.message.answer(
        text="Choose the size of the pizza",
        reply_markup= await kb.add_to_cart_kb()
        )

@user.callback_query(AddCart.size)
async def size(callback: CallbackQuery, state: FSMContext):
   await state.update_data(size=callback.data.split("_")[1])
   await state.set_state(AddCart.quantity)
   await callback.message.edit_text(
       text = "Enter the quantity of the pizza",
       reply_markup= await kb.choose_quantity_kb())
  

@user.callback_query(AddCart.quantity)
async def quantity(callback: CallbackQuery, state: FSMContext):
    await state.update_data(quantity=callback.data.split("_")[1])    
    data = await state.get_data()
    pizza_id = data["pizza_id"]  
    size = data["size"]
    quantity = data["quantity"]
   
    if await db.add_to_cart(callback.from_user.id, pizza_id, size, quantity):
        await state.clear()
        await callback.message.edit_text(f"""🍕Pizza added to cart!\nSize:{size}\nQuantity: {quantity}""",
                                        reply_markup=await kb.proceed_to_pay())
    else:
        await callback.message.answer("Error adding to cart")
    await callback.answer()

@user.callback_query(F.data=="menu")
async def menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="🍕Menu",
        reply_markup=kb.menu
        )
    await callback.answer()


@user.callback_query(F.data=="cart")
async def cart(callback: CallbackQuery):
    cart = await db.get_cart(callback.from_user.id)
    if not cart:
        await callback.answer("🛒Cart is empty",show_alert=True)
        await callback.message.edit_text(
            text="🍕Cart is empty, Slect something",
            reply_markup= kb.menu)
    else:
        await callback.message.edit_text(
            text="🛒Cart",
            reply_markup=await kb.cart_kb(callback.from_user.id)
            )
    await callback.answer()    

@user.callback_query(F.data.startswith("remove_"))
async def remove_item(callback: CallbackQuery):
    cart_id = int(callback.data.split("_")[1])
    await db.remove_quantity(cart_id)
    await callback.message.edit_text(
        text="Item removed from cart",
        reply_markup=await kb.cart_kb(callback.from_user.id)
        )
    await callback.answer()

@user.callback_query(F.data.startswith("add_"))
async def add_item(callback: CallbackQuery):
    cart_id = int(callback.data.split("_")[1])
    await db.add_quantity(cart_id)
    await callback.message.edit_text(
        text="Item added to cart",
        reply_markup=await kb.cart_kb(callback.from_user.id)
        )
    await callback.answer()
    
@user.callback_query(F.data=="pay")
async def pay(callback: CallbackQuery):
    await callback.message.edit_text(
        text="💳Pay",
        reply_markup=await kb.pay_kb()
        )
    await callback.answer()
    
    
@user.message(F.photo)
async def handle_photo(message: Message):
    await message.answer(message.photo[-1].file_id)