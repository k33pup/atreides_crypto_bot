import logging

intro_text = "Привет! Это бот Realize Brain 🧠. Вы хотите подключить его к себе? Если да, напишите /yes"
password_text = "👇 Введите ключ активации от продукта"
bad_pass_text = "Неверный ключ доступа! 😡"
accept_license = " 😎 Ваша лицензия активирована! Спасибо, что выбрали нас! " \
                 "В скором времени Вам начнут поступать сигналы 🤖. Будьте бдительны!"

logging.basicConfig(filename="swag logs/teleg.log", level=logging.ERROR)
log_error = logging.getLogger("TELEBOT")