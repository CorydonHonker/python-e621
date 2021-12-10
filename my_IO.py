import shutil
from json import dumps, loads
from os import makedirs

# NOTE: work on "move_dir()", and "move_file()"


def relocate(old_path, new_path):
    print(f'relocating: {old_path}\nto new path: {new_path}')
    try:
        shutil.move(old_path, new_path)
    except FileNotFoundError:
        print('Path not found...')


def name_filter(name):
    r = '_'
    name = name \
        .replace('<', r) \
        .replace('>', r) \
        .replace(':', r) \
        .replace('\\', r) \
        .replace('|', r) \
        .replace('?', r) \
        .replace('*', r) \
        .replace('"', r).replace('/', r)
    return name


def directory(directory_name):
    try:
        makedirs(directory_name, exist_ok=True)
        print("Directory ", directory_name, " Created ")
    except FileExistsError:
        print("Directory ", directory_name, " already exists...")


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def save_json_file(file_path, my_data):
    with open(file_path, "w", encoding="utf8") as f:
        f.write(dumps(my_data, ensure_ascii=bool(0)))


def open_json_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf8") as f:
            return loads(f.read())
    except IOError:
        print('File Not Found: ', file_path)
        return None


def save_txt_file(file_name, my_data):
    with open(file_name, "w", encoding="utf8") as f:
        f.write(my_data)
