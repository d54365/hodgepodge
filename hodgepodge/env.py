from environ import Env
from environ import Path

env = Env()

BASE_DIR = Path(__file__) - 1

PROJECT_DIR = BASE_DIR - 1

env_name = env.str("DJANGO_PROJECT_ENV", "local")

env.read_env(f"{BASE_DIR}/envs/.env.{env_name}")
