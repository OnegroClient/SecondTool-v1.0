import sqlite3, importlib, logging, requests, base64, libs.core.config as config, os
from libs import ui
from colorama import Fore

class database():
    def db_init():
        sql = sqlite3.connect("session.db")
        cursor = sql.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS libs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            path TEXT
        )""")
        sql.commit()
        return sql, cursor

class libs():
    def load(modules):
        loaded_modules = {}
        for module in modules:
            module_name = module[2]
            module_path = os.path.join(module_name)
            if os.path.isdir(f'libs/{module_path}') and '__init__.py' in os.listdir(f'libs/{module_path}'):
                try:
                    md = importlib.import_module(f"libs.{module_name}")
                    loaded_modules[module_name] = md
                    ui.MainUI.print_(f"Модуль {module_name} успешно загружен.", Fore.GREEN)
                except ModuleNotFoundError:
                    logging.warning(f"Модуль {module_name} не найден и не будет загружен.")
                except Exception as e:
                    logging.error(f"Ошибка при загрузке модуля {module_name}: {e}")
        return loaded_modules
    
    def addLib():
        ui.MainUI.logo(True)
        ui.MainUI.print_('Добавление модуля', Fore.YELLOW)
        name = input(Fore.CYAN + 'Введите название модуля >>> ' + Fore.RESET)
        path = input(Fore.CYAN + 'Введите название папки модуля в папке libs >>> ' + Fore.RESET)

        correct = input(Fore.CYAN + 'Проверьте данные. Они правильные?(Y/n)' + Fore.RESET)

        if correct.lower() == 'n':
            return libs.addLib()
        
        sql, cursor = database.db_init()
        cursor.execute("INSERT INTO libs (name, path) VALUES (?, ?)", (name, path))
        sql.commit()
        sql.close()

        return ui.MainUI.print_('Модуль успешно добавлен! Перезапустите программу.', Fore.GREEN)
    
    def deleteLib():
        ui.MainUI.logo(True)
        ui.MainUI.print_('Удаление модуля', Fore.YELLOW)

        name = input(Fore.CYAN + 'Введите название модуля >>> ' + Fore.RESET)
        correct = input(Fore.CYAN + 'Проверьте данные. Они правильные?(Y/n)' + Fore.RESET)

        if correct.lower() == 'n':
            return libs.deleteLib()
        
        sql, cursor = database.db_init()
        cursor.execute("DELETE FROM libs WHERE name = ?",(name.strip(),))
        result = cursor.fetchone()
        sql.commit()
        sql.close()

        ui.MainUI.print_('Внимание! Иногда программа дает сбой и не удаляет библиотеку с базы данных. Проверяйте это!', Fore.RED)
        return ui.MainUI.print_('Модуль успешно удален. Перезапустите программу.', Fore.GREEN)

class Server():
    def getLastVersion():
        try:
            external_ip = requests.get('https://api64.ipify.org?format=json').json()['ip']
            response = requests.get(
                url=f'{config.MAIN_URL}/SecondTool/MultiTool/PC/getVersion',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data={
                    'code': base64.b64encode(b'SecondTool-keyNot-ROOT-ADMIN'),
                    'ip': external_ip
                }
            )
        except:
            return False, 'Не удалось подключится к серверу. Попробуйте позже.'
        if response.ok:
            return True, response.json()['version']
        else:
            return False, 'Не удалось подключится к серверу. Попробуйте позже.'
