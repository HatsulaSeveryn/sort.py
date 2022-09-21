import shutil
from pathlib import Path
from clean_folder import constans
import send2trash
from sys import argv

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


def translate(name: str) -> str:
    """Function for transliteration"""
    return name.translate(constans.TRANS)


def normalize(file_or_folder_name: str) -> str:
    """
    Function that swaps cyrillic letters with Latin,
    and swaps non ascii letters and digits with
    """
    normal_name = ''
    for char in file_or_folder_name:
        if char in constans.CYRILLIC_SYMBOLS:
            normal_name += translate(char)
        elif char.isalnum():
            normal_name += char
        else:
            normal_name += '_'
    return normal_name


def new_folder(file_abs_path: Path, new_fold: str) -> None:
    """Function for creating folder and moving file to it"""
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


def sort_folder(fold_path: Path = None) -> dict:
    """
    Function for sorting files in folder and all sub-folders.
    Parameter fold_path is used for recursive purpose to indicate
    child folder (sub-folder).
    Recursive function call is used for bottom-top recursion.
    """
    if len(argv) < 2:
        print('Enter path to folder which should be cleaned')
        exit()
    fold_path = Path(argv[1])
    if not (fold_path.exists() and fold_path.is_dir()):
        print('Incorrect path')
        exit()
    list_glob_gen = []
    for child in fold_path.glob('*'):
        if child.is_file():
            if child.name.rfind('.') == 0:
                suffix_temp = child.name
            else:
                suffix_temp = child.suffix
            if suffix_temp in constans.IMAGE_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'images')
                images.append(f"{child.parent / 'images' / child.name}")
            elif suffix_temp in constans.VIDEO_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'video')
                videos.append(f"{child.parent / 'video' / child.name}")
            elif suffix_temp in constans.DOC_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'documents')
                texts.append(f"{child.parent / 'documents' / child.name}")
            elif suffix_temp in constans.MUSIC_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'audio')
                audio.append(f"{child.parent / 'audio' / child.name}")
            elif suffix_temp in constans.ARCH_FILES:
                known_formats.add(suffix_temp)
                new_folder(child, 'archives')
                archives.append(f"{child.parent / 'archives' / child.name}")
                shutil.unpack_archive(child.parent / 'archives' / child.name,
                                      child.parent / 'archives' / child.stem)
            else:
                unknown_formats.add(suffix_temp)
                other_files.append(str(child))
        elif child.is_dir() and (child.name not in constans.IGNORE_FOLDERS):
            sort_folder(child)
            if not any(child.iterdir()):
                empty_fold_del.append(child)
                send2trash.send2trash(child)
    for child in fold_path.glob('**/*'):
        list_glob_gen.append(child)
    for elem in reversed(list_glob_gen):
        if elem.exists():
            elem.rename(elem.with_name(f'{normalize(elem.stem)}{elem.suffix}'))
    return files_of_each_cat


if __name__ == '__main__':
    sort_folder()
