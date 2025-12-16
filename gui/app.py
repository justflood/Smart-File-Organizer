import customtkinter as ctk
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
from core.organizer import organize_files, undo_last_operation, MODE_ROOT, MODE_FLATTEN, MODE_RECURSIVE
from core.organizer import organize_files, undo_last_operation, MODE_ROOT, MODE_FLATTEN, MODE_RECURSIVE
from core.config import config
import core.config as config_module
from core.localization import translator

import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DisclaimerDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback_accept):
        super().__init__(parent)
        self.callback_accept = callback_accept
        self.title("WARNING / UYARI")
        
        # Adjust geometry to match approx ratio of 184:256 (0.72)
        # 520 / 0.72 ≈ 720. Let's try 540x700 which is spacious and vertical.
        self.geometry("540x700") 
        self.resizable(False, False)
        self.grab_set()
        
        # Icon Support
        try:
            icon_path = config_module.resource_path("icon.ico")
            self.after(200, lambda: self.iconbitmap(icon_path))
        except Exception:
            pass
        
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main Frame
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Language Switcher (New)
        self.lang_var = tk.StringVar(value="English" if config.get("language") == "en" else "Türkçe")
        self.lang_switch = ctk.CTkSegmentedButton(self.frame, values=["English", "Türkçe"], 
                                                  variable=self.lang_var, command=self.change_language)
        self.lang_switch.pack(pady=(10, 0), anchor="ne", padx=10)
        
        # Title
        self.lbl_title = ctk.CTkLabel(self.frame, text=translator.get("disclaimer_title"), 
                                      font=ctk.CTkFont(size=20, weight="bold"), text_color="red")
        self.lbl_title.pack(pady=(10, 10))
        
        # Text
        self.text_frame = ctk.CTkScrollableFrame(self.frame, fg_color="transparent") # letting it fill available space
        self.text_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.lbl_text = ctk.CTkLabel(self.text_frame, text=translator.get("disclaimer_text"), wraplength=460, justify="left")
        self.lbl_text.pack(pady=5, padx=5)
        
        # Checkbox
        self.var_dont_show = tk.BooleanVar(value=False)
        self.chk_dont_show = ctk.CTkCheckBox(self.frame, text=translator.get("disclaimer_check"), variable=self.var_dont_show)
        self.chk_dont_show.pack(pady=10)
        
        # Buttons
        self.btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.btn_frame.pack(pady=(0, 20))
        
        self.btn_exit = ctk.CTkButton(self.btn_frame, text=translator.get("disclaimer_exit"), fg_color="gray", command=self.on_exit)
        self.btn_exit.pack(side="left", padx=10)
        
        self.btn_accept = ctk.CTkButton(self.btn_frame, text=translator.get("disclaimer_accept"), fg_color="red", command=self.on_accept)
        self.btn_accept.pack(side="left", padx=10)

    def change_language(self, value):
        lang_code = "en" if value == "English" else "tr"
        config.set("language", lang_code)
        self.refresh_text()

    def refresh_text(self):
        self.lbl_title.configure(text=translator.get("disclaimer_title"))
        self.lbl_text.configure(text=translator.get("disclaimer_text"))
        self.chk_dont_show.configure(text=translator.get("disclaimer_check"))
        self.btn_exit.configure(text=translator.get("disclaimer_exit"))
        self.btn_accept.configure(text=translator.get("disclaimer_accept"))

    def on_exit(self):
        sys.exit() 

    def on_accept(self):
        if self.var_dont_show.get():
            config.set("agreed_to_terms", True)
        self.callback_accept()
        self.destroy()


import webbrowser
import logging
import traceback
import shutil
from core.config import config, APP_DATA_DIR

