Эта часть проекта, которая использует библиотеку telethon для чтения сообщений из под аккаунта (не бота).
Она запрашивает список подписок у Backend части. Проходит по всем подпискам, ищет ключевые слова и пересылает их.
Если группа недоступна - она попадает в список исключений.

Для локального тестирования надо поднять бэк часть на 127.0.0.1:8080 и добавить файл credentials.json в папку app и запустить main.py.
На хостинге переменные кред передаются через переменные окружения.

При старте приложения нужно будет один раз залогиниться (ввести номер телефона и код подтверждения). При этом данные сохраняются в файл сессии в папку mounted.