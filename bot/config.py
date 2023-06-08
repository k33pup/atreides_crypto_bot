from environs import Env

env = Env()
env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")
DB_PASS: str = env.str("DB_PASS")
DB_NAME: str = env.str("DB_NAME")
DB_USER: str = env.str("DB_USER")
IP: str = env.str("IP")
PORT: int = env.int("PORT")
PG_URL: str = f"postgresql+asyncpg://postgres:{DB_PASS}@{IP}/{DB_NAME}"
ADMINS: list[int] = list(map(int, env.list("ADMINS")))
NEED_TO_INIT_MODELS: bool = False
licenses: list[str] = ["bronze", "silver", "gold"]
key_length: int = 10
