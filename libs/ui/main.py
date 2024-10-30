import os
from colorama import Fore
import importlib
import logging

from libs import core

class MainUI():
    def logo(clear=False):
        if clear is True:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        
        print(Fore.YELLOW + """
███████╗███████╗ ██████╗ ██████╗ ███╗   ██╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     
██╔════╝██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
███████╗█████╗  ██║     ██║   ██║██╔██╗ ██║██║  ██║       ██║   ██║   ██║██║   ██║██║     
╚════██║██╔══╝  ██║     ██║   ██║██║╚██╗██║██║  ██║       ██║   ██║   ██║██║   ██║██║     
███████║███████╗╚██████╗╚██████╔╝██║ ╚████║██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
        """ + Fore.RESET)

    def print_(text, color):
        print(color + text + Fore.RESET)
    
    def end_module(clear = True):
        if clear is True:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        
        sql, cursor = core.database.db_init()

        cursor.execute("SELECT * FROM libs")
        libs = cursor.fetchall()

        MainUI.client(libs)
    
    def client(modules): 
        MainUI.logo(True)

        global_comm = []

        for module in modules:
            module_name = module[1]
            module_path = f'libs.{module[2]}'

            try:
                md = importlib.import_module(module_path)
                if hasattr(md, "commands") and callable(md.commands):
                    module_commands = md.commands()
                    global_comm.extend(f"{key}" for key in module_commands.keys())
                    MainUI.print_("\n".join([f"{key}" for key in module_commands]), Fore.CYAN)
                else:
                    return MainUI.print_(f'Произошла критическая ошибка модуля {module_name}. Проверьте источник модуля и попробуйте переустановить его.', Fore.RED)
            except ModuleNotFoundError:
                logging.warning(f"Модуль {module_name} не найден.")
            except Exception as e:
                logging.error(f"Ошибка при загрузке модуля {module_name}: {e}")
        
        MainUI.print_('clear: Clear Console', Fore.GREEN)
        MainUI.print_('close: Close Console', Fore.GREEN)
        global_comm.append('clear')
        global_comm.append('close')
        
        def get_command(global_comm):
            try:
                command = input('Введите команду >>> ')
            except KeyboardInterrupt:
                return exit(401)

            if command not in global_comm:
                MainUI.print_('Команда не найдена', Fore.RED)
                return get_command(global_comm)
            return command
        
        command = get_command(global_comm)

        if command == 'clear':
            return MainUI.client(modules)
        
        if command == 'close':
            return
        
        for module in modules:
            module_name = module[1]
            module_path = f'libs.{module[2]}'

            try:
                md = importlib.import_module(module_path)
                if hasattr(md, "commands") and callable(md.commands):
                    commands = md.commands()
                    if command in commands:
                        commands[command]()
                else:
                    return MainUI.print_(f'Произошла критическая ошибка модуля {module_name}. Проверьте источник модуля и попробуйте переустановить его.', Fore.RED)
            except ModuleNotFoundError:
                logging.warning(f"Модуль {module_name} не найден.")
            except Exception as e:
                logging.error(f"Ошибка при загрузке модуля {module_name}: {e}")