# Configure Logging
log_file = os.path.join(APP_DATA_DIR, 'error_log.txt')
logging.basicConfig(filename=log_file, level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ErrorDialog(ctk.CTkToplevel):
    def __init__(self, parent, error_message, traceback_text=None):
        super().__init__(parent)
        self.title(translator.get("crash_title"))
        self.geometry("600x500")
        self.resizable(False, False)
        self.grab_set()
        
        # Icon Support
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            try:
                self.after(200, lambda: self.iconbitmap(icon_path))
            except Exception:
                pass

        self.traceback_text = traceback_text
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Icon/Title
        self.lbl_title = ctk.CTkLabel(self, text=translator.get("crash_title"), 
                                      font=ctk.CTkFont(size=20, weight="bold"), text_color="red")
        self.lbl_title.pack(pady=(20, 10))
        
        # Message
        self.lbl_msg = ctk.CTkLabel(self, text=error_message, wraplength=550)
        self.lbl_msg.pack(pady=10, padx=20)
        
        # Traceback Box
        if traceback_text:
            self.txt_trace = ctk.CTkTextbox(self, height=200)
            self.txt_trace.pack(pady=10, padx=20, fill="both", expand=True)
            self.txt_trace.insert("1.0", traceback_text)
            self.txt_trace.configure(state="disabled") # Read-only
            
        # Button Frame
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)
        
        if traceback_text:
            self.btn_copy = ctk.CTkButton(self.btn_frame, text=translator.get("btn_copy_log"), 
                                          command=self.copy_log, fg_color="gray")
            self.btn_copy.pack(side="left", padx=10)
            
            self.btn_report = ctk.CTkButton(self.btn_frame, text=translator.get("btn_report"), 
                                            command=self.report_issue, fg_color="blue")
            self.btn_report.pack(side="left", padx=10)
            
        self.btn_close = ctk.CTkButton(self.btn_frame, text=translator.get("btn_close"), 
                                       command=self.destroy, fg_color="red")
        self.btn_close.pack(side="left", padx=10)

    def copy_log(self):
        if self.traceback_text:
            self.clipboard_clear()
            self.clipboard_append(self.traceback_text)
            messagebox.showinfo("Copied", "Error log copied to clipboard.")

    def report_issue(self):
        webbrowser.open("https://github.com/justflood/Smart-File-Organizer/issues/new/choose")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title(translator.get("title"))
        self.geometry("750x650")
        
        # Icon Support
        try:
            icon_path = config_module.resource_path("icon.ico")
            self.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Variables
        self.selected_folder = tk.StringVar(value=translator.get("no_folder"))
        self.organize_mode = tk.StringVar(value=MODE_ROOT)
        self.operation_log = []
        self.radio_buttons = [] 
        
        # UI Elements
        self.create_widgets()
        
        # Check Disclaimer
        if not config.get("agreed_to_terms"):
            self.after(100, self.show_disclaimer)

    def show_disclaimer(self):
        # Refresh UI after disclaimer in case language changed there
        DisclaimerDialog(self, self.on_disclaimer_accepted)

    def on_disclaimer_accepted(self):
        self.refresh_ui_texts()
        # Update main lang switcher visual state
        self.lang_var.set("English" if config.get("language") == "en" else "Türkçe")

    def create_widgets(self):
        # Header (Now with Language Switcher)
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Language Switcher
        self.lang_var = tk.StringVar(value="English" if config.get("language") == "en" else "Türkçe")
        self.lang_switch = ctk.CTkSegmentedButton(self.header_frame, values=["English", "Türkçe"], 
                                                  variable=self.lang_var, command=self.change_language)
        self.lang_switch.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        
        self.label_title = ctk.CTkLabel(self.header_frame, text=translator.get("title"), font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.grid(row=0, column=1, pady=5)
        
        self.label_desc = ctk.CTkLabel(self.header_frame, text=translator.get("desc"))
        self.label_desc.grid(row=1, column=1, pady=5)

        # Folder Selection
        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_select_folder = ctk.CTkButton(self.folder_frame, text=translator.get("btn_folder"), command=self.select_folder)
        self.btn_select_folder.pack(side="left", padx=20, pady=20)
        
        self.label_folder_path = ctk.CTkLabel(self.folder_frame, textvariable=self.selected_folder, wraplength=400)
        self.label_folder_path.pack(side="left", padx=10, pady=20)

        # Mode Selection
        self.mode_frame = ctk.CTkFrame(self)
        self.mode_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.label_mode = ctk.CTkLabel(self.mode_frame, text=translator.get("label_mode"), font=ctk.CTkFont(weight="bold"))
        self.label_mode.pack(pady=10, anchor="w", padx=20)

        self._create_radio_option(self.mode_frame, translator.get("mode_root"), MODE_ROOT, translator.get("mode_root_help"))
        self._create_radio_option(self.mode_frame, translator.get("mode_flatten"), MODE_FLATTEN, translator.get("mode_flatten_help"))
        self._create_radio_option(self.mode_frame, translator.get("mode_recursive"), MODE_RECURSIVE, translator.get("mode_recursive_help"))

        # Warning Label
        self.warning_label = ctk.CTkLabel(self, text=translator.get("warning"), 
                                          text_color="red", font=ctk.CTkFont(weight="bold"))
        self.warning_label.grid(row=3, column=0, padx=20, pady=(10, 0))

        # Controls & Progress
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_start = ctk.CTkButton(self.control_frame, text=translator.get("btn_start"), command=self.start_organization_thread, state="disabled", fg_color="green", height=40)
        self.btn_start.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.control_frame)
        self.progress_bar.pack(pady=10, fill="x", padx=20)
        self.progress_bar.set(0)
        
        self.label_status = ctk.CTkLabel(self.control_frame, text=translator.get("status_ready"))
        self.label_status.pack(pady=5)

        # Footer (Undo & Feedback)
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
        
        self.btn_undo = ctk.CTkButton(self.footer_frame, text=translator.get("btn_undo"), command=self.undo_operation, state="disabled", fg_color="red")
        self.btn_undo.pack(side="left", padx=20, pady=10)
        
        self.btn_feedback = ctk.CTkButton(self.footer_frame, text=translator.get("btn_feedback"), 
                                          command=self.open_feedback, fg_color="transparent", 
                                          text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), height=30)
        self.btn_feedback.pack(side="right", padx=20, pady=10)

    def _create_radio_option(self, parent, text, value, help_text):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=5)
        
        radio = ctk.CTkRadioButton(container, text=text, variable=self.organize_mode, value=value)
        radio.pack(side="left")
        self.radio_buttons.append(radio)
        
        # Help Button
        btn_help = ctk.CTkButton(container, text="?", width=20, height=20, fg_color="gray", command=lambda: self.show_help(text, help_text))
        btn_help.pack(side="left", padx=10)

    def change_language(self, value):
        lang_code = "en" if value == "English" else "tr"
        config.set("language", lang_code)
        
        # Refresh UI
        self.refresh_ui_texts()

    def refresh_ui_texts(self):
        # Update simple labels
        self.title(translator.get("title"))
        self.label_title.configure(text=translator.get("title"))
        self.label_desc.configure(text=translator.get("desc"))
        self.btn_select_folder.configure(text=translator.get("btn_folder"))
        self.label_mode.configure(text=translator.get("label_mode"))
        self.warning_label.configure(text=translator.get("warning"))
        self.btn_start.configure(text=translator.get("btn_start"))
        self.label_status.configure(text=translator.get("status_ready"))
        self.btn_undo.configure(text=translator.get("btn_undo"))
        self.btn_feedback.configure(text=translator.get("btn_feedback"))
        
        # Harder part: Radio buttons and their help texts. 
        # Since help text is bound in lambda, we can't easily update it without recreating.
        # For V3, let's just accept that switching language might require restart for complex widgets 
        # OR we can just recreate the mode frame.
        
        # Let's recreate the mode frame content
        for widget in self.mode_frame.winfo_children():
            widget.destroy()
            
        self.radio_buttons.clear()
        
        self.label_mode = ctk.CTkLabel(self.mode_frame, text=translator.get("label_mode"), font=ctk.CTkFont(weight="bold"))
        self.label_mode.pack(pady=10, anchor="w", padx=20)

        self._create_radio_option(self.mode_frame, translator.get("mode_root"), MODE_ROOT, translator.get("mode_root_help"))
        self._create_radio_option(self.mode_frame, translator.get("mode_flatten"), MODE_FLATTEN, translator.get("mode_flatten_help"))
        self._create_radio_option(self.mode_frame, translator.get("mode_recursive"), MODE_RECURSIVE, translator.get("mode_recursive_help"))
        
        # Restore selection
        # (variable is shared so selection stays)

    def show_help(self, title, message):
        messagebox.showinfo(title, message)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder.set(folder_path)
            self.btn_start.configure(state="normal")
            self.label_status.configure(text=f"{translator.get('label_status')} {os.path.basename(folder_path)}") # Simple concat for now

    def update_progress(self, current, total, filename):
        progress = current / total if total > 0 else 0
        self.after(0, lambda: self._update_ui_progress(progress, filename))

    def _update_ui_progress(self, progress, filename):
        self.progress_bar.set(progress)
        self.label_status.configure(text=f"{filename}")

    def start_organization_thread(self):
        folder_path = self.selected_folder.get()
        mode = self.organize_mode.get()
        
        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", translator.get("error_path"))
            return

        self._set_ui_busy()
        
        thread = threading.Thread(target=self.run_organization, args=(folder_path, mode))
        thread.start()

    def run_organization(self, folder_path, mode):
        try:
            self.operation_log = organize_files(folder_path, mode=mode, progress_callback=self.update_progress)
            self.after(0, self.organization_complete)
        except PermissionError:
            self.after(0, lambda: self.show_error_dialog(translator.get("error_permission")))
            self.after(0, self.reset_ui)
        except shutil.Error as e:
            self.after(0, lambda: self.show_error_dialog(f"{translator.get('error_copy')}\n{str(e)}"))
            self.after(0, self.reset_ui)
        except Exception as e:
            error_msg = translator.get("error_unexpected")
            trace = traceback.format_exc()
            logging.error(f"Organization Error: {str(e)}\n{trace}")
            self.after(0, lambda: self.show_error_dialog(error_msg, trace))
            self.after(0, self.reset_ui)

    def show_error_dialog(self, message, trace=None):
        ErrorDialog(self, message, trace)

    def organization_complete(self):
        self.label_status.configure(text=translator.get("status_done"))
        messagebox.showinfo("Success", translator.get("msg_success"))
        self.reset_ui()
        if self.operation_log:
            self.btn_undo.configure(state="normal")

    def undo_operation(self):
        if not self.operation_log:
            return
            
        if messagebox.askyesno("Undo", translator.get("msg_undo_confirm")):
            self._set_ui_busy()
            thread = threading.Thread(target=self.run_undo)
            thread.start()

    def run_undo(self):
        try:
            undo_last_operation(self.operation_log, progress_callback=self.update_progress)
            self.after(0, self.undo_complete)
        except PermissionError:
            self.after(0, lambda: self.show_error_dialog(translator.get("error_permission")))
            self.after(0, self.reset_ui)
        except Exception as e:
            error_msg = translator.get("error_unexpected")
            trace = traceback.format_exc()
            logging.error(f"Undo Error: {str(e)}\n{trace}")
            self.after(0, lambda: self.show_error_dialog(error_msg, trace))
            self.after(0, self.reset_ui)

    def undo_complete(self):
        self.operation_log = []
        self.reset_ui()
        self.btn_undo.configure(state="disabled")
        self.label_status.configure(text=translator.get("status_undo"))
        messagebox.showinfo("Info", translator.get("msg_undo"))

    def open_feedback(self):
        webbrowser.open("https://github.com/justflood/Smart-File-Organizer/issues/new/choose")
        
    def _set_ui_busy(self):
        self.btn_start.configure(state="disabled")
        self.btn_select_folder.configure(state="disabled")
        self.btn_undo.configure(state="disabled")
        self.lang_switch.configure(state="disabled")
        for radio in self.radio_buttons:
            radio.configure(state="disabled")
        self.progress_bar.set(0)

    def reset_ui(self):
        self.btn_start.configure(state="normal")
        self.btn_select_folder.configure(state="normal")
        self.lang_switch.configure(state="normal")
        self.progress_bar.set(0)
        for radio in self.radio_buttons:
            radio.configure(state="normal")
