#from decouple import Config, RepositoryEnv
import os

# Specify the path to your .env file
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
#config = Config(RepositoryEnv(env_path))

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
