# File extension mapping
# Updated for English compatibility

FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.svg', '.webp'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.rtf', '.csv'],
    'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso'],
    'Programs': ['.exe', '.msi', '.bat', '.sh', '.apk', '.app'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.json', '.xml', '.sql']
}

# Reverse mapping
EXTENSION_MAP = {}
for category, extensions in FILE_CATEGORIES.items():
    for ext in extensions:
        EXTENSION_MAP[ext] = category
