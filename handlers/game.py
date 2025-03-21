from telegram import Update
from telegram.ext import CallbackContext
from database import get_db, User, Game
from config import GAME_ENTRY_FEE, MIN_GAME_BET, MAX_GAME_BET
import random

# ... هندلرهای مربوط به بازی (شروع بازی، انتخاب عدد، حدس زدن، اعلام نتیجه و غیره)
