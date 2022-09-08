import shutil
from pathlib import Path
import send2trash
from string import ascii_letters, digits

IMAGE_FILES = ('.jpeg', '.png', '.jpg', '.svg')
VIDEO_FILES = ('.avi', '.mp4', '.mov', '.mkv')
DOC_FILES = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
MUSIC_FILES = ('.mp3', '.ogg', '.wav', '.amr')
ARCH_FILES = ('.zip', '.gz', '.tar')

IGNORE_FOLDERS = ('archives', 'video', 'audio', 'documents', 'images')

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyr)] = lat
    TRANS[ord(cyr.upper())] = lat.upper()

empty_fold_del = []
known_formats = set()
unknown_formats = set()
images = []
videos = []
texts = []
audio = []
archives = []
other_files = []

files_of_each_cat = {
    'images': images,
    'videos': videos,
    'texts': texts,
    'audio': audio,
    'archives': archives,
    'other': other_files,
    'known formats': known_formats,
    'unknown formats': unknown_formats,
    'deleted folders': empty_fold_del
}


# Function for transliteration
def translate(name: str) -> str:
    return name.translate(TRANS)


# Function that swaps cyrillic letters with Latin,
# and swaps non ascii letters and digits with "_"
def normalize(file_or_folder_name: str) -> str:
    normal_name = ''
    for char in file_or_folder_name:
        if char in CYRILLIC_SYMBOLS:
            normal_name += translate(char)
        elif (char in ascii_letters) or (char in digits):
            normal_name += char
        else:
            normal_name += '_'
    return normal_name


# Function for creating folder and moving file to it
def new_folder(file_abs_path: Path, new_fold: str) -> None:
    if not Path(file_abs_path.parent / new_fold).exists():
        try:
            Path.mkdir(file_abs_path.parent / new_fold)
        except Exception as error:
            print(error)
    try:
        Path.replace(file_abs_path,
                     file_abs_path.parent / new_fold / file_abs_path.name)
    except Exception as error:
        print(error)


# Function for sorting files in folder and all subfolders
def sort_folder(fold_path: Path) -> dict:
    list_glob_gen = []
    for child in Path(fold_path).glob('*'):
        if child.is_file():
            if child.name.rfind('.') == 0:
                suffix_temp = child.name
            else:
                suffix_temp = child.suffix
            if suffix_temp in IMAGE_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'images')
                images.append(f"{child.parent / 'images' / child.name}")
            elif suffix_temp in VIDEO_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'video')
                videos.append(f"{child.parent / 'video' / child.name}")
            elif suffix_temp in DOC_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'documents')
                texts.append(f"{child.parent / 'documents' / child.name}")
            elif suffix_temp in MUSIC_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'audio')
                audio.append(f"{child.parent / 'audio' / child.name}")
            elif suffix_temp in ARCH_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'archives')
                archives.append(f"{child.parent / 'archives' / child.name}")
                shutil.unpack_archive(child.parent / 'archives' / child.name,
                                      child.parent / 'archives' / child.stem)
            else:
                unknown_formats.add(suffix_temp)
                other_files.append(str(child))
        elif child.is_dir() and (child.name not in IGNORE_FOLDERS):
            sort_folder(child)
            if not any(child.iterdir()):
                empty_fold_del.append(child)
                send2trash.send2trash(child)
        else:
            pass
    for child in Path(fold_path).glob('**/*'):
        list_glob_gen.append(child)
    for elem in reversed(list_glob_gen):
        if elem.exists():
            Path.rename(elem, elem.with_name(f'{normalize(elem.stem)}{elem.suffix}'))
    return files_of_each_cat


if __name__ == '__main__':
    p = Path(r'C:\Users\User02\Desktop\Python Study')
    sort_folder(p)

    # print(files_of_each_cat)
