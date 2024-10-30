import os, time, sqlite3, libs.core.config as config, configparser
from tqdm import tqdm
from libs import core, ui
from colorama import Fore, init

init(autoreset=True)

def main():
    sql, cursor = core.database.db_init()

    cursor.execute("SELECT * FROM libs")
    libs = cursor.fetchall()
    sql.close()

    ui.MainUI.logo()
    for i in tqdm(range(len(libs)), desc=Fore.CYAN + "Вас приветствует утилита Second Tool. Происходит загрузка модулей, подождите..." + Fore.GREEN):
        time.sleep(0.01)
    modules = core.libs.load(libs)
    ui.MainUI.print_('Подключение к серверу...', Fore.YELLOW)

    configp = configparser.ConfigParser()
    configp.read('config.ini', encoding='utf-8')
    offline = configp['main']['offline'].lower()
    if offline == 'true':
        offline = True
    else:
        offline = False

    status, msg = core.Server.getLastVersion()
    if status is False and offline is False:
        ui.MainUI.print_('Режим оффлайн отключен', Fore.BLUE)
        return ui.MainUI.print_(msg, Fore.RED)
    elif status is False and offline is True:
        ui.MainUI.print_(msg, Fore.RED)
        ui.MainUI.print_('Режим оффлайн активен.', Fore.RED)
    else:
        if status is not False and float(msg) != float(config.VERSION):
            ui.MainUI.print_('Установлена не актуальная версия программы. Рекомендуется актуализировать программу!', Fore.RED)
        elif status is True:
            ui.MainUI.print_('Успешно подключено!', Fore.GREEN)

    try:
        a = int(input(Fore.CYAN + '1.Start application\n2.Add lib\n3.Delete lib\n>>> ' + Fore.RESET))

        if a != 1 and a != 2 and a != 3:
            return ui.MainUI.print_('Invalid option', Fore.RED)
    except ValueError:
        return ui.MainUI.print_('Invalid option', Fore.RED)

    if a == 2:
        return core.libs.addLib()
    elif a == 3:
        return core.libs.deleteLib()

    time.sleep(2)
    return ui.MainUI.client(libs)  
    
main()