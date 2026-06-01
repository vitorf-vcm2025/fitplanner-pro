import json
from pathlib import Path

import customtkinter as ctk


WORKOUTS_FILE = Path(__file__).parent / "data" / "treinos.json"
DEFAULT_WORKOUTS = [
    {
        "nome": "Treino A - Peito e Triceps",
        "foco": "Forca e hipertrofia",
        "duracao": "55 min",
        "exercicios": ["Supino reto", "Supino inclinado", "Crucifixo", "Triceps corda"],
    },
    {
        "nome": "Treino B - Costas e Biceps",
        "foco": "Puxada e estabilidade",
        "duracao": "60 min",
        "exercicios": ["Puxada alta", "Remada baixa", "Remada curvada", "Rosca direta"],
    },
    {
        "nome": "Treino C - Pernas",
        "foco": "Base, potencia e resistencia",
        "duracao": "65 min",
        "exercicios": ["Agachamento", "Leg press", "Cadeira extensora", "Mesa flexora"],
    },
]


class FitPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("FitPlanner PRO")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.active_screen = "Dashboard"
        self.menu_buttons = {}
        self.new_workout_window = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_content()
        self._show_screen(self.active_screen)

    def _create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=("#111827", "#0B1220"))
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(8, weight=1)
        sidebar.grid_propagate(False)

        logo = ctk.CTkLabel(
            sidebar,
            text="FitPlanner\nPRO",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#38BDF8",
            justify="left",
        )
        logo.grid(row=0, column=0, padx=26, pady=(32, 22), sticky="w")

        subtitle = ctk.CTkLabel(
            sidebar,
            text="Planejamento fitness",
            font=ctk.CTkFont(size=13),
            text_color="#94A3B8",
        )
        subtitle.grid(row=1, column=0, padx=26, pady=(0, 26), sticky="w")

        menu_items = [
            "Dashboard",
            "Treinos",
            "Dieta",
            "Progresso",
            "Agenda",
            "Configurações",
        ]

        for index, item in enumerate(menu_items, start=2):
            button = ctk.CTkButton(
                sidebar,
                text=item,
                height=44,
                anchor="w",
                corner_radius=12,
                fg_color="#1D4ED8" if item == "Dashboard" else "transparent",
                hover_color="#2563EB",
                text_color="#F8FAFC",
                font=ctk.CTkFont(size=15, weight="bold" if item == "Dashboard" else "normal"),
                command=lambda screen=item: self._show_screen(screen) if screen in ("Dashboard", "Treinos", "Dieta", "Progresso", "Agenda", "Configurações") else None,
            )
            button.grid(row=index, column=0, padx=18, pady=6, sticky="ew")
            self.menu_buttons[item] = button

        profile = ctk.CTkFrame(sidebar, corner_radius=18, fg_color="#111C2F")
        profile.grid(row=9, column=0, padx=18, pady=24, sticky="ew")

        ctk.CTkLabel(
            profile,
            text="Plano atual",
            font=ctk.CTkFont(size=12),
            text_color="#94A3B8",
        ).pack(anchor="w", padx=18, pady=(16, 2))

        ctk.CTkLabel(
            profile,
            text="Performance",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F8FAFC",
        ).pack(anchor="w", padx=18, pady=(0, 16))

    def _create_content(self):
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="#0F172A")
        self.content.grid(row=0, column=1, sticky="nsew")

    def _show_screen(self, screen):
        self.active_screen = screen

        for item, button in self.menu_buttons.items():
            is_active = item == screen
            button.configure(
                fg_color="#1D4ED8" if is_active else "transparent",
                font=ctk.CTkFont(size=15, weight="bold" if is_active else "normal"),
            )

        for widget in self.content.winfo_children():
            widget.destroy()

        if screen == "Dashboard":
            self._create_dashboard_screen()
        elif screen == "Treinos":
            self._create_workouts_screen()
        elif screen == "Dieta":
            self._create_diet_screen()
        elif screen == "Progresso":
            self._create_progress_screen()
        elif screen in ("Agenda", "Configurações"):
            self._create_coming_soon_screen(screen)

    def _load_workouts(self):
        if not WORKOUTS_FILE.exists():
            WORKOUTS_FILE.parent.mkdir(parents=True, exist_ok=True)
            WORKOUTS_FILE.write_text(json.dumps(DEFAULT_WORKOUTS, indent=4), encoding="utf-8")

        with WORKOUTS_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_workout(self, workout):
        workouts = self._load_workouts()
        if not isinstance(workouts, list):
            workouts = []

        workouts.append(workout)
        WORKOUTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        WORKOUTS_FILE.write_text(json.dumps(workouts, indent=4, ensure_ascii=False), encoding="utf-8")

    def _open_new_workout_popup(self):
        if self.new_workout_window is not None and self.new_workout_window.winfo_exists():
            self.new_workout_window.focus()
            return

        window = ctk.CTkToplevel(self)
        window.title("Novo treino")
        window.geometry("560x720")
        window.minsize(500, 680)
        window.configure(fg_color="#0F172A")
        window.transient(self)
        window.grab_set()
        self.new_workout_window = window

        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)

        form = ctk.CTkFrame(window, corner_radius=26, fg_color="#111C2F")
        form.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            form,
            text="Cadastrar novo treino",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#F8FAFC",
        ).grid(row=0, column=0, padx=24, pady=(24, 6), sticky="w")

        ctk.CTkLabel(
            form,
            text="Preencha os dados para adicionar um treino ao plano.",
            font=ctk.CTkFont(size=14),
            text_color="#94A3B8",
        ).grid(row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        name_entry = self._create_form_entry(form, 2, "Nome do treino", "Ex: Treino A - Peito e Triceps")
        objective_entry = self._create_form_entry(form, 4, "Objetivo", "Ex: Forca e hipertrofia")
        duration_entry = self._create_form_entry(form, 6, "Duracao (min)", "Ex: 55")

        ctk.CTkLabel(
            form,
            text="Exercicios",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#CBD5E1",
        ).grid(row=8, column=0, padx=24, pady=(12, 6), sticky="w")

        exercises_text = ctk.CTkTextbox(
            form,
            height=120,
            corner_radius=14,
            fg_color="#172033",
            border_width=1,
            border_color="#1E293B",
            text_color="#F8FAFC",
        )
        exercises_text.grid(row=9, column=0, padx=24, sticky="ew")

        ctk.CTkButton(
            form,
            text="Salvar Treino",
            height=48,
            corner_radius=16,
            fg_color="#0EA5E9",
            hover_color="#0284C7",
            text_color="#F8FAFC",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: self._handle_save_workout(
                window,
                feedback,
                name_entry,
                objective_entry,
                duration_entry,
                exercises_text,
            ),
        ).grid(row=10, column=0, padx=24, pady=(18, 0), sticky="ew")

        feedback = ctk.CTkLabel(
            form,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#F87171",
        )
        feedback.grid(row=11, column=0, padx=24, pady=(12, 0), sticky="w")

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=12, column=0, padx=24, pady=24, sticky="ew")
        actions.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            actions,
            text="Cancelar",
            width=120,
            height=42,
            corner_radius=14,
            fg_color="#1E293B",
            hover_color="#334155",
            command=window.destroy,
        ).grid(row=0, column=1, sticky="e")

        name_entry.focus()

    def _create_form_entry(self, parent, row, label, placeholder):
        ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#CBD5E1",
        ).grid(row=row, column=0, padx=24, pady=(12, 6), sticky="w")

        entry = ctk.CTkEntry(
            parent,
            height=42,
            corner_radius=14,
            fg_color="#172033",
            border_color="#1E293B",
            text_color="#F8FAFC",
            placeholder_text=placeholder,
        )
        entry.grid(row=row + 1, column=0, padx=24, sticky="ew")
        return entry

    def _handle_save_workout(self, window, feedback, name_entry, objective_entry, duration_entry, exercises_text):
        name = name_entry.get().strip()
        objective = objective_entry.get().strip()
        duration = duration_entry.get().strip()
        raw_exercises = exercises_text.get("1.0", "end").strip()

        if not name:
            feedback.configure(text="Informe o nome do treino.")
            return

        exercises = [
            exercise.strip()
            for exercise in raw_exercises.replace(";", "\n").replace(",", "\n").splitlines()
            if exercise.strip()
        ]

        workout = {
            "nome": name,
            "foco": objective or "Objetivo nao informado",
            "duracao": duration if duration.lower().endswith("min") else f"{duration} min" if duration else "Duracao nao informada",
            "exercicios": exercises,
        }

        self._save_workout(workout)
        window.destroy()
        self._show_screen("Treinos")

    def _create_dashboard_screen(self):
        content = self.content
        content.grid_columnconfigure((0, 1, 2), weight=1)
        content.grid_rowconfigure((0, 1, 2), weight=0)
        content.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, padx=32, pady=(32, 12), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Dashboard",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color="#F8FAFC",
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Organize treinos, dieta e progresso em um so lugar.",
            font=ctk.CTkFont(size=15),
            text_color="#94A3B8",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(6, 0))

        new_plan_button = ctk.CTkButton(
            header,
            text="+ Novo plano",
            width=150,
            height=42,
            corner_radius=14,
            fg_color="#0EA5E9",
            hover_color="#0284C7",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._open_new_workout_popup,
        )
        new_plan_button.grid(row=0, column=1, rowspan=2, padx=(16, 0), sticky="e")

        cards = [
            ("Treinos na semana", "05", "Meta: 6 sessoes", "#38BDF8"),
            ("Calorias hoje", "2.180", "Restam 320 kcal", "#22C55E"),
            ("Evolucao mensal", "+12%", "Consistencia em alta", "#A855F7"),
        ]

        for column, (label, value, detail, color) in enumerate(cards):
            self._create_stat_card(content, column, label, value, detail, color)

        plan_panel = ctk.CTkFrame(content, corner_radius=24, fg_color="#111C2F")
        plan_panel.grid(row=2, column=0, columnspan=2, padx=(32, 12), pady=20, sticky="nsew")
        plan_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            plan_panel,
            text="Plano de hoje",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F8FAFC",
        ).grid(row=0, column=0, padx=24, pady=(24, 12), sticky="w")

        workout_items = [
            ("Aquecimento", "10 min de mobilidade e cardio leve"),
            ("Forca", "Peito, ombros e triceps"),
            ("Cardio", "20 min em zona moderada"),
        ]

        for row, (title, description) in enumerate(workout_items, start=1):
            item = ctk.CTkFrame(plan_panel, corner_radius=16, fg_color="#172033")
            item.grid(row=row, column=0, padx=24, pady=8, sticky="ew")
            item.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                item,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#F8FAFC",
            ).grid(row=0, column=0, padx=18, pady=(14, 2), sticky="w")

            ctk.CTkLabel(
                item,
                text=description,
                font=ctk.CTkFont(size=13),
                text_color="#94A3B8",
            ).grid(row=1, column=0, padx=18, pady=(0, 14), sticky="w")

        progress_panel = ctk.CTkFrame(content, corner_radius=24, fg_color="#111C2F")
        progress_panel.grid(row=2, column=2, padx=(12, 32), pady=20, sticky="nsew")

        ctk.CTkLabel(
            progress_panel,
            text="Consistencia",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F8FAFC",
        ).pack(anchor="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            progress_panel,
            text="78%",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#38BDF8",
        ).pack(anchor="w", padx=24, pady=(8, 0))

        progress = ctk.CTkProgressBar(progress_panel, height=12, corner_radius=8, progress_color="#38BDF8")
        progress.pack(fill="x", padx=24, pady=18)
        progress.set(0.78)

        ctk.CTkLabel(
            progress_panel,
            text="Continue seguindo o plano para bater sua meta semanal.",
            wraplength=230,
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color="#CBD5E1",
        ).pack(anchor="w", padx=24, pady=(0, 24))

    def _create_simple_screen(self, screen):
        descriptions = {
            "Treinos": "Monte, acompanhe e ajuste suas sessoes de treino.",
            "Dieta": "Organize refeicoes, calorias e metas nutricionais.",
        }

        accent_colors = {
            "Treinos": "#38BDF8",
            "Dieta": "#22C55E",
        }

        content = self.content
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure((1, 2), weight=0)
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure((1, 2, 3), weight=0)

        panel = ctk.CTkFrame(content, corner_radius=28, fg_color="#111C2F")
        panel.grid(row=0, column=0, padx=32, pady=32, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            panel,
            text=screen,
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#F8FAFC",
        ).grid(row=0, column=0, padx=34, pady=(34, 8), sticky="w")

        ctk.CTkLabel(
            panel,
            text=descriptions[screen],
            font=ctk.CTkFont(size=16),
            text_color="#94A3B8",
        ).grid(row=1, column=0, padx=34, sticky="w")

        highlight = ctk.CTkFrame(panel, corner_radius=22, fg_color="#172033")
        highlight.grid(row=2, column=0, padx=34, pady=34, sticky="ew")
        highlight.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            highlight,
            text=f"Voce esta na tela de {screen}",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=accent_colors[screen],
        ).grid(row=0, column=0, padx=24, pady=(24, 6), sticky="w")

        ctk.CTkLabel(
            highlight,
            text="Em breve este espaco recebera os recursos completos desta area.",
            font=ctk.CTkFont(size=14),
            text_color="#CBD5E1",
        ).grid(row=1, column=0, padx=24, pady=(0, 24), sticky="w")

    def _create_diet_screen(self):
        meals = [
            ("Caf\u00e9 da Manh\u00e3 - 3 Ovos + Aveia", "07:30", "480 kcal", "Proteina alta", "#F59E0B"),
            ("Almoco - Frango + Arroz + Salada", "12:30", "720 kcal", "Refeicao principal", "#22C55E"),
            ("Lanche - Iogurte + Banana", "16:00", "310 kcal", "Energia pre-treino", "#38BDF8"),
            ("Jantar - Peixe + Batata Doce", "20:00", "590 kcal", "Recuperacao muscular", "#A855F7"),
        ]

        content = self.content
        content.grid_columnconfigure((0, 1, 2), weight=1)
        content.grid_rowconfigure((0, 1, 2), weight=0)
        content.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, padx=32, pady=(32, 12), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Dieta",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color="#F8FAFC",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Rotina alimentar premium com metas diarias simuladas.",
            font=ctk.CTkFont(size=15),
            text_color="#94A3B8",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        stats = [
            ("Calorias", "2.100", "Meta: 2.500 kcal", "#22C55E"),
            ("Proteinas", "156g", "Foco em massa magra", "#38BDF8"),
            ("Agua", "2.4L", "Meta: 3.0L", "#A855F7"),
        ]

        for column, (label, value, detail, color) in enumerate(stats):
            self._create_stat_card(content, column, label, value, detail, color)

        meals_panel = ctk.CTkFrame(content, corner_radius=26, fg_color="#111C2F")
        meals_panel.grid(row=2, column=0, columnspan=3, padx=32, pady=20, sticky="nsew")
        meals_panel.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            meals_panel,
            text="Plano alimentar de hoje",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#F8FAFC",
        ).grid(row=0, column=0, columnspan=2, padx=26, pady=(26, 12), sticky="w")

        for index, (name, time, calories, tag, color) in enumerate(meals, start=1):
            card = ctk.CTkFrame(meals_panel, corner_radius=20, fg_color="#172033")
            card.grid(row=((index - 1) // 2) + 1, column=(index - 1) % 2, padx=14, pady=14, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                card,
                text=time,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=color,
            ).grid(row=0, column=0, padx=22, pady=(20, 4), sticky="w")

            ctk.CTkLabel(
                card,
                text=name,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#F8FAFC",
                wraplength=340,
                justify="left",
            ).grid(row=1, column=0, padx=22, sticky="w")

            ctk.CTkLabel(
                card,
                text=f"{calories} - {tag}",
                font=ctk.CTkFont(size=14),
                text_color="#CBD5E1",
            ).grid(row=2, column=0, padx=22, pady=(10, 20), sticky="w")

    def _create_progress_screen(self):
        history = [
            ("28/05/2026", "78.4 kg", "18.5%", "Medidas atuais"),
            ("14/05/2026", "79.1 kg", "19.2%", "Melhora de definicao"),
            ("30/04/2026", "80.0 kg", "20.1%", "Inicio do ciclo"),
        ]

        content = self.content
        content.grid_columnconfigure((0, 1, 2), weight=1)
        content.grid_rowconfigure((0, 1, 2), weight=0)
        content.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, padx=32, pady=(32, 12), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Progresso",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color="#F8FAFC",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Historico de avaliacao fisica com indicadores principais.",
            font=ctk.CTkFont(size=15),
            text_color="#94A3B8",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        stats = [
            ("Peso atual", "78.4 kg", "-1.6 kg no mes", "#38BDF8"),
            ("Gordura corporal", "18.5%", "Meta: 15%", "#22C55E"),
            ("Massa magra", "63.9 kg", "Estimativa atual", "#A855F7"),
        ]

        for column, (label, value, detail, color) in enumerate(stats):
            self._create_stat_card(content, column, label, value, detail, color)

        history_panel = ctk.CTkFrame(content, corner_radius=26, fg_color="#111C2F")
        history_panel.grid(row=2, column=0, columnspan=2, padx=(32, 12), pady=20, sticky="nsew")
        history_panel.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            history_panel,
            text="Avaliacoes recentes",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#F8FAFC",
        ).grid(row=0, column=0, columnspan=3, padx=26, pady=(26, 14), sticky="w")

        for row, (date, weight, fat, note) in enumerate(history, start=1):
            item = ctk.CTkFrame(history_panel, corner_radius=18, fg_color="#172033")
            item.grid(row=row, column=0, columnspan=3, padx=26, pady=8, sticky="ew")
            item.grid_columnconfigure((0, 1, 2), weight=1)

            ctk.CTkLabel(item, text=date, font=ctk.CTkFont(size=14, weight="bold"), text_color="#F8FAFC").grid(row=0, column=0, padx=18, pady=(16, 2), sticky="w")
            ctk.CTkLabel(item, text=f"Peso: {weight}", font=ctk.CTkFont(size=14), text_color="#38BDF8").grid(row=0, column=1, padx=18, pady=(16, 2), sticky="w")
            ctk.CTkLabel(item, text=f"Gordura: {fat}", font=ctk.CTkFont(size=14), text_color="#22C55E").grid(row=0, column=2, padx=18, pady=(16, 2), sticky="w")
            ctk.CTkLabel(item, text=note, font=ctk.CTkFont(size=13), text_color="#94A3B8").grid(row=1, column=0, columnspan=3, padx=18, pady=(0, 16), sticky="w")

        goal_panel = ctk.CTkFrame(content, corner_radius=26, fg_color="#111C2F")
        goal_panel.grid(row=2, column=2, padx=(12, 32), pady=20, sticky="nsew")

        ctk.CTkLabel(
            goal_panel,
            text="Meta atual",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F8FAFC",
        ).pack(anchor="w", padx=24, pady=(26, 8))

        ctk.CTkLabel(
            goal_panel,
            text="15%",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#22C55E",
        ).pack(anchor="w", padx=24, pady=(6, 0))

        progress = ctk.CTkProgressBar(goal_panel, height=12, corner_radius=8, progress_color="#22C55E")
        progress.pack(fill="x", padx=24, pady=18)
        progress.set(0.72)

        ctk.CTkLabel(
            goal_panel,
            text="Reducao gradual de gordura mantendo massa magra.",
            wraplength=230,
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color="#CBD5E1",
        ).pack(anchor="w", padx=24, pady=(0, 24))

    def _create_coming_soon_screen(self, screen):
        features = [
            ("Sincronização de horários", "Conecte treinos, refeições e compromissos em uma agenda inteligente."),
            ("Automações fitness", "Receba ajustes automáticos para manter sua rotina no ritmo certo."),
            ("Alertas premium", "Lembretes precisos para treino, hidratação, dieta e avaliações."),
        ]

        content = self.content
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure((1, 2), weight=0)
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure((1, 2, 3), weight=0)

        panel = ctk.CTkFrame(content, corner_radius=30, fg_color="#111C2F")
        panel.grid(row=0, column=0, padx=32, pady=32, sticky="nsew")
        panel.grid_columnconfigure((0, 1, 2), weight=1)
        panel.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            panel,
            text=screen,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#38BDF8",
        ).grid(row=0, column=0, columnspan=3, padx=34, pady=(38, 8), sticky="w")

        ctk.CTkLabel(
            panel,
            text="Em Breve na Versão 2.0",
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color="#F8FAFC",
        ).grid(row=1, column=0, columnspan=3, padx=34, sticky="w")

        ctk.CTkLabel(
            panel,
            text="Estamos preparando sincronização de horários e automações para deixar seu plano fitness praticamente no piloto automático.",
            font=ctk.CTkFont(size=16),
            text_color="#CBD5E1",
            wraplength=760,
            justify="left",
        ).grid(row=2, column=0, columnspan=3, padx=34, pady=(12, 30), sticky="w")

        for column, (title, description) in enumerate(features):
            card = ctk.CTkFrame(panel, corner_radius=22, fg_color="#172033")
            card.grid(row=3, column=column, padx=(34 if column == 0 else 10, 34 if column == 2 else 10), pady=(0, 34), sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                card,
                text=f"0{column + 1}",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#0EA5E9",
            ).grid(row=0, column=0, padx=22, pady=(24, 8), sticky="w")

            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#F8FAFC",
                wraplength=230,
                justify="left",
            ).grid(row=1, column=0, padx=22, sticky="w")

            ctk.CTkLabel(
                card,
                text=description,
                font=ctk.CTkFont(size=14),
                text_color="#94A3B8",
                wraplength=230,
                justify="left",
            ).grid(row=2, column=0, padx=22, pady=(12, 24), sticky="w")

    def _create_workouts_screen(self):
        workouts = self._load_workouts()

        content = self.content
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure((1, 2), weight=0)
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure((1, 2, 3), weight=0)

        panel = ctk.CTkFrame(content, corner_radius=28, fg_color="#111C2F")
        panel.grid(row=0, column=0, padx=32, pady=32, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            panel,
            text="Treinos",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#F8FAFC",
        ).grid(row=0, column=0, padx=34, pady=(34, 8), sticky="w")

        ctk.CTkLabel(
            panel,
            text="Treinos carregados de data/treinos.json.",
            font=ctk.CTkFont(size=16),
            text_color="#94A3B8",
        ).grid(row=1, column=0, padx=34, sticky="w")

        workouts_list = ctk.CTkScrollableFrame(panel, corner_radius=22, fg_color="#0F172A")
        workouts_list.grid(row=2, column=0, padx=34, pady=34, sticky="nsew")
        workouts_list.grid_columnconfigure((0, 1), weight=1)

        for index, workout in enumerate(workouts):
            card = ctk.CTkFrame(workouts_list, corner_radius=20, fg_color="#172033")
            card.grid(row=index // 2, column=index % 2, padx=10, pady=10, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            name = workout.get("nome", "Treino sem nome")
            focus = workout.get("foco", "Foco nao informado")
            duration = workout.get("duracao", "Duracao nao informada")
            exercises = workout.get("exercicios", [])

            ctk.CTkLabel(
                card,
                text=name,
                font=ctk.CTkFont(size=19, weight="bold"),
                text_color="#38BDF8",
                wraplength=330,
                justify="left",
            ).grid(row=0, column=0, padx=22, pady=(22, 8), sticky="w")

            ctk.CTkLabel(
                card,
                text=focus,
                font=ctk.CTkFont(size=14),
                text_color="#CBD5E1",
                wraplength=330,
                justify="left",
            ).grid(row=1, column=0, padx=22, pady=(0, 10), sticky="w")

            ctk.CTkLabel(
                card,
                text=duration,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#F8FAFC",
            ).grid(row=2, column=0, padx=22, pady=(0, 12), sticky="w")

            ctk.CTkLabel(
                card,
                text=", ".join(exercises),
                font=ctk.CTkFont(size=13),
                text_color="#94A3B8",
                wraplength=330,
                justify="left",
            ).grid(row=3, column=0, padx=22, pady=(0, 22), sticky="w")

    def _create_stat_card(self, parent, column, label, value, detail, color):
        card = ctk.CTkFrame(parent, corner_radius=22, fg_color="#111C2F")
        card.grid(row=1, column=column, padx=(32 if column == 0 else 12, 32 if column == 2 else 12), pady=16, sticky="ew")

        ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=14),
            text_color="#94A3B8",
        ).pack(anchor="w", padx=22, pady=(20, 4))

        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color=color,
        ).pack(anchor="w", padx=22, pady=(0, 4))

        ctk.CTkLabel(
            card,
            text=detail,
            font=ctk.CTkFont(size=13),
            text_color="#CBD5E1",
        ).pack(anchor="w", padx=22, pady=(0, 20))


if __name__ == "__main__":
    app = FitPlannerApp()
    app.mainloop()
