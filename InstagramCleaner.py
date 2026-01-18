import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
import webbrowser

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AnimatedButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_color = kwargs.get("fg_color", "#6366f1")
        self.hover_color = kwargs.get("hover_color", "#818cf8")
        
    def animate_click(self, callback):
        original_color = self._fg_color
        self.configure(fg_color="#4f46e5")
        self.after(100, lambda: self.configure(fg_color=original_color))
        self.after(150, callback)


class StatCard(ctk.CTkFrame):
    def __init__(self, master, title, value="0", icon="📊", color="#6366f1", **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#1e1e2e", corner_radius=15)
        
        self.icon_label = ctk.CTkLabel(
            self, text=icon, font=("Segoe UI Emoji", 32)
        )
        self.icon_label.pack(pady=(15, 5))
        
        self.value_label = ctk.CTkLabel(
            self, text=value, font=("Segoe UI", 36, "bold"), text_color=color
        )
        self.value_label.pack(pady=5)
        
        self.title_label = ctk.CTkLabel(
            self, text=title, font=("Segoe UI", 12), text_color="#a1a1aa"
        )
        self.title_label.pack(pady=(0, 15))
        
        self._target_value = 0
        self._current_value = 0
    
    def set_value(self, value, animate=True):
        if animate and value > 0:
            self._target_value = value
            self._current_value = 0
            self._animate_count()
        else:
            self.value_label.configure(text=str(value))
    
    def _animate_count(self):
        if self._current_value < self._target_value:
            step = max(1, self._target_value // 20)
            self._current_value = min(self._current_value + step, self._target_value)
            self.value_label.configure(text=str(self._current_value))
            self.after(30, self._animate_count)


class FileSelector(ctk.CTkFrame):
    def __init__(self, master, label, placeholder="Select a file...", **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        
        self.file_path = ctk.StringVar()
        
        self.label = ctk.CTkLabel(
            self, text=label, font=("Segoe UI", 13, "bold"), 
            text_color="#e4e4e7", anchor="w"
        )
        self.label.pack(fill="x", pady=(0, 8))
        
        container = ctk.CTkFrame(self, fg_color="#27273a", corner_radius=12)
        container.pack(fill="x")
        
        self.entry = ctk.CTkEntry(
            container, textvariable=self.file_path, 
            placeholder_text=placeholder,
            font=("Segoe UI", 12),
            fg_color="transparent",
            border_width=0,
            height=45
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(15, 5))
        
        self.browse_btn = ctk.CTkButton(
            container, text="📁 Browse", width=100, height=35,
            font=("Segoe UI", 12, "bold"),
            fg_color="#6366f1", hover_color="#818cf8",
            corner_radius=8,
            command=self._browse
        )
        self.browse_btn.pack(side="right", padx=5, pady=5)
    
    def _browse(self):
        filename = filedialog.askopenfilename(
            title=f"Select {self.label.cget('text')}",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            self.entry.configure(text_color="#22c55e")
            self.after(500, lambda: self.entry.configure(text_color="#e4e4e7"))
    
    def get(self):
        return self.file_path.get()


class UserListItem(ctk.CTkFrame):
    def __init__(self, master, username, index, **kwargs):
        super().__init__(master, **kwargs)
        self.username = username
        self.configure(fg_color="#27273a", corner_radius=10, height=50, cursor="hand2")
        self.pack_propagate(False)
        
        badge = ctk.CTkLabel(
            self, text=str(index), width=35, height=35,
            font=("Segoe UI", 11, "bold"),
            fg_color="#6366f1", corner_radius=8,
            text_color="white"
        )
        badge.pack(side="left", padx=(10, 15), pady=7)
        
        user_label = ctk.CTkLabel(
            self, text=f"@{username}", 
            font=("Segoe UI", 13),
            text_color="#e4e4e7", anchor="w"
        )
        user_label.pack(side="left", fill="x", expand=True)
        
        open_btn = ctk.CTkButton(
            self, text="Open Profile →", width=110, height=30,
            font=("Segoe UI", 11, "bold"),
            fg_color="#6366f1", hover_color="#818cf8",
            corner_radius=6,
            command=self._open_profile
        )
        open_btn.pack(side="right", padx=(5, 10))
        
        ig_icon = ctk.CTkLabel(
            self, text="📷", font=("Segoe UI Emoji", 16)
        )
        ig_icon.pack(side="right", padx=(0, 5))
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        for child in [badge, user_label, ig_icon]:
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)
            child.bind("<Button-1>", self._on_click)
    
    def _open_profile(self):
        url = f"https://instagram.com/{self.username}"
        webbrowser.open(url)
    
    def _on_click(self, event):
        self._open_profile()
    
    def _on_enter(self, event):
        self.configure(fg_color="#363654")
    
    def _on_leave(self, event):
        self.configure(fg_color="#27273a")


class InstagramCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("✨ InstagramCleaner")
        self.geometry("900x700")
        self.minsize(600, 900)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_container = ctk.CTkFrame(self, fg_color="#0f0f1a", corner_radius=0)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=0)
        self.main_container.grid_rowconfigure(1, weight=0)
        self.main_container.grid_rowconfigure(2, weight=0)
        self.main_container.grid_rowconfigure(3, weight=1)
        self.main_container.grid_rowconfigure(4, weight=0)
        
        self.non_mutual_list = []
        
        self._create_header()
        self._create_file_section()
        self._create_stats_section()
        self._create_results_section()
        self._create_footer()
        
        self.after(100, self._startup_animation)
    
    def _startup_animation(self):
        self.attributes("-alpha", 0)
        self._fade_in(0)
    
    def _fade_in(self, alpha):
        if alpha < 1:
            alpha += 0.1
            self.attributes("-alpha", alpha)
            self.after(10, lambda: self._fade_in(alpha))
    
    def _create_header(self):
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))
        
        logo_frame = ctk.CTkFrame(header, fg_color="#6366f1", width=60, height=60, corner_radius=15)
        logo_frame.pack(side="left")
        logo_frame.pack_propagate(False)
        
        logo_text = ctk.CTkLabel(logo_frame, text="IG", font=("Segoe UI", 22, "bold"), text_color="white")
        logo_text.place(relx=0.5, rely=0.5, anchor="center")
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=20)
        
        title = ctk.CTkLabel(
            title_frame, text="InstagramCleaner", 
            font=("Segoe UI", 28, "bold"),
            text_color="#ffffff"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            title_frame, text="Find who doesn't follow you back",
            font=("Segoe UI", 13),
            text_color="#71717a"
        )
        subtitle.pack(anchor="w")
    
    def _create_file_section(self):
        file_frame = ctk.CTkFrame(self.main_container, fg_color="#1a1a2e", corner_radius=20)
        file_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=10)
        
        inner_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        inner_frame.pack(fill="x", padx=25, pady=25)
        
        self.followers_selector = FileSelector(
            inner_frame, "📥 Followers File (followers_1.json)",
            "Select your followers JSON file..."
        )
        self.followers_selector.pack(fill="x", pady=(0, 15))
        
        self.following_selector = FileSelector(
            inner_frame, "📤 Following File (following.json)",
            "Select your following JSON file..."
        )
        self.following_selector.pack(fill="x")
        
        self.analyze_btn = ctk.CTkButton(
            inner_frame, text="🔍  Analyze Now", height=55,
            font=("Segoe UI", 15, "bold"),
            fg_color="#6366f1", hover_color="#818cf8",
            corner_radius=12,
            command=self._start_analysis
        )
        self.analyze_btn.pack(fill="x", pady=(25, 0))
        
        self.progress = ctk.CTkProgressBar(inner_frame, height=6, corner_radius=3)
        self.progress.set(0)
    
    def _create_stats_section(self):
        stats_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        stats_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=15)
        
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.followers_card = StatCard(
            stats_frame, "Followers", "—", "👥", "#22c55e"
        )
        self.followers_card.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.following_card = StatCard(
            stats_frame, "Following", "—", "👤", "#3b82f6"
        )
        self.following_card.grid(row=0, column=1, sticky="ew", padx=5)
        
        self.non_mutual_card = StatCard(
            stats_frame, "Non-Mutual", "—", "💔", "#ef4444"
        )
        self.non_mutual_card.grid(row=0, column=2, sticky="ew", padx=(10, 0))
    
    def _create_results_section(self):
        results_container = ctk.CTkFrame(self.main_container, fg_color="#1a1a2e", corner_radius=20)
        results_container.grid(row=3, column=0, sticky="nsew", padx=30, pady=10)
        
        header_frame = ctk.CTkFrame(results_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))
        
        results_title = ctk.CTkLabel(
            header_frame, text="📋 Non-Mutual Users",
            font=("Segoe UI", 16, "bold"),
            text_color="#e4e4e7"
        )
        results_title.pack(side="left")
        
        self.results_count_label = ctk.CTkLabel(
            header_frame, text="",
            font=("Segoe UI", 12),
            text_color="#71717a"
        )
        self.results_count_label.pack(side="right")
        
        self.results_scroll = ctk.CTkScrollableFrame(
            results_container, fg_color="transparent",
            scrollbar_button_color="#6366f1",
            scrollbar_button_hover_color="#818cf8"
        )
        self.results_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.placeholder = ctk.CTkLabel(
            self.results_scroll,
            text="🔍\n\nSelect your Instagram data files and click Analyze\nto see who doesn't follow you back",
            font=("Segoe UI", 14),
            text_color="#52525b",
            justify="center"
        )
        self.placeholder.pack(expand=True, pady=50)
    
    def _create_footer(self):
        footer = ctk.CTkFrame(self.main_container, fg_color="transparent", height=70)
        footer.grid(row=4, column=0, sticky="ew", padx=30, pady=(5, 20))
        
        self.export_btn = ctk.CTkButton(
            footer, text="📄  Export to TXT", height=45, width=180,
            font=("Segoe UI", 13, "bold"),
            fg_color="#27273a", hover_color="#363654",
            border_width=2, border_color="#6366f1",
            corner_radius=10,
            command=self._export_results,
            state="disabled"
        )
        self.export_btn.pack(side="left")
        
        self.copy_btn = ctk.CTkButton(
            footer, text="📋  Copy All", height=45, width=140,
            font=("Segoe UI", 13, "bold"),
            fg_color="#27273a", hover_color="#363654",
            border_width=2, border_color="#6366f1",
            corner_radius=10,
            command=self._copy_to_clipboard,
            state="disabled"
        )
        self.copy_btn.pack(side="left", padx=10)
        
        credits = ctk.CTkLabel(
            footer, text="Made with 💜 by Michele Gramegna",
            font=("Segoe UI", 11),
            text_color="#52525b"
        )
        credits.pack(side="right")
    
    def _start_analysis(self):
        if not self.followers_selector.get() or not self.following_selector.get():
            self._show_toast("⚠️ Please select both files first!", "#f59e0b")
            return
        
        self.analyze_btn.configure(text="⏳  Analyzing...", state="disabled")
        self.progress.pack(fill="x", pady=(15, 0))
        self.progress.set(0)
        
        thread = threading.Thread(target=self._analyze)
        thread.start()
    
    def _analyze(self):
        try:
            for i in range(3):
                self.after(i * 200, lambda v=i*0.3: self.progress.set(v))
            
            with open(self.followers_selector.get(), "r", encoding="utf-8") as f:
                followers_data = json.load(f)
            
            self.after(600, lambda: self.progress.set(0.5))
            
            with open(self.following_selector.get(), "r", encoding="utf-8") as f:
                following_data = json.load(f)
            
            self.after(800, lambda: self.progress.set(0.7))
            
            followers_usernames = set()
            for entry in followers_data:
                for s in entry.get("string_list_data", []):
                    username = s.get("value")
                    if username:
                        followers_usernames.add(username)
            
            following_usernames = set()
            for entry in following_data.get("relationships_following", []):
                username = entry.get("title")
                if username:
                    following_usernames.add(username)
            
            self.after(1000, lambda: self.progress.set(0.9))
            
            self.non_mutual_list = sorted(following_usernames - followers_usernames)
            
            self.after(1200, lambda: self._display_results(
                len(followers_usernames), 
                len(following_usernames)
            ))
            
        except FileNotFoundError as e:
            self.after(0, lambda: self._show_error(f"File not found: {e.filename}"))
        except json.JSONDecodeError:
            self.after(0, lambda: self._show_error("Invalid JSON file format"))
        except Exception as e:
            self.after(0, lambda: self._show_error(str(e)))
    
    def _display_results(self, followers_count, following_count):
        self.progress.pack_forget()
        self.analyze_btn.configure(text="🔍  Analyze Now", state="normal")
        
        self.followers_card.set_value(followers_count)
        self.following_card.set_value(following_count)
        self.non_mutual_card.set_value(len(self.non_mutual_list))
        
        self.placeholder.pack_forget()
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        for i, username in enumerate(self.non_mutual_list):
            self._add_result_item(username, i + 1)
        
        count = len(self.non_mutual_list)
        self.results_count_label.configure(
            text=f"{count} user{'s' if count != 1 else ''} found"
        )
        
        if count > 0:
            self.export_btn.configure(state="normal")
            self.copy_btn.configure(state="normal")
            self._show_toast(f"✅ Found {count} non-mutual users!", "#22c55e")
        else:
            self._show_toast("🎉 Everyone follows you back!", "#22c55e")
    
    def _add_result_item(self, username, index):
        item = UserListItem(self.results_scroll, username, index)
        item.pack(fill="x", pady=3)
    
    def _show_toast(self, message, color):
        toast = ctk.CTkFrame(self, fg_color=color, corner_radius=10)
        toast.place(relx=0.5, rely=0.95, anchor="center")
        
        label = ctk.CTkLabel(
            toast, text=message,
            font=("Segoe UI", 13, "bold"),
            text_color="white"
        )
        label.pack(padx=20, pady=10)
        
        self.after(2500, lambda: toast.destroy())
    
    def _show_error(self, message):
        self.progress.pack_forget()
        self.analyze_btn.configure(text="🔍  Analyze Now", state="normal")
        self._show_toast(f"❌ Error: {message}", "#ef4444")
    
    def _export_results(self):
        if not self.non_mutual_list:
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("╔══════════════════════════════════════════════════╗\n")
                    f.write("║   INSTAGRAMCLEANER - NON-MUTUAL USERS REPORT     ║\n")
                    f.write("╚══════════════════════════════════════════════════╝\n\n")
                    f.write(f"Total: {len(self.non_mutual_list)} users\n")
                    f.write("─" * 44 + "\n\n")
                    for i, username in enumerate(self.non_mutual_list, 1):
                        f.write(f"{i:4}. @{username}\n")
                self._show_toast("✅ Exported successfully!", "#22c55e")
            except Exception as e:
                self._show_toast(f"❌ Export failed: {str(e)}", "#ef4444")
    
    def _copy_to_clipboard(self):
        if not self.non_mutual_list:
            return
        
        text = "\n".join([f"@{u}" for u in self.non_mutual_list])
        self.clipboard_clear()
        self.clipboard_append(text)
        self._show_toast("📋 Copied to clipboard!", "#22c55e")


def main():
    app = InstagramCleanerApp()
    app.mainloop()


if __name__ == "__main__":
    main()