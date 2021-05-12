# Shotgun app for lazy médecine boys and girls

## What is it?

This is a bot that will let you shotgun your seat in the **very crowded** Necker library, without having to stay up all night for it.
This will mimick the peasant that spams the website around midnight, when it's updated, except it's way faster and doesn't need coffee.

## How to install?

1. Install Chrome (or another web browser you like)
2. Get a WebDriver for this web browser.

   Please be careful to select the right version, which you can usually find by opening your browser and selecting _Help_ > _About_.  
   You can then find yours by googling "{browsername} {webdriver}".

   **For Chrome**  
   Go to https://chromedriver.chromium.org/downloads.  
   Download the driver, then move it to your preferred folder and rename it (e.g.: `path/to/webdrivers/chrome_89_driver`).

3. If you don't have it already, [get Python](https://www.python.org/downloads/).
4. Download this code (using Git clone or by un-zipping it).
5. Install dependencies

- Open the folder in a terminal
- (Activate your virtual environment if you want to use one)
- `pip install -r requirements.txt`

6. Setup your environment

- Rename the `.env.example` file into `.env`
- Fill in the path to your webdriver as well as your web browser version, like this:

```
SELENIUM_DRIVERS_PATH=path/to/webdrivers
CHROME_VERSION=89
```

7. Setup the script!

- Open `preferences.json` in a text editor and edit it, like this:

```json
{
  "firstname": "Jean",
  "lastname": "Dupont",
  "email": "jean.dupont@etu.u-paris.fr",
  "master": "D2",
  "min_hour": "10:00", // Earliest acceptable hour for you.
  "max_hour": "20:00", // Latest acceptable hour for you.
  "start_trying_at": "23:55:00" // The bot will start spamming the website at this time and until it succeeds.
}
```

- Save: **you're all set!**

## How to use?

- Open the folder in a terminal
- (Activate your virtual environment if you want to use one)
- `python poc.py`
- Go do whatever you want to do.

## Librairies used

- [Selenium](https://selenium-python.readthedocs.io/)
- [Python Dotenv](https://github.com/theskumar/python-dotenv)
- [Schedule](https://github.com/dbader/schedule)
