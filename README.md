# Monee Share

MoneeShare revolutionizes financial accessibility with a seamless text-based banking platform designed for everyone, aimed at financial inclusion especially for those in rural areas, and to breach connectivity constraints.

## Tools used

1. Fast API
2. Supabase
3. Kora API
4. Africas talking

## How to use MoneeShare

All commands are sent via SMS to 34461. At the moment only MTN users can try out MoneeShare.
*Note: make sure to include "mshare" at the beginning*of every command.

Here are the commands to try out:

**Help:** this gives you information about how to use MoneeShare
e.g mshare help

**Create:** create an account for yourself on MoneeShare
e.g mshare create

---

## How to run the Backend

1. Clone the repo
2. Create a virtual environment `python -m venv venv`
3. Activate the virtual environment `source \venv\Scripts\activate` for Mac/Linux/git bash and `.\venv\Scripts\activate` for windows
4. run `pip install -r requirements.txt`
5. Register on the various platforms and provide the required variables in the .env file
6. run `fastapi run main.py` to start the server
