import platform
import os 
import yaml
from dotenv import load_dotenv
from multiprocessing.dummy import Pool as ThreadPool
from modules.watchdog_handler import logCheck
from modules.windows_event_handler import windows_event_log_check
from modules.recursive_handler import recursive_training_data_check
from modules.utils import initValue


def load_Yaml():
    with open('.\config\Setting.yaml', encoding='UTF-8') as f:
        _config = yaml.load(f, Loader=yaml.FullLoader)

    return _config

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def create_Dir():
    file_fullpath = os.path.dirname(os.path.abspath(__file__))
    createDirectory(file_fullpath + "\\output\\windows_event_log")
    createDirectory(file_fullpath + "\\output\\training")
    createDirectory(file_fullpath + "\\output\\offset")

def working(work):
    if "monitoring" in work and "file" in work["monitoring"]:
        if "type" not in work or work["type"] == "normal":
            logCheck(work)
        elif work["type"] == "windows-event" and platform.system() == 'Windows':
            windows_event_log_check(work)
        elif work["type"] == "recursive":
            recursive_training_data_check(work)

def workThread(worklist, threadnum=1):
    pool = ThreadPool(threadnum)
    result = pool.map(working, worklist)
    pool.close()
    pool.join()

    return result

def main():
    create_Dir()
    _config = load_Yaml()

    data = _config['data']
    common = _config['common']

    for d in data:
        initValue(d, 'interval', common, 1)
        initValue(d, 'minimum-length', common, 10)
        initValue(d, 'mode', common, 'training')
        initValue(d, 'report', common, False)
        initValue(d, 'initial-check', common, False)
        initValue(d, 'similarity-threshold', common, 0.4)
        initValue(d, 'match-rate', common, 0)
        initValue(d, 'match-max-count', common, 0)
        initValue(d, 'depth', common, 4)
        initValue(d, 'compress-state', common, True)
        initValue(d, 'parametrize-numeric-tokens', common, True)
        initValue(d, 'write-file-flag', common, False)

    result = workThread(data, len(data))
    print(result)

if __name__ == "__main__":
    main()
