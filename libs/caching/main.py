import os
import shutil
import time
from colorama import Fore
from libs.ui.main import MainUI

def clear_cache():
    root_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
    cache_removed = False
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname == '__pycache__':
                dir_to_remove = os.path.join(dirpath, dirname)
                shutil.rmtree(dir_to_remove)
                MainUI.print_(f'Удалена папка: {dir_to_remove}', Fore.YELLOW)
                cache_removed = True
        for filename in filenames:
            if filename.endswith('.pyc'):
                file_to_remove = os.path.join(dirpath, filename)
                os.remove(file_to_remove)
                MainUI.print_(f'Удалён файл: {file_to_remove}', Fore.YELLOW)
                cache_removed = True
    
    if cache_removed:
        MainUI.print_('Кэш успешно удален!', Fore.GREEN)
    else:
        MainUI.print_('Кэш не найден!', Fore.RED)
    
    time.sleep(3)
    return MainUI.end_module(True)

def commands():
    return {
        'clear cache': clear_cache
    }
