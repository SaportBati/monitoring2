import logging
import asyncio
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройки
API_TOKEN = '8615103385:AAEtikLdZYMTZgqMkDWBJTewsqU-CK5gYyg'
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Глобальная переменная для драйвера
driver = None

def init_browser():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    # Добавляем User-Agent, чтобы сайт не блокировал нас
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    
    # Авторизация
    driver.get("https://forum.arizona-rp.com/")
    
    # Нажатие "Вход"
    login_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Вход")))
    login_btn.click()
    
    # Ввод данных
    username_field = wait.until(EC.visibility_of_element_located((By.NAME, "login")))
    username_field.send_keys("Kions_Loast")
    driver.find_element(By.NAME, "password").send_keys("_f6Oy8sFIn")
    
    # Клик "Войти"
    submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    driver.execute_script("arguments[0].click();", submit_btn)
    
    logging.info("Авторизация в браузере пройдена.")

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Бот запущен. Пришлите ссылку для проверки.")

@dp.message(F.text.startswith("http"))
async def process_link(message: Message):
    url = message.text
    try:
        driver.get(url)
        # Если переход успешен, бот ответит yes
        await message.answer("yes")
    except Exception as e:
        logging.error(f"Debug: {e}")
        await message.answer("debug")

async def main():
    init_browser()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        if driver:
            driver.quit()
