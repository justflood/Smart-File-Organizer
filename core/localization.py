from core.config import config

TEXTS = {
    "en": {
        "title": "Smart File Organizer v0.1",
        "desc": "Organize your files instantly with a single click.",
        "btn_folder": "Select Folder",
        "no_folder": "No folder selected",
        "label_mode": "Organization Mode:",
        "mode_root": "Root Folder Only",
        "mode_root_help": "Standard Mode.\nOnly organizes files in the selected folder.\nSubfolders are ignored.",
        "mode_flatten": "Flatten (Centralize)",
        "mode_flatten_help": "Deep Maintenance Mode.\nSearches deep into all subfolders.\nMoves ALL found files to the main folder categories.",
        "mode_recursive": "Recursive (In-Place)",
        "mode_recursive_help": "Preservation Mode.\nGoes into each subfolder and organizes them internally.\nKeeps your folder structure intact.",
        "warning": "⚠️ WARNING: Do not use on System, Game, or Code Project folders!",
        "btn_start": "Start Organizing",
        "status_ready": "Ready",
        "btn_undo": "Undo Last Operation",
        "status_done": "Completed!",
        "msg_success": "Files organized successfully!",
        "status_undo": "Undo Completed",
        "msg_undo": "Undo completed successfully.",
        "msg_undo_confirm": "Are you sure you want to undo the last operation?",
        "error_path": "Invalid folder path!",
        "disclaimer_title": "WARNING / UYARI",
        "disclaimer_text": """
LEGAL DISCLAIMER / YASAL UYARI

Usage of this software may PERMANENTLY altering your file structure.
The developer is NOT RESPONSIBLE for any data loss, file corruption, or system instability.

DO NOT USE THIS SOFTWARE ON:
- Windows/System32 Folders
- Program Files / AppData
- Git Repositories / Code Projects (node_modules, venv)
- Game Installation Folders (Steam, libraries)

By clicking 'I Accept', you acknowledge that YOU are solely responsible for your data.
        """,
        "disclaimer_accept": "I Accept",
        "disclaimer_exit": "Exit",
        "disclaimer_check": "Don't show this again",
        "btn_feedback": "Report Bug / Suggest Feature",
        "error_permission": "Permission Denied! Please ensure the file is not open or run the program as Administrator.",
        "error_copy": "File copy error occurred.",
        "error_unexpected": "An unexpected error occurred during the operation.",
        "crash_title": "Error / Hata",
        "crash_msg": "An unexpected error occurred.",
        "btn_copy_log": "Copy Error Log",
        "btn_report": "Report on GitHub",
        "btn_close": "Close",
    },
    "tr": {
        "title": "Akıllı Dosya Düzenleyici v0.1",
        "desc": "Dosyalarınızı tek tıkla anında düzenleyin.",
        "btn_folder": "Klasör Seç",
        "no_folder": "Klasör seçilmedi",
        "label_mode": "Düzenleme Modu:",
        "mode_root": "Sadece Kök Klasör",
        "mode_root_help": "Standart Mod.\nSadece seçili klasördeki dosyaları düzenler.\nAlt klasörlere dokunmaz.",
        "mode_flatten": "Hepsini Topla (Flatten)",
        "mode_flatten_help": "Derin Temizlik Modu.\nTüm alt klasörleri tarar.\nBulduğu HER dosyayı ana klasördeki kategorilere taşır.",
        "mode_recursive": "Yerinde Düzenle (Recursive)",
        "mode_recursive_help": "Koruma Modu.\nHer alt klasörün içine girer ve onları kendi içinde düzenler.\nKlasör yapınızı bozmaz.",
        "warning": "⚠️ UYARI: Sistem, Oyun veya Kod Projesi klasörlerinde kullanmayın!",
        "btn_start": "Düzenlemeyi Başlat",
        "status_ready": "Hazır",
        "btn_undo": "Son İşlemi Geri Al",
        "status_done": "Tamamlandı!",
        "msg_success": "Dosyalar başarıyla düzenlendi!",
        "status_undo": "Geri Alma Tamamlandı",
        "msg_undo": "İşlem başarıyla geri alındı.",
        "msg_undo_confirm": "Son işlemi geri almak istediğinize emin misiniz?",
        "error_path": "Geçersiz klasör yolu!",
        "disclaimer_title": "YASAL UYARI / WARNING",
        "disclaimer_text": """
YASAL UYARI / LEGAL DISCLAIMER

Bu yazılımın kullanımı dosya yapınızı KALICI OLARAK değiştirebilir.
Geliştirici, oluşabilecek veri kaybı, bozulma veya sistem hatalarından SORUMLU DEĞİLDİR.

BU YAZILIMI ŞURALARDA KULLANMAYIN:
- Windows/System32 Klasörleri
- Program Files / AppData
- Git Depoları / Yazılım Projeleri (node_modules, venv)
- Oyun Kurulum Klasörleri (Steam kütüphaneleri)

'Kabul Ediyorum' butonuna tıklayarak, verilerinizin sorumluluğunun tamamen SİZE ait olduğunu kabul edersiniz.
        """,
        "disclaimer_accept": "Kabul Ediyorum",
        "disclaimer_exit": "Çıkış",
        "disclaimer_check": "Bir daha gösterme",
        "btn_feedback": "Hata Bildir / Öneri Yap",
        "error_permission": "Erişim Reddedildi! Lütfen dosyanın açık olmadığından emin olun veya programı Yönetici olarak çalıştırın.",
        "error_copy": "Dosya kopyalama hatası oluştu.",
        "error_unexpected": "İşlem sırasında beklenmedik bir hata oluştu.",
        "crash_title": "Hata / Error",
        "crash_msg": "Beklenmedik bir hata oluştu.",
        "btn_copy_log": "Hata Kaydını Kopyala",
        "btn_report": "GitHub'da Raporla",
        "btn_close": "Kapat",
    }
}

class Localization:
    def get(self, key):
        lang = config.get("language")
        if lang not in TEXTS:
            lang = "en"
        return TEXTS[lang].get(key, key)

translator = Localization()
