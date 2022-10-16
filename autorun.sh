cd /home/def/gold_price_bot/
if [ $(ps -aux | grep gold_price_bot | wc -l) -eq 1 ]; then python3 app.py >> bot.log ; fi