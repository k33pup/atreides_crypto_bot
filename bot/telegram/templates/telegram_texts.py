from bot.config import licenses

intro_text = "Привет! Это бот Atreides. Вы хотите подключить его к себе? Если да, отправьте ключ активации так:\n\n" \
             "/activate 1234567890"
bad_pass_text = "Неверный ключ доступа! 😡"
accept_license = " 😎 Ваша лицензия активирована! Спасибо, что выбрали нас! " \
                 "В скором времени Вам начнут поступать сигналы 🤖. Будьте бдительны!"

bad_license_cmd = "Неправильное использование команды генерации лицензии!" \
                  "Используйте команду так:\n\n" \
                  "/new_license _тип лицензии_ _число дней_"

bad_license_type = f"Вы ввели несуществующий тип лицензии!\n" \
                   f"Доступные типы: {','.join(licenses)}"

bad_days_license = f"Вы неправильно ввели число дней!"
accept_license_create = "Вы успешно создали ключ!\n\n" \
                        "`{}`\n\n" \
                        "Истекает через {} дней"