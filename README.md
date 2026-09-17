Hello. To start this programm, follow these steps:

Choose "Trust this folder" if you didn`t do that.

Copy and paste commands under one by one to your terminal:

cd ..

sudo apt update

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo apt install ./google-chrome-stable_current_amd64.deb

Y

cd auto_autumn_duell

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

Write your skolenmin username and password in .env file.

Start programm with:

python main.py

If you want to open this project again, you need to wait 1 minute and after that, you can start the program with just a single command in the terminal:

python main.py

If you don't see "start" message in terminal for more than 10 seconds, stop programm with

CTRL+C

and start it again with

python main.py

If you have any questions, write to me on glikha@eigskole.no

P.S. It is normal to get "error" when you press CTRL+C, don't worry.
