# Table of Contents
1. [Example](#example)
2. [Example2](#example2)
3. [Third Example](#third-example)
4. [Fourth Example](#fourth-examplehttpwwwfourthexamplecom)


## Example


<h1 align="center">
  <br>
 API development. Social network with authentication and votes. <br>
 :robot:
</h1>


<h3 align="center">
  Built with
  <br>
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/aad4d15178483720bcc0562617c86a7c84a7d257/shields.io/python.svg" height="30">
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/aad4d15178483720bcc0562617c86a7c84a7d257/shields.io/heroku.svg" height="30">
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/4747733b63d843a80f861cc51bf58fcf8586dd82/shields.io/postgres.svg" height="30">
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/4747733b63d843a80f861cc51bf58fcf8586dd82/shields.io/fastapi.svg" height="30">
    <img src="https://raw.githubusercontent.com/boramorka/usercontent/4747733b63d843a80f861cc51bf58fcf8586dd82/shields.io/docker.svg" height="30">
    <img src="https://github.com/boramorka/usercontent/blob/main/API_dev/pydantic.png?raw=true" height="30">
    <img src="https://github.com/boramorka/usercontent/blob/main/API_dev/sqlalchemy.png?raw=true" height="30">

<p align="center">
  • <a href="#how-to-use">How To Use</a> • <br>
  • <a href="#built-process">Built process</a> :arrow_right: <a href="#built-process">Built process</a> • <a href="#built-process">Built process</a> • <a href="#built-process">Built process</a> • <a href="#built-process">Built process</a> • <a href="#built-process">Built process</a> • <a href="#built-process">Built process</a> • <a href="#built-process">Built process</a> • <br>
  • <a href="#feedback">Feedback</a> •
</p>

## How to use
Go to https://fastapi-boramorka.herokuapp.com/docs#/
## How To Run Locally

  ``` bash
  # Clone this repository
  $ git clone https://github.com/boramorka/text-extraction-app.git

  # Go into the repository
  $ cd text-extraction-app

  # Install dependencies
  $ pip install requirements.txt

  # Run app
  $ python bot.py
  ```

## Built process

- First of all we creating an app.py file for the main app. It contains:
  ```python
  # Path to pytesseract
  pytesseract.pytesseract.tesseract_cmd

  # Code for text recognition
  def get_text():
  ...............
  ```
- Bot.py script starts the bot. It containts **AIOGram**. It's a pretty simple and fully asynchronous framework for [Telegram Bot API](https://core.telegram.org/bots/api) written in Python 3.7 with [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://github.com/aio-libs/aiohttp). It helps you to make your bots faster and simpler.
  

  ```python
  # Bot class takes an API key to connect to the Telegram servers.
  bot = Bot(token=os.getenv("TEXT_EXTRACTOR_API_KEY")) #Note: API key is envioroment variable

  """
  Dispatcher will process incoming updates: 
      • messages
      • edited messages
      • channel posts
      • edited channel posts
      • inline queries
      • chosen inline results
      • callback queries
      • shipping queries
      • pre-checkout queries.
  """
  dp = Dispatcher(bot) 
  
  # Decorator that takes a message and processes it.
  @dp.message_handler(text=message)
  ```

- Heroku deployment:
Important files:
  - :page_facing_up: bot.py: the bot application (refer to my Github for the source code) 
  - :page_facing_up: Aptfile : the third-party dependencies for Heroku to install (e.g: tesseract-ocr)
  - :page_facing_up: Procfile : a list of process types in an app (on Heroku)
  - :page_facing_up: requirements.txt : a list of dependencies to install
  - :page_facing_up: runtime.txt : version of Python to run on Heroku (optional)

  ```bash
  # HEROKU DEPLOYMENT PROCESS

  # Note:
  # Add this line to bot.py
  pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"
  # (refer to my Github for the source code)

  # Login to Heroku, and create a new app:
  $ heroku login
  $git init
  $heroku create boramorka-text-extraction-app
  $heroku git:remote -a boramorka-text-extraction-app

  # Add Buildpacks:
  $ heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
  $ heroku buildpacks:add --index 2 heroku/python

  # Add Config Vars:
  $ heroku config:set TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/4.00/tessdata

  # heroku stack (heroku-20) has bad compatibility with tesseract.
  # You may need to change heroku stack from 20 to 18 using command:
  $ heroku stack:set heroku-18

  # Deploy app on Heroku:
  $ git add .
  $ git commit -m "Initial commit to Heroku"
  $ heroku git:remote -a boramorka-text-extraction-app
  $ git push heroku master

  # Check worker status:
  $ heroku ps

  # Run worker
  $ heroku ps:scale worker=1
  ```

## Feedback
:person_in_tuxedo: Feel free to send me feedback on [Telegram](https://t.me/boramorka). Feature requests are always welcome. 

:abacus: [Check my other projects.](https://github.com/boramorka)


