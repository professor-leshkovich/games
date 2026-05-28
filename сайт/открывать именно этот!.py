import eel
from os.path import dirname, join

# Экспортируем функцию, которую вызывает JS через eel
@eel.expose
def передатьФайл(событие):
    print("Получено событие из JS:", событие)
    # здесь ваша логика обработки файла

def main():
    путь_к_папке_с_хтмл = join(dirname(__file__), "games")
    # инициализация
    eel.init(путь_к_папке_с_хтмл)

    # запуск html
    eel.start("index.html", size=(1000, 600))

main()