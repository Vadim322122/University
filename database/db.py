import aiosqlite

async def start_db():
    async with aiosqlite.connect("base.db") as db:
        cur = await db.cursor()
        await cur.execute('''CREATE TABLE IF NOT EXISTS Users (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Telegram INT,
            TAG_Telegram TEXT,
            Language TEXT,
            Admin_Role INT
        );''')
        await db.commit()

async def is_admin():
    async with aiosqlite.connect("base.db") as db:
        cur = await db.cursor()
        await cur.execute("SELECT ID_Telegram FROM Users WHERE Admin_Role = ?", (1,))
        existing_records = await cur.fetchall()
    return [row[0] for row in existing_records]

async def get_language(user_id):
    async with aiosqlite.connect("base.db") as db:
        cur = await db.cursor()
        await cur.execute("SELECT Language FROM Users WHERE ID_Telegram = (?)", (user_id,))
        result = await cur.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

async def update_language(user_id, new_language):
    async with aiosqlite.connect("base.db") as db:
        cur = await db.cursor()
        await cur.execute("UPDATE Users SET Language = ? WHERE ID_Telegram = ?", (new_language, user_id))
        await db.commit()

async def is_user_profiled(user_id):
    async with aiosqlite.connect("base.db") as db:
        cur = await db.cursor()
        await cur.execute("SELECT ID_Telegram FROM Users WHERE ID_Telegram = ?", (user_id,))
        existing_record = await cur.fetchone()
        if existing_record is not None:
            return True
        else:
            return False