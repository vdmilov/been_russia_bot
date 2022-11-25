from aiogram import Bot, Dispatcher, executor, types
import os

import keyboards as kb
import polls as p
import regions_map as r_map
import db

bot = Bot(token=os.environ.get('token'))
dp = Dispatcher(bot)

owner_id = os.environ.get('owner_id')

start_msg = (
    "After you click 'Start', there will be a series of polls with regions to select for each federal district "
    "(for some districts there are even two polls due to the limitations of Telegram). Multiple answers are "
    "possible. "
    "\n"
    "\nIf you haven't been to any region in the poll, just select 'Not yet ✖':) "
    "\n"
    "\nWhen done with all the selection, you will get your stats and the map. "
    "\n"
    "\nLet's start! Enjoy:)")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Hi there, please, select /been")


@dp.message_handler(commands=['been'])
async def been(message: types.Message):
    await bot.send_message(owner_id, f'@{message.from_user.username} has just started!')
    await bot.send_message(message.from_user.id, start_msg, reply_markup=kb.start)


@dp.message_handler()
async def other(message: types.Message):
    await bot.send_message(message.from_user.id, "To (re)start, please, select /been")


@dp.callback_query_handler()
async def callback_workaround(callback: types.callback_query):
    await callback.answer()
    if callback.data == 'start':
        db.log_user(callback, callback.data)  # logs user data into table users
        db.create_table(callback.from_user.id)  # creates table in db for each user with the name id_+user_name
        question = list(p.regions.keys())[0]
        options = list(p.regions[question])
        db.insert_question(callback.from_user.id, question)  # inserts current question
        await bot.send_message(callback.from_user.id, "Select all the regions you've been to in")
        await bot.send_poll(callback.from_user.id, question, options,
                            allows_multiple_answers=True, is_anonymous=False)
    elif callback.data == 'finish':
        db.log_user(callback, callback.data)  # logs user data into table users
        await bot.send_message(callback.from_user.id, text=db.send_stats(callback.from_user.id))
        await bot.send_message(callback.from_user.id, 'The map is rendering...')
        await bot.send_photo(callback.from_user.id, photo=r_map.map_to_send(callback.from_user.id))
        await bot.send_message(owner_id, f'@{callback.from_user.username} has just finished!')


@dp.poll_answer_handler()
async def poll_answer(poll_answer: types.PollAnswer):
    user_id = poll_answer.user.id
    last_question = db.last_question(user_id)  # gets last question from user table
    last_answers = poll_answer.option_ids
    db.delete_question(user_id)  # delete row with last question from user table
    db.insert_answers(user_id, last_question, last_answers)  # insert user answers

    if last_question == 'Volga Federal District (2/2)':
        await bot.send_message(user_id, "Well done! Let's see your map 🗺️", reply_markup=kb.finish)
    else:
        question = list(p.regions.keys())[list(p.regions.keys()).index(last_question) + 1]  # gets new question
        options = list(p.regions[question])  # gets new options for the poll
        db.insert_question(user_id, question)
        await bot.send_message(user_id, "Select all the regions you've been to in")
        await bot.send_poll(user_id, question, options, allows_multiple_answers=True, is_anonymous=False)


if __name__ == '__main__':
    db.check_db_exists()
    executor.start_polling(dp, skip_updates=True)
