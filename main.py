from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


API_TOKEN = 'TOKEN'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, "Привет")


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    url = f'https://uk.wikipedia.org/w/index.php?go=Перейти&search={message.text}'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    links = soup.find_all('div', class_='mw-search-result-heading')

    if len(links) > 0:
        url = f'https://uk.wikipedia.org{links[0].find("a")["href"]}'

    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)

    driver.execute_script("window.scrollTo(0, 180)")
    driver.save_screenshot("img.png")
    driver.close()


    photo = open("img.png", "rb")
    await bot.send_photo(message.chat.id, photo=photo, caption=f'Ссылка на статью: <a href="{url}">тык</a>', parse_mode='HTML')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)