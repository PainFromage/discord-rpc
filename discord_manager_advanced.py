"""
Discord Bot & Rich Presence Manager Advanced
Application complète pour gérer bot Discord et Rich Presence avec assets
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import time
import threading
import base64
import requests
from pypresence import Presence
from PIL import Image, ImageTk
import io

class DiscordAdvancedManager:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_notebook()
        self.load_config()
        
        # RPC
        self.rpc = None
        self.rpc_connected = False
        self.update_thread = None
        
        # Bot
        self.bot_session = requests.Session()
        self.application_id = None
        
    def setup_window(self):
        """Configuration de la fenêtre principale"""
        self.root.title("Discord Bot & RPC Manager Advanced")
        self.root.geometry("700x800")
        self.root.resizable(True, True)
        
        # Couleurs Discord
        self.colors = {
            'bg': '#2C2F33',
            'card': '#36393F',
            'accent': '#7289DA',
            'success': '#43B581',
            'danger': '#F04747',
            'warning': '#FAA61A',
            'text': '#FFFFFF',
            'text_muted': '#B9BBBE'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
    def setup_variables(self):
        """Initialisation des variables"""
        # RPC Variables
        self.client_id_var = tk.StringVar()
        self.details_var = tk.StringVar()
        self.state_var = tk.StringVar()
        self.large_image_var = tk.StringVar()
        self.large_text_var = tk.StringVar()
        self.small_image_var = tk.StringVar()
        self.small_text_var = tk.StringVar()
        self.show_time_var = tk.BooleanVar()
        self.rpc_status_var = tk.StringVar(value="❌ RPC Déconnecté")
        
        # Bot Variables
        self.bot_token_var = tk.StringVar()
        self.bot_name_var = tk.StringVar()
        self.bot_status_var = tk.StringVar(value="❌ Bot Déconnecté")
        
        # Assets Variables
        self.assets_list = []
        
    def setup_styles(self):
        """Configuration des styles"""
        style = ttk.Style()
        
        # Style pour les frames
        style.configure('Card.TFrame', 
                       background=self.colors['card'],
                       relief='flat')
        
        # Style pour les labels
        style.configure('Title.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Heading.TLabel',
                       background=self.colors['card'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Info.TLabel',
                       background=self.colors['card'],
                       foreground=self.colors['text_muted'],
                       font=('Segoe UI', 9))
        
        # Style pour le notebook
        style.configure('Custom.TNotebook', 
                       background=self.colors['bg'],
                       tabposition='n',
                       borderwidth=0)
        
        style.configure('Custom.TNotebook.Tab',
                       background=self.colors['card'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10),
                       padding=[20, 10],
                       borderwidth=1,
                       focuscolor='none')
        
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', self.colors['accent']),
                           ('active', self.colors['bg'])],
                 foreground=[('selected', self.colors['text']),
                           ('active', self.colors['text'])])
        
    def create_notebook(self):
        """Création du système d'onglets"""
        # Frame principal pour contenir le notebook
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill="both", expand=True)
        
        # Notebook (onglets) avec style amélioré
        self.notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Onglet Rich Presence
        self.create_rpc_tab()
        
        # Onglet Bot Manager
        self.create_bot_tab()
        
        # Onglet Assets Manager
        self.create_assets_tab()
        
    def create_rpc_tab(self):
        """Création de l'onglet Rich Presence"""
        # Frame avec scroll pour RPC
        rpc_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(rpc_frame, text="🎮 Rich Presence")
        
        # Canvas pour scroll
        canvas = tk.Canvas(rpc_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(rpc_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Ajuster la largeur
        def configure_scroll_region(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', configure_scroll_region)
        
        # Contenu RPC
        self.create_rpc_content(scrollable_frame)
        
        # Bind molette
        self.bind_mouse_wheel_to_canvas(canvas)
        
    def create_rpc_content(self, parent):
        """Contenu de l'onglet RPC"""
        # Titre
        title_frame = tk.Frame(parent, bg=self.colors['bg'], height=60)
        title_frame.pack(fill='x', padx=20, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🎮 Discord Rich Presence", 
                             bg=self.colors['bg'], fg=self.colors['text'],
                             font=('Segoe UI', 16, 'bold'))
        title_label.pack(expand=True)
        
        # Status RPC
        status_frame = tk.Frame(parent, bg=self.colors['bg'])
        status_frame.pack(fill='x', padx=20, pady=5)
        
        self.rpc_status_label = tk.Label(status_frame, 
                                       textvariable=self.rpc_status_var,
                                       bg=self.colors['bg'],
                                       fg=self.colors['danger'],
                                       font=('Segoe UI', 10, 'bold'))
        self.rpc_status_label.pack()
        
        # Configuration RPC
        self.create_rpc_config_section(parent)
        self.create_rpc_text_section(parent)
        self.create_rpc_image_section(parent)
        self.create_rpc_options_section(parent)
        self.create_rpc_buttons(parent)
        
    def create_bot_tab(self):
        """Création de l'onglet Bot Manager"""
        bot_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(bot_frame, text="🤖 Bot Manager")
        
        # Canvas pour scroll
        canvas = tk.Canvas(bot_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(bot_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def configure_scroll_region(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', configure_scroll_region)
        
        # Contenu Bot
        self.create_bot_content(scrollable_frame)
        self.bind_mouse_wheel_to_canvas(canvas)
        
    def create_bot_content(self, parent):
        """Contenu de l'onglet Bot"""
        # Titre
        title_frame = tk.Frame(parent, bg=self.colors['bg'], height=60)
        title_frame.pack(fill='x', padx=20, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🤖 Discord Bot Manager", 
                             bg=self.colors['bg'], fg=self.colors['text'],
                             font=('Segoe UI', 16, 'bold'))
        title_label.pack(expand=True)
        
        # Status Bot
        status_frame = tk.Frame(parent, bg=self.colors['bg'])
        status_frame.pack(fill='x', padx=20, pady=5)
        
        self.bot_status_label = tk.Label(status_frame, 
                                       textvariable=self.bot_status_var,
                                       bg=self.colors['bg'],
                                       fg=self.colors['danger'],
                                       font=('Segoe UI', 10, 'bold'))
        self.bot_status_label.pack()
        
        # Configuration Bot
        self.create_bot_config_section(parent)
        self.create_bot_profile_section(parent)
        self.create_bot_buttons(parent)
        
    def create_assets_tab(self):
        """Création de l'onglet Assets Manager"""
        assets_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(assets_frame, text="🖼️ Assets Manager")
        
        # Canvas pour scroll
        canvas = tk.Canvas(assets_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(assets_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def configure_scroll_region(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', configure_scroll_region)
        
        # Contenu Assets
        self.create_assets_content(scrollable_frame)
        self.bind_mouse_wheel_to_canvas(canvas)
        
    def create_assets_content(self, parent):
        """Contenu de l'onglet Assets"""
        # Titre
        title_frame = tk.Frame(parent, bg=self.colors['bg'], height=60)
        title_frame.pack(fill='x', padx=20, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🖼️ Assets Manager", 
                             bg=self.colors['bg'], fg=self.colors['text'],
                             font=('Segoe UI', 16, 'bold'))
        title_label.pack(expand=True)
        
        # Section ajout d'asset
        self.create_add_asset_section(parent)
        
        # Section liste des assets
        self.create_assets_list_section(parent)
        
    def bind_mouse_wheel_to_canvas(self, canvas):
        """Bind la molette à un canvas spécifique"""
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        def _on_mousewheel_linux_up(event):
            canvas.yview_scroll(-1, "units")
            
        def _on_mousewheel_linux_down(event):
            canvas.yview_scroll(1, "units")
        
        # Bind les événements quand la souris entre dans le canvas
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", _on_mousewheel_linux_up)
            canvas.bind_all("<Button-5>", _on_mousewheel_linux_down)
            
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
        
        canvas.bind('<Enter>', _bind_mousewheel)
        canvas.bind('<Leave>', _unbind_mousewheel)
        
    # =================== RPC SECTIONS ===================
    
    def create_rpc_config_section(self, parent):
        """Section configuration RPC"""
        config_frame = self.create_card_frame(parent, "⚙️ Configuration RPC")
        
        tk.Label(config_frame, text="Application ID / Client ID", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(5, 2))
        
        client_frame = tk.Frame(config_frame, bg=self.colors['card'])
        client_frame.pack(fill='x', pady=(0, 5))
        
        self.client_id_entry = self.create_entry(client_frame, self.client_id_var)
        self.client_id_entry.pack(side='left', fill='x', expand=True)
        
        help_btn = tk.Button(client_frame, text="?", 
                           bg=self.colors['accent'], fg=self.colors['text'],
                           font=('Segoe UI', 8, 'bold'), relief='flat', width=3,
                           command=self.show_rpc_help)
        help_btn.pack(side='right', padx=(5, 0))
        
    def create_rpc_text_section(self, parent):
        """Section textes RPC"""
        text_frame = self.create_card_frame(parent, "📝 Textes du statut")
        
        tk.Label(text_frame, text="Détails (ligne du haut)", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(10, 2))
        self.create_entry(text_frame, self.details_var).pack(fill='x')
        
        tk.Label(text_frame, text="État (ligne du bas)", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(10, 2))
        self.create_entry(text_frame, self.state_var).pack(fill='x')
        
    def create_rpc_image_section(self, parent):
        """Section images RPC"""
        image_frame = self.create_card_frame(parent, "🖼️ Images")
        
        tk.Label(image_frame, text="Grande image (nom de l'asset)", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(10, 2))
        self.create_entry(image_frame, self.large_image_var).pack(fill='x')
        
        tk.Label(image_frame, text="Texte au survol (grande image)", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(5, 2))
        self.create_entry(image_frame, self.large_text_var).pack(fill='x')
        
        tk.Label(image_frame, text="Petite image (nom de l'asset)", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(10, 2))
        self.create_entry(image_frame, self.small_image_var).pack(fill='x')
        
        tk.Label(image_frame, text="Texte au survol (petite image)", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(5, 2))
        self.create_entry(image_frame, self.small_text_var).pack(fill='x')
        
    def create_rpc_options_section(self, parent):
        """Section options RPC"""
        options_frame = self.create_card_frame(parent, "⚙️ Options")
        
        time_check = tk.Checkbutton(options_frame, text="Afficher le temps écoulé",
                                  variable=self.show_time_var,
                                  bg=self.colors['card'], fg=self.colors['text'],
                                  selectcolor=self.colors['accent'],
                                  font=('Segoe UI', 10), relief='flat')
        time_check.pack(anchor='w', pady=(10, 0))
        
    def create_rpc_buttons(self, parent):
        """Boutons RPC"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill='x', padx=20, pady=20)
        
        self.rpc_connect_btn = tk.Button(button_frame, text="🔌 Connecter RPC",
                                       command=self.toggle_rpc_connection,
                                       bg=self.colors['success'], fg=self.colors['text'],
                                       font=('Segoe UI', 12, 'bold'), relief='flat', pady=10)
        self.rpc_connect_btn.pack(fill='x', pady=(0, 10))
        
    # =================== BOT SECTIONS ===================
    
    def create_bot_config_section(self, parent):
        """Section configuration Bot"""
        config_frame = self.create_card_frame(parent, "🔑 Configuration Bot")
        
        tk.Label(config_frame, text="Token du Bot Discord", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(5, 2))
        
        token_frame = tk.Frame(config_frame, bg=self.colors['card'])
        token_frame.pack(fill='x', pady=(0, 5))
        
        self.bot_token_entry = self.create_entry(token_frame, self.bot_token_var, show="*")
        self.bot_token_entry.pack(side='left', fill='x', expand=True)
        
        help_btn = tk.Button(token_frame, text="?", 
                           bg=self.colors['accent'], fg=self.colors['text'],
                           font=('Segoe UI', 8, 'bold'), relief='flat', width=3,
                           command=self.show_bot_help)
        help_btn.pack(side='right', padx=(5, 0))
        
    def create_bot_profile_section(self, parent):
        """Section profil Bot"""
        profile_frame = self.create_card_frame(parent, "👤 Profil du Bot")
        
        tk.Label(profile_frame, text="Nouveau nom du bot", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(10, 2))
        self.create_entry(profile_frame, self.bot_name_var).pack(fill='x')
        
        # Photo de profil
        pp_frame = tk.Frame(profile_frame, bg=self.colors['card'])
        pp_frame.pack(fill='x', pady=(15, 10))
        
        tk.Label(pp_frame, text="Photo de profil", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w')
        
        self.pp_btn = tk.Button(pp_frame, text="📷 Choisir une image",
                              command=self.select_profile_picture,
                              bg=self.colors['accent'], fg=self.colors['text'],
                              font=('Segoe UI', 10), relief='flat', pady=8)
        self.pp_btn.pack(fill='x', pady=(5, 0))
        
        self.selected_pp_path = None
        
    def create_bot_buttons(self, parent):
        """Boutons Bot"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill='x', padx=20, pady=20)
        
        name_btn = tk.Button(button_frame, text="📝 Changer le nom",
                           command=self.change_bot_name,
                           bg=self.colors['warning'], fg=self.colors['text'],
                           font=('Segoe UI', 11, 'bold'), relief='flat', pady=8)
        name_btn.pack(fill='x', pady=(0, 5))
        
        pp_update_btn = tk.Button(button_frame, text="🖼️ Changer la photo",
                                command=self.change_bot_avatar,
                                bg=self.colors['accent'], fg=self.colors['text'],
                                font=('Segoe UI', 11, 'bold'), relief='flat', pady=8)
        pp_update_btn.pack(fill='x', pady=5)
        
    # =================== ASSETS SECTIONS ===================
    
    def create_add_asset_section(self, parent):
        """Section ajout d'asset"""
        add_frame = self.create_card_frame(parent, "➕ Ajouter un Asset")
        
        tk.Label(add_frame, text="Nom de l'asset", 
                bg=self.colors['card'], fg=self.colors['text_muted'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(10, 2))
        
        self.asset_name_var = tk.StringVar()
        self.create_entry(add_frame, self.asset_name_var).pack(fill='x')
        
        # Bouton sélection image
        img_btn = tk.Button(add_frame, text="🖼️ Choisir l'image",
                          command=self.select_asset_image,
                          bg=self.colors['accent'], fg=self.colors['text'],
                          font=('Segoe UI', 10), relief='flat', pady=8)
        img_btn.pack(fill='x', pady=(15, 10))
        
        self.selected_asset_path = None
        self.asset_preview_label = tk.Label(add_frame, text="Aucune image sélectionnée",
                                          bg=self.colors['card'], fg=self.colors['text_muted'],
                                          font=('Segoe UI', 9))
        self.asset_preview_label.pack(pady=5)
        
        # Bouton ajout
        add_btn = tk.Button(add_frame, text="✅ Ajouter l'Asset",
                          command=self.add_asset,
                          bg=self.colors['success'], fg=self.colors['text'],
                          font=('Segoe UI', 11, 'bold'), relief='flat', pady=10)
        add_btn.pack(fill='x', pady=(10, 0))
        
    def create_assets_list_section(self, parent):
        """Section liste des assets"""
        list_frame = self.create_card_frame(parent, "📋 Assets Disponibles")
        
        # Frame pour la liste avec scrollbar
        list_container = tk.Frame(list_frame, bg=self.colors['card'])
        list_container.pack(fill='both', expand=True, pady=10)
        
        # Listbox avec scrollbar
        scrollbar_assets = ttk.Scrollbar(list_container)
        scrollbar_assets.pack(side='right', fill='y')
        
        self.assets_listbox = tk.Listbox(list_container,
                                       yscrollcommand=scrollbar_assets.set,
                                       bg='#40444B', fg=self.colors['text'],
                                       font=('Segoe UI', 10),
                                       selectbackground=self.colors['accent'],
                                       relief='flat', bd=0, height=8)
        self.assets_listbox.pack(side='left', fill='both', expand=True)
        scrollbar_assets.config(command=self.assets_listbox.yview)
        
        # Boutons pour assets
        btn_frame = tk.Frame(list_frame, bg=self.colors['card'])
        btn_frame.pack(fill='x', pady=(10, 0))
        
        refresh_btn = tk.Button(btn_frame, text="🔄 Actualiser",
                              command=self.load_assets,
                              bg=self.colors['accent'], fg=self.colors['text'],
                              font=('Segoe UI', 9), relief='flat', pady=5)
        refresh_btn.pack(side='left', fill='x', expand=True, padx=(0, 2))
        
        delete_btn = tk.Button(btn_frame, text="🗑️ Supprimer",
                             command=self.delete_asset,
                             bg=self.colors['danger'], fg=self.colors['text'],
                             font=('Segoe UI', 9), relief='flat', pady=5)
        delete_btn.pack(side='right', fill='x', expand=True, padx=(2, 0))
        
    # =================== HELPER METHODS ===================
    
    def create_card_frame(self, parent, title):
        """Crée un frame avec style carte"""
        outer_frame = tk.Frame(parent, bg=self.colors['bg'])
        outer_frame.pack(fill='x', padx=20, pady=5)
        
        card_frame = tk.Frame(outer_frame, bg=self.colors['card'], relief='flat', bd=1)
        card_frame.pack(fill='x')
        
        inner_frame = tk.Frame(card_frame, bg=self.colors['card'])
        inner_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(inner_frame, text=title, 
                bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        return inner_frame
        
    def create_entry(self, parent, variable, show=None):
        """Crée un entry avec style"""
        entry = tk.Entry(parent, textvariable=variable,
                        font=('Segoe UI', 10), bg='#40444B', fg=self.colors['text'],
                        insertbackground=self.colors['text'], relief='flat', bd=8)
        if show:
            entry.configure(show=show)
        return entry
        
    # =================== RPC METHODS ===================
    
    def toggle_rpc_connection(self):
        """Bascule la connexion RPC"""
        if not self.rpc_connected:
            self.connect_rpc()
        else:
            self.disconnect_rpc()
            
    def connect_rpc(self):
        """Connexion RPC"""
        client_id = self.client_id_var.get().strip()
        if not client_id:
            messagebox.showerror("Erreur", "Veuillez entrer votre Client ID!")
            return
            
        try:
            self.rpc = Presence(client_id)
            self.rpc.connect()
            self.rpc_connected = True
            
            self.rpc_status_var.set("✅ RPC Connecté")
            self.rpc_status_label.configure(fg=self.colors['success'])
            self.rpc_connect_btn.configure(text="🔌 Déconnecter RPC", bg=self.colors['danger'])
            
            self.start_rpc_auto_update()
            messagebox.showinfo("Succès", "RPC connecté avec succès!")
            
        except Exception as e:
            messagebox.showerror("Erreur RPC", f"Impossible de se connecter:\n{str(e)}")
            
    def disconnect_rpc(self):
        """Déconnexion RPC"""
        if self.rpc:
            try:
                self.rpc.close()
            except:
                pass
                
        self.rpc_connected = False
        self.rpc = None
        
        self.rpc_status_var.set("❌ RPC Déconnecté")
        self.rpc_status_label.configure(fg=self.colors['danger'])
        self.rpc_connect_btn.configure(text="🔌 Connecter RPC", bg=self.colors['success'])
        
    def start_rpc_auto_update(self):
        """Démarre la mise à jour automatique RPC"""
        if self.update_thread and self.update_thread.is_alive():
            return
            
        self.update_thread = threading.Thread(target=self.rpc_auto_update_loop, daemon=True)
        self.update_thread.start()
        
    def rpc_auto_update_loop(self):
        """Boucle de mise à jour automatique RPC"""
        while self.rpc_connected and self.rpc:
            try:
                self.update_rpc_presence()
                time.sleep(15)
            except:
                break
                
    def update_rpc_presence(self):
        """Met à jour la Rich Presence"""
        if not self.rpc_connected or not self.rpc:
            return
            
        try:
            presence_data = {}
            
            if self.details_var.get().strip():
                presence_data['details'] = self.details_var.get().strip()
                
            if self.state_var.get().strip():
                presence_data['state'] = self.state_var.get().strip()
                
            if self.large_image_var.get().strip():
                presence_data['large_image'] = self.large_image_var.get().strip()
                
            if self.large_text_var.get().strip():
                presence_data['large_text'] = self.large_text_var.get().strip()
                
            if self.small_image_var.get().strip():
                presence_data['small_image'] = self.small_image_var.get().strip()
                
            if self.small_text_var.get().strip():
                presence_data['small_text'] = self.small_text_var.get().strip()
                
            if self.show_time_var.get():
                presence_data['start'] = int(time.time())
                
            self.rpc.update(**presence_data)
            
        except Exception as e:
            print(f"Erreur mise à jour RPC: {e}")
    
    def show_rpc_help(self):
        """Affiche l'aide RPC"""
        help_text = """Pour obtenir votre Client ID Discord :

1. Allez sur https://discord.com/developers/applications
2. Cliquez sur "New Application"
3. Donnez un nom à votre application
4. Copiez l'Application ID dans "General Information"
5. Collez-le dans le champ Client ID

Pour les images, utilisez l'onglet Assets Manager !"""
        
        messagebox.showinfo("Aide - Client ID Discord", help_text)
        
    # =================== BOT METHODS ===================
    
    def show_bot_help(self):
        """Affiche l'aide Bot"""
        help_text = """Pour obtenir le token de votre bot :

1. Allez sur https://discord.com/developers/applications
2. Sélectionnez votre application (ou créez-en une)
3. Allez dans l'onglet "Bot"
4. Cliquez sur "Reset Token" puis "Copy"
5. Collez-le dans le champ Token

⚠️ ATTENTION : Ne partagez JAMAIS votre token !"""
        
        messagebox.showinfo("Aide - Token Bot Discord", help_text)
        
    def get_bot_headers(self):
        """Retourne les headers pour l'API Discord"""
        token = self.bot_token_var.get().strip()
        if not token:
            return None
        return {
            'Authorization': f'Bot {token}',
            'Content-Type': 'application/json'
        }
    
    def get_application_id(self):
        """Récupère l'ID de l'application"""
        headers = self.get_bot_headers()
        if not headers:
            return None
            
        try:
            response = self.bot_session.get('https://discord.com/api/v10/oauth2/applications/@me', 
                                          headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.application_id = data['id']
                self.bot_status_var.set("✅ Bot Connecté")
                self.bot_status_label.configure(fg=self.colors['success'])
                return data['id']
            else:
                self.bot_status_var.set("❌ Token Invalide")
                self.bot_status_label.configure(fg=self.colors['danger'])
                return None
        except Exception as e:
            self.bot_status_var.set("❌ Erreur Connexion")
            self.bot_status_label.configure(fg=self.colors['danger'])
            return None
    
    def change_bot_name(self):
        """Change le nom du bot"""
        new_name = self.bot_name_var.get().strip()
        if not new_name:
            messagebox.showerror("Erreur", "Veuillez entrer un nom!")
            return
            
        app_id = self.get_application_id()
        if not app_id:
            messagebox.showerror("Erreur", "Token invalide ou connexion échouée!")
            return
            
        headers = self.get_bot_headers()
        data = {'name': new_name}
        
        try:
            response = self.bot_session.patch(f'https://discord.com/api/v10/applications/{app_id}',
                                            headers=headers, json=data)
            if response.status_code == 200:
                messagebox.showinfo("Succès", f"Nom changé en '{new_name}' avec succès!")
            else:
                error_data = response.json()
                messagebox.showerror("Erreur", f"Erreur: {error_data.get('message', 'Erreur inconnue')}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du changement de nom:\n{str(e)}")
    
    def select_profile_picture(self):
        """Sélectionne une photo de profil"""
        filename = filedialog.askopenfilename(
            title="Choisir une photo de profil",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            # Vérifier la taille du fichier (max 8MB pour Discord)
            if os.path.getsize(filename) > 8 * 1024 * 1024:
                messagebox.showerror("Erreur", "L'image est trop grande! Maximum 8MB.")
                return
                
            self.selected_pp_path = filename
            self.pp_btn.configure(text=f"📷 {os.path.basename(filename)}")
    
    def change_bot_avatar(self):
        """Change l'avatar du bot"""
        if not self.selected_pp_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner une image!")
            return
            
        app_id = self.get_application_id()
        if not app_id:
            messagebox.showerror("Erreur", "Token invalide ou connexion échouée!")
            return
            
        try:
            # Lire et encoder l'image
            with open(self.selected_pp_path, 'rb') as f:
                image_data = f.read()
            
            # Déterminer le type MIME
            ext = os.path.splitext(self.selected_pp_path)[1].lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(ext, 'image/png')
            
            # Encoder en base64
            b64_image = base64.b64encode(image_data).decode('utf-8')
            avatar_data = f"data:{mime_type};base64,{b64_image}"
            
            headers = self.get_bot_headers()
            data = {'icon': avatar_data}
            
            response = self.bot_session.patch(f'https://discord.com/api/v10/applications/{app_id}',
                                            headers=headers, json=data)
            
            if response.status_code == 200:
                messagebox.showinfo("Succès", "Avatar changé avec succès!")
                self.pp_btn.configure(text="📷 Choisir une image")
                self.selected_pp_path = None
            else:
                error_data = response.json()
                messagebox.showerror("Erreur", f"Erreur: {error_data.get('message', 'Erreur inconnue')}")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du changement d'avatar:\n{str(e)}")
    
    # =================== ASSETS METHODS ===================
    
    def select_asset_image(self):
        """Sélectionne une image pour asset"""
        filename = filedialog.askopenfilename(
            title="Choisir une image pour l'asset",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            # Vérifier la taille (max 8MB)
            if os.path.getsize(filename) > 8 * 1024 * 1024:
                messagebox.showerror("Erreur", "L'image est trop grande! Maximum 8MB.")
                return
                
            self.selected_asset_path = filename
            self.asset_preview_label.configure(text=f"📷 {os.path.basename(filename)}")
    
    def add_asset(self):
        """Ajoute un asset via l'API Discord Developer Portal"""
        asset_name = self.asset_name_var.get().strip()
        if not asset_name:
            messagebox.showerror("Erreur", "Veuillez entrer un nom pour l'asset!")
            return
            
        if not self.selected_asset_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner une image!")
            return
        
        # Vérifier que l'application ID est disponible
        app_id = self.application_id or self.client_id_var.get().strip()
        if not app_id:
            messagebox.showerror("Erreur", "Veuillez d'abord vous connecter avec un token bot ou entrer un Client ID!")
            return
            
        try:
            # Pour les Rich Presence Assets, on utilise une approche différente
            # Car Discord ne permet plus l'ajout d'assets via l'API publique
            
            # Solution alternative : sauvegarder localement et informer l'utilisateur
            local_assets_file = 'local_assets.json'
            local_assets = []
            
            # Charger les assets locaux existants
            if os.path.exists(local_assets_file):
                try:
                    with open(local_assets_file, 'r', encoding='utf-8') as f:
                        local_assets = json.load(f)
                except:
                    local_assets = []
            
            # Copier l'image dans un dossier local
            assets_dir = 'assets'
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir)
            
            # Générer un nom de fichier unique
            import uuid
            ext = os.path.splitext(self.selected_asset_path)[1]
            unique_filename = f"{asset_name}_{str(uuid.uuid4())[:8]}{ext}"
            local_path = os.path.join(assets_dir, unique_filename)
            
            # Copier le fichier
            import shutil
            shutil.copy2(self.selected_asset_path, local_path)
            
            # Ajouter à la liste locale
            asset_info = {
                'id': str(uuid.uuid4()),
                'name': asset_name,
                'local_path': local_path,
                'original_path': self.selected_asset_path,
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            local_assets.append(asset_info)
            
            # Sauvegarder
            with open(local_assets_file, 'w', encoding='utf-8') as f:
                json.dump(local_assets, f, indent=4, ensure_ascii=False)
            
            # Message d'information
            messagebox.showinfo("Asset ajouté localement", 
                              f"Asset '{asset_name}' sauvegardé localement!\n\n"
                              f"⚠️ Note : Pour utiliser cet asset dans Discord :\n"
                              f"1. Allez sur https://discord.com/developers/applications\n"
                              f"2. Sélectionnez votre application\n"
                              f"3. Allez dans 'Rich Presence' > 'Art Assets'\n"
                              f"4. Uploadez manuellement votre image\n"
                              f"5. Utilisez le nom '{asset_name}' dans votre RPC\n\n"
                              f"L'image a été copiée dans le dossier 'assets/'")
            
            # Réinitialiser les champs
            self.asset_name_var.set("")
            self.selected_asset_path = None
            self.asset_preview_label.configure(text="Aucune image sélectionnée")
            self.load_assets()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'asset:\n{str(e)}")
    
    def load_assets(self):
        """Charge la liste des assets (locaux et Discord si possible)"""
        # Vider la listbox
        self.assets_listbox.delete(0, tk.END)
        
        # Charger les assets locaux
        local_assets_file = 'local_assets.json'
        if os.path.exists(local_assets_file):
            try:
                with open(local_assets_file, 'r', encoding='utf-8') as f:
                    local_assets = json.load(f)
                
                for asset in local_assets:
                    self.assets_listbox.insert(tk.END, f"📁 {asset['name']} (Local)")
                    
            except Exception as e:
                print(f"Erreur chargement assets locaux: {e}")
        
        # Essayer de charger les assets Discord (si token bot disponible)
        app_id = self.application_id or self.client_id_var.get().strip()
        headers = self.get_bot_headers()
        
        if app_id and headers:
            try:
                # Utiliser l'endpoint correct pour les applications
                response = self.bot_session.get(f'https://discord.com/api/v10/applications/{app_id}',
                                              headers=headers)
                
                if response.status_code == 200:
                    app_data = response.json()
                    # Discord ne retourne plus les assets via cette API
                    # On affiche juste l'info de l'application
                    self.assets_listbox.insert(0, f"🤖 Application: {app_data.get('name', 'Unknown')}")
                
            except Exception as e:
                print(f"Erreur chargement assets Discord: {e}")
        
        # Si aucun asset, afficher un message d'aide
        if self.assets_listbox.size() == 0:
            self.assets_listbox.insert(tk.END, "Aucun asset trouvé - Ajoutez-en un!")
    
    def delete_asset(self):
        """Supprime un asset sélectionné (local uniquement)"""
        selection = self.assets_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un asset à supprimer!")
            return
            
        selected_text = self.assets_listbox.get(selection[0])
        
        # Vérifier si c'est un asset local
        if not selected_text.startswith("📁"):
            messagebox.showinfo("Info", "Seuls les assets locaux peuvent être supprimés depuis cette application.\n"
                                      "Pour supprimer des assets Discord, utilisez le Developer Portal.")
            return
        
        # Extraire le nom de l'asset
        asset_name = selected_text.replace("📁 ", "").replace(" (Local)", "")
        
        # Confirmation
        result = messagebox.askyesno("Confirmation", 
                                   f"Voulez-vous vraiment supprimer l'asset local '{asset_name}'?")
        if not result:
            return
        
        try:
            # Charger les assets locaux
            local_assets_file = 'local_assets.json'
            if os.path.exists(local_assets_file):
                with open(local_assets_file, 'r', encoding='utf-8') as f:
                    local_assets = json.load(f)
                
                # Trouver et supprimer l'asset
                for i, asset in enumerate(local_assets):
                    if asset['name'] == asset_name:
                        # Supprimer le fichier local
                        if os.path.exists(asset['local_path']):
                            os.remove(asset['local_path'])
                        
                        # Supprimer de la liste
                        local_assets.pop(i)
                        break
                
                # Sauvegarder
                with open(local_assets_file, 'w', encoding='utf-8') as f:
                    json.dump(local_assets, f, indent=4, ensure_ascii=False)
                
                messagebox.showinfo("Succès", f"Asset local '{asset_name}' supprimé avec succès!")
                self.load_assets()
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression:\n{str(e)}")
    
    # =================== CONFIG METHODS ===================
    
    def load_config(self):
        """Charge la configuration"""
        config_file = 'advanced_rpc_config.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # RPC Config
                self.client_id_var.set(config.get('client_id', ''))
                self.details_var.set(config.get('details', ''))
                self.state_var.set(config.get('state', ''))
                self.large_image_var.set(config.get('large_image', ''))
                self.large_text_var.set(config.get('large_text', ''))
                self.small_image_var.set(config.get('small_image', ''))
                self.small_text_var.set(config.get('small_text', ''))
                self.show_time_var.set(config.get('show_time', False))
                
                # Bot Config (ne pas charger le token pour sécurité)
                self.bot_name_var.set(config.get('bot_name', ''))
                
            except Exception as e:
                print(f"Erreur chargement config: {e}")
    
    def save_config(self):
        """Sauvegarde la configuration"""
        config = {
            # RPC Config
            'client_id': self.client_id_var.get(),
            'details': self.details_var.get(),
            'state': self.state_var.get(),
            'large_image': self.large_image_var.get(),
            'large_text': self.large_text_var.get(),
            'small_image': self.small_image_var.get(),
            'small_text': self.small_text_var.get(),
            'show_time': self.show_time_var.get(),
            
            # Bot Config (ne pas sauvegarder le token pour sécurité)
            'bot_name': self.bot_name_var.get(),
        }
        
        try:
            with open('advanced_rpc_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde config: {e}")
    
    def on_closing(self):
        """Gestionnaire de fermeture"""
        self.save_config()
        if self.rpc_connected:
            self.disconnect_rpc()
        self.root.destroy()

def main():
    """Fonction principale"""
    # Vérifier les dépendances
    try:
        import pypresence
        import requests
        from PIL import Image, ImageTk
    except ImportError as e:
        import tkinter.messagebox as mb
        root = tk.Tk()
        root.withdraw()
        missing_module = str(e).split("'")[1]
        mb.showerror("Module manquant", 
                    f"Le module '{missing_module}' n'est pas installé.\n\n"
                    f"Installez les dépendances avec:\n"
                    f"pip install pypresence requests pillow")
        return
    
    root = tk.Tk()
    app = DiscordAdvancedManager(root)
    
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
