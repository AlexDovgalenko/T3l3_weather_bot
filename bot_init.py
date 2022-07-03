import sqlite3

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

from config import APP_DB_NAME, USER_OPTIONS_TABLE_NAME, BOT_HASH

storage = MemoryStorage()

bot = Bot(token=BOT_HASH, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


class UserOptionsDB:
    f"""Class to initialize SQLite db instance and creates weather cache file '{APP_DB_NAME}' if it is absent.
     Also it creates table with name '{USER_OPTIONS_TABLE_NAME}' in case if it absent."""

    def __init__(self, db_name):
        self._db_connection = sqlite3.connect(db_name, check_same_thread=False)
        self._db_cursor = self._db_connection.cursor()
        result_query = self._db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        # creates a table in case if it is absent
        if not result_query or USER_OPTIONS_TABLE_NAME not in sorted(list(zip(*result_query))[0]):
            self._db_cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {USER_OPTIONS_TABLE_NAME} (USER_ID INTEGER PRIMARY KEY, LANGUAGE TEXT, WEATHER_PROVIDER TEXT)""")
            self._db_connection.commit()

    @property
    def db_cursor(self):
        return self._db_cursor

    @property
    def db_connection(self):
        return self._db_connection


app_db = UserOptionsDB(APP_DB_NAME)


def get_all_user_ids():
    """Loads list of user IDs from user options table"""
    logger.info(f"Trying to load list of user IDs from user options table ...")
    try:
        sql_query = f"""SELECT USER_ID from {USER_OPTIONS_TABLE_NAME}"""
        app_db.db_cursor.execute(sql_query)
        result = app_db.db_cursor.fetchall()
    except Exception as err:
        logger.error(err)
        raise RuntimeError(f"Failed to fetch user IDs list from the '{USER_OPTIONS_TABLE_NAME}' table.")
    if result:
        user_ids_list = [user_id[0] for user_id in result]
        logger.debug(f"List of user ids in DB:\n{user_ids_list}")
        return user_ids_list
    else:
        return result


def get_user_data(user_id):
    """Loads specific user data from the BD by specified user ID"""
    try:
        logger.info(f"Trying to load user data for used with ID '{user_id}' ...")
        sql_query = f"""SELECT * from {USER_OPTIONS_TABLE_NAME} WHERE USER_ID = {user_id}"""
        app_db.db_cursor.execute(sql_query)
        result = app_db.db_cursor.fetchall()
        if len(result) > 1:
            raise RuntimeError("Only one record with the same USER_ID should be present in DB!!!")
    except Exception as err:
        logger.error(err)
        raise RuntimeError(f"Failed to fetch user IDs list from the '{USER_OPTIONS_TABLE_NAME}' table.")
    return result[0]


def insert_user_data(user_id, user_data):
    """Inserts user options data into db by specific ID"""
    try:
        logger.info(f"Trying to insert user options data with user id: '{user_id}' ...")
        sql_query = f"""INSERT into {USER_OPTIONS_TABLE_NAME} values (?, ?, ?)"""
        app_db.db_cursor.execute(sql_query, (user_id, user_data.get("language"), user_data.get("weather_provider")))
        app_db.db_connection.commit()
    except Exception as err:
        logger.error(err)
        raise RuntimeError("Failed to insert user options data into the DB.")


def update_user_data(user_id, user_data):
    logger.info(f"Trying to update user options data with user ID: '{user_id}'...")
    try:
        sql_query = f""" UPDATE {USER_OPTIONS_TABLE_NAME} SET LANGUAGE = '{user_data.get("language")}', WEATHER_PROVIDER = '{user_data.get("weather_provider")}' WHERE  USER_ID = {user_id}"""
        app_db.db_cursor.execute(sql_query)
        app_db.db_connection.commit()
    except Exception as err:
        logger.error(err)
        raise RuntimeError("Failed to update user options data in the DB.")


def delete_user_data(user_id):
    raise NotImplementedError


def write_user_data(user_id, user_data):
    """Updates user options in the DB if provided user_id is already present, or Inserts new record otherwise."""
    logger.info("Trying to write user configuration data into DB.")
    if user_id in get_all_user_ids():
        update_user_data(user_id, user_data)
    else:
        insert_user_data(user_id, user_data)
