from src import app

if __name__ =='__main__':
    app.run()

#  післі створення структури робимо наступні три кроки
# ініціалізувати БД
# flask db init

# Виконуємо міграцію
# flask db migrate -m "Initial migration"

# і виконуємо апгрейд, після цього кроку з'являється БД
# flask db upgrade