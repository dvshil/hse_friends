from aiohttp.web_routedef import static
from sqlalchemy import text, insert, select, inspect, and_, func, cast, Integer, or_
from sqlalchemy.sql.functions import random



from app.database.database_f import sync_engine, async_engine, session_factory, async_session_factory
from app.database.models import User, Base, UserProfile
from app.database.schemas import UsersDTO, ProfilesDTO


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        # Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_users():
        with session_factory() as session:
            tg_ismail = User(tg_id="@imukuev")
            session.add_all([tg_ismail])

            # После flush каждый из работников получает первичный ключ id, который отдала БД
            session.flush()
            session.commit()

    @staticmethod
    def select_users():
        with session_factory() as session:
            query = select(User) # SELECT * FROM workers
            result = session.execute(query)
            users = result.scalars().all()
            print(f"{users=}")


    @staticmethod
    def update_users(user_id: int = 1, new_username: str = "mukuev9"):
        with session_factory() as session:
            user_ismail = session.get(User, user_id)
            user_ismail.tg_id = new_username
            # refresh нужен, если мы хотим заново подгрузить данные модели из базы.
            # Подходит, если мы давно получили модель и в это время
            # данные в базе данных могли быть изменены
            session.refresh(user_ismail)

            # expire: мы получили какой-то объект из базы данных
            # мы провели с ним какие-то изменения, но в базе они еще не оказались
            # и нам захотелось чтобы все изменения которые мы к этому работнику применили, сбросились
            # для этого и используется session.expire. Мы можем применить expire к одному объекту или сразу ко всем
            # session.expire_all()
            session.commit()

    @staticmethod
    def insert_profiles():
        with session_factory() as session:
            user_1 = UserProfile(id=1,
                name="Ismail", age=19, gender="Male", group="КНТ-6",
                hobbies="Like football, running, hiking",
            contact="@imukuev", user_id = 1)
            # resume_jack_2 = ResumesOrm(
            #     title="Python Разработчик", compensation=150000, workload=Workload.fulltime, worker_id=1)
            # resume_michael_1 = ResumesOrm(
            #     title="Python Data Engineer", compensation=250000, workload=Workload.parttime, worker_id=2)
            # resume_michael_2 = ResumesOrm(
            #     title="Data Scientist", compensation=300000, workload=Workload.fulltime, worker_id=2)
            session.add(user_1)
            session.commit()
            sync_engine.echo = True


    @staticmethod
    def send_profile():
        with session_factory() as session:
            query = select(UserProfile)
            result = session.execute(query)
            profile = result.scalars().all()

            print(f"{profile=}")
            return profile


    @staticmethod
    def convert_users_to_dto():
        with session_factory() as session:
            query = (
                select(UserProfile)
                .limit(2)
            )

            res = session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [ProfilesDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto








class AsyncORM:

    # @staticmethod
    # async def insert_photo(infile_id: str):
    #     async with async_session_factory() as session:
    #         photo1 = Photo(id=1, file_id=infile_id)
    #         session.add_all([photo1])
    #         await session.commit()
    #
    #
    # @staticmethod
    # async def convert_photo_to_dto():
    #     async with async_session_factory() as session:
    #         query = (
    #             select(Photo)
    #             .limit(1)
    #         )
    #
    #         res = await session.execute(query)
    #         result_orm = res.scalars().all()
    #         result_dto = [PhotosDTO.model_validate(row, from_attributes=True) for row in result_orm]
    #         print(f"{result_dto=}")
    #         return result_dto
    #

    @staticmethod
    async def send_profile():
        async with async_session_factory() as session:
            # query = select(UserProfile)
            # result = await session.execute(query)
            # profile = result.scalars().all()
            query = select(UserProfile)
            res = await session.execute(query)
            result = res.all()
            print(f"{result=}")

    @staticmethod
    async def convert_users_to_dto():
        async with async_session_factory() as session:
            query = (
                select(UserProfile)
                .order_by(func.random())
                .limit(1)
            )

            res = await session.execute(query)
            result_orm = res.scalars().all()
            result_dto = [ProfilesDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto


    @staticmethod
    async def insert_users(intg_id: str):
        async with async_session_factory() as session:
            user1 = User(tg_id=intg_id) # RETURNING id
            # tg_user2 = User(id=39, tg_id="@oops_yy")
            # tg_user3 = User(id=36, tg_id="@vladisslavva")
            # tg_user4 = User(id=37, tg_id="@lola_os")
            session.add_all([user1])

            await session.flush()
            await session.commit()
            query = (
                select(User)
                .order_by(User.id.desc())
                .limit(1)
            )
            result = await session.execute(query)
            result_orm = result.scalars().all()
            result_dto = [UsersDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto


    @staticmethod
    async def select_users():
        async with async_session_factory() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            print(f"{users=}")

    @staticmethod
    async def insert_profiles(name: str, age: int, birthday: str, zodiac: str, group: str, hobbies: str, contact: str,
                              photo_id: str, user_id: int):
        async with async_session_factory() as session:
            profile1 = UserProfile(name=name, age=age, birthday=birthday, zodiac=zodiac, group=group,
                                 hobbies=hobbies, contact=contact, photo_id=photo_id, user_id=user_id)
            # profile2 = UserProfile(id=39, name="Дашуля💕", age=18, gender="Девушка",
            #                              group="КНТ-6", hobbies="хожу на танцы, изучаю языки, люблю путешествовать и музыку! зз: близнецы",
            #                              contact="@oops_yy", user_id=39)
            # profile3 = UserProfile(id=36, name="Владислава", age=18, gender="Девушка",
            #                              group="КНТ-5", hobbies="телец♉️, мс по танцам, обожаю путешествовать и новые знакомства🎀🤍",
            #                              contact="@vladisslavva", user_id=36)
            # profile4 = UserProfile(id=37, name="Лола", age=18, gender="Девушка",
            #                        group="КНТ-5", hobbies="люблю танцевать перед зеркалом, проводить время с друзьями, за любой движ, могу и шаурму на лавочке поесть и в кафешке с тобой посидеть зз: дева",
            #                        contact="@lola_os", user_id=37)


            session.add_all([profile1])
            await session.commit()

    @staticmethod
    async def update_profile():
        async with async_session_factory() as session:
            profile_lolita = await session.get(UserProfile, 2)
            profile_lolita.gender = "Девушка"
            await session.commit()






#     @staticmethod
#     async def create_tables():
#         async with async_engine.begin() as conn:
#             await conn.run_sync(Base.metadata.drop_all)
#             await conn.run_sync(Base.metadata.create_all)
#
#     @staticmethod
#     async def insert_workers():
#         async with async_session_factory() as async_session:
#             worker_jack = WorkersOrm(username="Jack")
#             worker_michael = WorkersOrm(username="Michael")
#             async_session.add_all([worker_jack, worker_michael])
#             # flush взаимодействует с БД, поэтому пишем await
#             await async_session.flush()
#             await async_session.commit()
#
#
#     @staticmethod
#     async def update_worker(worker_id: int = 2, new_username: str = "Misha"):
#         async with async_session_factory() as session:
#             worker_michael = await session.get(WorkersOrm, worker_id)
#             worker_michael.username = new_username
#             await session.refresh(worker_michael)
#             await session.commit()