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