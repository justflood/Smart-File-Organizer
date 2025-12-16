<img width="934" height="848" alt="Image" src="https://github.com/user-attachments/assets/063a0845-0b1f-4e7d-9452-402692463240" />

---

# 📂 Smart File Organizer

![Version](https://img.shields.io/badge/version-v0.1.0-blue) ![Platform](https://img.shields.io/badge/platform-Windows-win) ![License](https://img.shields.io/badge/license-MIT-green)

**Smart File Organizer** is a modern, open-source desktop utility designed to organize messy folders automatically. Whether you want to clean up your Downloads folder or organize a complex directory tree, this tool handles it securely and efficiently.

*(Türkçe açıklama aşağıdadır / Turkish description is below)* 👇

---

## ✨ Features

* **🚀 3 Organization Modes:**
    * **Root Only:** Organizes only the selected folder.
    * **Flatten:** Pulls files from all subfolders into one place.
    * **Recursive:** Organizes inside subfolders without breaking structure.
* **🛡️ Safety Guard:** Automatically ignores system folders (`Windows`, `Program Files`) and developer directories (`node_modules`, `.git`, `venv`).
* **↩️ Undo System:** Full rollback capability with session logging.
* **🎨 Modern UI:** Dark-themed interface built with CustomTkinter.
* **🌍 Multi-Language:** Switch between English and Turkish instantly.
* **⚡ Portable:** Runs as a single `.exe` file without installation.

---

## 📦 Installation & Usage

### Method 1: Download EXE (Recommended)
1.  Go to the [Releases Page](https://github.com/justflood/Smart-File-Organizer/releases).
2.  Download `Smart File Organizer.exe`.
3.  Double-click to run!

### Method 2: Run from Source
If you are a developer, you can run it via Python:

```bash
# Clone the repository
git clone https://github.com/justflood/Smart-File-Organizer.git

# Install requirements
pip install -r requirements.txt

# Run the app
python main.py
```

---

## ⚠️ Disclaimer
This software modifies your file structure. While it includes safety features (like duplicate handling and ignore lists), ALWAYS backup your critical data before running organization tools on important directories. The developer is not responsible for any data loss.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **GUI:** CustomTkinter
* **Packaging:** PyInstaller
* **Config:** JSON (Stored in LocalAppData)

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

**Developed by FloodTechLab**

---

# 🇹🇷 Smart File Organizer (Türkçe)

**Smart File Organizer**, karışık klasörlerinizi (İndirilenler, Masaüstü vb.) tek tıkla türlerine göre (Resimler, Videolar, Belgeler) ayıran modern bir araçtır.

## ✨ Özellikler

* **3 Farklı Mod:** İster sadece ana klasörü, ister tüm alt klasörleri toplayarak, isterseniz de alt klasörlerin düzenini bozmadan temizlik yapın.
* **Geliştirici Dostu:** Yazılım projelerinizi (`node_modules`, `.git` vb.) ve oyun dosyalarınızı tanır, onlara DOKUNMAZ.
* **Geri Al (Undo):** Yanlışlıkla mı düzenlediniz? Tek tıkla her şeyi eski haline getirin.
* **Türkçe Dil Desteği:** Ayarlardan Türkçe'yi seçerek kullanabilirsiniz.

## 📥 Kurulum
[Releases](https://github.com/justflood/Smart-File-Organizer/releases) sayfasından `.exe` dosyasını indirip direkt çalıştırabilirsiniz. Kurulum gerektirmez.

---

**FloodTechLab Tarafından Geliştirildi**

---
