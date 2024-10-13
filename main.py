import asyncio
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from aiogram import Bot, Dispatcher, F

from app.handlers import router

from app.database.orm import SyncORM, AsyncORM


# SyncORM.create_tables()
# SyncORM.insert_users()
#SyncORM.select_users()
# SyncORM.update_users() не работает че-т
#SyncORM.insert_profiles()
# SyncORM.send_profile()
# SyncORM.convert_users_to_dto()



async def main():
    # await AsyncORM.insert_photo()
    # await AsyncORM.send_profile()
    # await AsyncORM.insert_users()
    # await AsyncORM.insert_profiles()
    # await AsyncORM.update_profile()
    # await AsyncORM.convert_users_to_dto()
    # await AsyncORM.select_users()
    bot = Bot(token='7126231479:AAHILyOiKMIHEBN58Dq7IXViiXXUf4r0q-E')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)




if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is turned off')
