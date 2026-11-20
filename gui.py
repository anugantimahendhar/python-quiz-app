
import customtkinter as ctk
from tkinter import messagebox
from quiz import Quiz


# ==========================================
# COLOR PALETTE
# ==========================================

ORANGE = "#F58220"
ORANGE_HOVER = "#DC7015"
BEIGE = "#EAE6DC"
IVORY = "#F7F5EF"
WHITE = "#FFFFFF"
CHARCOAL = "#33332F"
MUTED = "#79776F"
BORDER = "#E0DCD3"

GREEN = "#DDE9D7"
GREEN_TEXT = "#46663B"
WRONG = "#F7D9B8"


ctk.set_appearance_mode("light")


class QuizApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Quiz Studio")
        self.geometry("850x650")
        self.minsize(650, 450)

        self.configure(fg_color=IVORY)

        self.quiz = Quiz()

        self.timer_id = None
        self.time_left = 30

        self.option_buttons = []

        self.results_visible = False

        # Difficulty timer settings
        self.level_times = {
            "Beginner": 30,
            "Intermediate": 45,
            "Advanced": 60
        }

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_app
        )

        self.build_ui()
        self.load_question()

    # ==========================================
    # BUILD USER INTERFACE
    # ==========================================

    def build_ui(self):

        # Header
        header = ctk.CTkFrame(
            self,
            fg_color=ORANGE,
            corner_radius=0,
            height=70
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Quiz Studio.",
            font=("Segoe UI", 30, "bold"),
            text_color=CHARCOAL
        ).pack(
            side="left",
            padx=25
        )

        ctk.CTkLabel(
            header,
            text="PYTHON EDITION",
            font=("Segoe UI", 12, "bold"),
            text_color=CHARCOAL
        ).pack(
            side="right",
            padx=25
        )

        # Footer
        footer = ctk.CTkFrame(
            self,
            fg_color=BEIGE,
            corner_radius=0
        )

        footer.pack(
            side="bottom",
            fill="x"
        )

        ctk.CTkLabel(
            footer,
            text="QUIZ STUDIO",
            font=("Segoe UI", 11, "bold"),
            text_color=CHARCOAL
        ).pack(
            side="left",
            padx=25,
            pady=8
        )

        ctk.CTkLabel(
            footer,
            text="PRACTICE • LEARN • REPEAT",
            font=("Segoe UI", 11),
            text_color=MUTED
        ).pack(
            side="right",
            padx=25
        )

        # ==========================================
        # FIXED NAVIGATION
        # ==========================================

        self.navigation = ctk.CTkFrame(
            self,
            fg_color=IVORY,
            corner_radius=0
        )

        self.navigation.pack(
            side="bottom",
            fill="x",
            padx=25,
            pady=12
        )

        self.restart_button = ctk.CTkButton(
            self.navigation,
            text="Restart",
            width=120,
            height=45,
            corner_radius=0,
            fg_color=BEIGE,
            hover_color="#DAD5CA",
            text_color=CHARCOAL,
            font=("Segoe UI", 14, "bold"),
            command=self.restart_quiz
        )

        self.restart_button.pack(
            side="left"
        )

        self.next_button = ctk.CTkButton(
            self.navigation,
            text="Next Question →",
            width=170,
            height=45,
            corner_radius=0,
            fg_color=ORANGE,
            hover_color=ORANGE_HOVER,
            text_color=CHARCOAL,
            text_color_disabled=MUTED,
            font=("Segoe UI", 14, "bold"),
            command=self.next_question
        )

        self.next_button.pack(
            side="right"
        )

        # ==========================================
        # SCROLLABLE CONTENT
        # ==========================================

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color=IVORY,
            corner_radius=0,
            orientation="vertical",
            scrollbar_fg_color=IVORY,
            scrollbar_button_color=ORANGE,
            scrollbar_button_hover_color=ORANGE_HOVER
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(15, 5)
        )

        # ==========================================
        # TITLE AND TIMER
        # ==========================================

        top = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            pady=(0, 15)
        )

        title_frame = ctk.CTkFrame(
            top,
            fg_color="transparent"
        )

        title_frame.pack(
            side="left"
        )

        self.title_label = ctk.CTkLabel(
            title_frame,
            text=f"Python {self.quiz.level}",
            font=("Segoe UI", 24, "bold"),
            text_color=CHARCOAL
        )

        self.title_label.pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_frame,
            text="Test. Learn. Improve.",
            font=("Segoe UI", 13),
            text_color=MUTED
        ).pack(
            anchor="w"
        )

        self.timer_label = ctk.CTkLabel(
            top,
            text="00:30",
            width=100,
            height=45,
            fg_color=BEIGE,
            corner_radius=0,
            font=("Segoe UI", 20, "bold"),
            text_color=CHARCOAL
        )

        self.timer_label.pack(
            side="right"
        )

        # ==========================================
        # STATISTICS
        # ==========================================

        stats = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            pady=(0, 15)
        )

        for col in range(3):

            stats.grid_columnconfigure(
                col,
                weight=1,
                uniform="stats"
            )

        self.question_count = self.create_stat_card(
            stats,
            "QUESTION",
            "01 / 20",
            ORANGE,
            0
        )

        self.score_label = self.create_stat_card(
            stats,
            "SCORE",
            "0 Points",
            BEIGE,
            1
        )

        # ==========================================
        # DIFFICULTY DROPDOWN
        # ==========================================

        level_card = ctk.CTkFrame(
            stats,
            fg_color=WHITE,
            corner_radius=0
        )

        level_card.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=4
        )

        ctk.CTkLabel(
            level_card,
            text="SELECT LEVEL",
            font=("Segoe UI", 11, "bold"),
            text_color=CHARCOAL
        ).pack(
            anchor="w",
            padx=12,
            pady=(8, 2)
        )

        self.level_menu = ctk.CTkOptionMenu(
            level_card,

            values=[
                "Beginner",
                "Intermediate",
                "Advanced"
            ],

            command=self.change_level,

            width=150,
            height=33,
            corner_radius=0,

            fg_color=BEIGE,
            button_color=ORANGE,
            button_hover_color=ORANGE_HOVER,

            dropdown_fg_color=WHITE,
            dropdown_hover_color=BEIGE,
            dropdown_text_color=CHARCOAL,

            text_color=CHARCOAL,

            font=("Segoe UI", 14, "bold"),
            dropdown_font=("Segoe UI", 14),

            dynamic_resizing=False
        )

        self.level_menu.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.level_menu.set(
            self.quiz.level
        )

        # ==========================================
        # PROGRESS BAR
        # ==========================================

        self.progress = ctk.CTkProgressBar(
            self.content,
            height=7,
            corner_radius=0,
            fg_color=BEIGE,
            progress_color=ORANGE
        )

        self.progress.pack(
            fill="x",
            pady=(0, 18)
        )

        self.progress.set(0)

        # ==========================================
        # QUESTION CARD
        # ==========================================

        self.question_card = ctk.CTkFrame(
            self.content,
            fg_color=WHITE,
            corner_radius=0,
            border_width=1,
            border_color=BORDER
        )

        self.question_card.pack(
            fill="x",
            pady=(0, 10)
        )

        self.question_number = ctk.CTkLabel(
            self.question_card,
            text="QUESTION 01",
            font=("Segoe UI", 12, "bold"),
            text_color="#B35A14"
        )

        self.question_number.pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        self.question_label = ctk.CTkLabel(
            self.question_card,
            text="",
            font=("Segoe UI", 21, "bold"),
            text_color=CHARCOAL,
            wraplength=550,
            justify="left",
            anchor="w"
        )

        self.question_label.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

        # ==========================================
        # ANSWER OPTIONS
        # ==========================================

        options_frame = ctk.CTkFrame(
            self.question_card,
            fg_color="transparent"
        )

        options_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        for column in range(2):

            options_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="options"
            )

        for i in range(4):

            button = ctk.CTkButton(
                options_frame,
                text="",
                width=100,
                height=75,
                corner_radius=0,
                fg_color=IVORY,
                hover_color=BEIGE,
                text_color=CHARCOAL,
                text_color_disabled=CHARCOAL,
                border_width=1,
                border_color=BORDER,
                font=("Segoe UI", 14, "bold"),

                command=lambda index=i:
                    self.select_answer(index)
            )

            button.grid(
                row=i // 2,
                column=i % 2,
                sticky="nsew",
                padx=5,
                pady=5
            )

            self.option_buttons.append(
                button
            )

        # Feedback
        self.feedback = ctk.CTkLabel(
            self.question_card,
            text="Select one correct answer.",
            font=("Segoe UI", 13, "bold"),
            text_color=MUTED,
            wraplength=550,
            justify="left"
        )

        self.feedback.pack(
            anchor="w",
            padx=20,
            pady=12
        )

        self.question_card.bind(
            "<Configure>",
            self.resize_question
        )

    # ==========================================
    # RESPONSIVE TEXT WRAPPING
    # ==========================================

    def resize_question(self, event):

        width = max(
            200,
            event.width - 45
        )

        self.question_label.configure(
            wraplength=width
        )

        self.feedback.configure(
            wraplength=width
        )

    # Wrap longer answer options
    def format_option(self, index, text):

        import textwrap

        letter = chr(65 + index)

        wrapped = textwrap.fill(
            text,
            width=25,
            break_long_words=True,
            break_on_hyphens=False
        )

        return f"{letter}. {wrapped}"

    # ==========================================
    # CHANGE DIFFICULTY LEVEL
    # ==========================================

    def change_level(self, selected_level):

        if selected_level == self.quiz.level:
            return

        progress_started = (
            self.quiz.current_index > 0
            or self.quiz.answered
        )

        self.stop_timer()

        if progress_started:

            confirmation = messagebox.askyesno(
                "Change Difficulty",
                f"Switch to {selected_level} level?\n\n"
                "Your current quiz progress will be reset.",
                parent=self
            )

            if not confirmation:

                self.level_menu.set(
                    self.quiz.level
                )

                if not self.quiz.answered:
                    self.time_left += 1
                    self.update_timer()

                return

        self.quiz.set_level(
            selected_level
        )

        self.title_label.configure(
            text=f"Python {selected_level}"
        )

        self.level_menu.set(
            selected_level
        )

        self.load_question()

    # ==========================================
    # CREATE STAT CARDS
    # ==========================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        color,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=0
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=4
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 11, "bold"),
            text_color=CHARCOAL
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 21, "bold"),
            text_color=CHARCOAL
        )

        value_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        return value_label

    # ==========================================
    # LOAD QUESTIONS
    # ==========================================

    def load_question(self):

        self.stop_timer()

        question = self.quiz.get_question()

        number = self.quiz.current_index + 1
        total = self.quiz.get_total_questions()

        self.title_label.configure(
            text=f"Python {self.quiz.level}"
        )

        self.question_count.configure(
            text=f"{number:02d} / {total:02d}"
        )

        self.score_label.configure(
            text=f"{self.quiz.score} Points"
        )

        self.question_number.configure(
            text=(
                f"QUESTION {number:02d}"
                f"  •  {self.quiz.level.upper()}"
            )
        )

        self.question_label.configure(
            text=question["question"]
        )

        self.progress.set(
            number / total
        )

        for i, button in enumerate(
            self.option_buttons
        ):

            button.configure(
                text=self.format_option(
                    i,
                    question["options"][i]
                ),

                fg_color=IVORY,
                border_color=BORDER,
                state="normal"
            )

        self.feedback.configure(
            text="Select one correct answer.",
            text_color=MUTED
        )

        self.next_button.configure(
            state="disabled",
            text="View Results →"
            if number == total
            else "Next Question →"
        )

        self.time_left = self.level_times[
            self.quiz.level
        ]

        self.update_timer()

    # ==========================================
    # SELECT ANSWER
    # ==========================================

    def select_answer(self, selected_index):

        if self.quiz.answered:
            return

        self.stop_timer()

        correct = self.quiz.check_answer(
            selected_index
        )

        question = self.quiz.get_question()

        correct_index = question["answer"]

        self.highlight_answers(
            selected_index
        )

        if correct:

            self.feedback.configure(
                text="Correct answer! Well done.",
                text_color=GREEN_TEXT
            )

        else:

            answer = question["options"][
                correct_index
            ]

            self.feedback.configure(
                text=f"Incorrect! Correct answer: {answer}",
                text_color="#A35419"
            )

        self.score_label.configure(
            text=f"{self.quiz.score} Points"
        )

        self.next_button.configure(
            state="normal"
        )

    # ==========================================
    # HIGHLIGHT ANSWERS
    # ==========================================

    def highlight_answers(self, selected_index):

        correct_index = self.quiz.get_question()[
            "answer"
        ]

        for i, button in enumerate(
            self.option_buttons
        ):

            if i == correct_index:

                button.configure(
                    fg_color=GREEN,
                    border_color="#62834F"
                )

            elif i == selected_index:

                button.configure(
                    fg_color=WRONG,
                    border_color=ORANGE
                )

            button.configure(
                state="disabled"
            )

    # ==========================================
    # COUNTDOWN TIMER
    # ==========================================

    def update_timer(self):

        self.timer_id = None

        minutes, seconds = divmod(
            self.time_left,
            60
        )

        self.timer_label.configure(
            text=f"{minutes:02d}:{seconds:02d}",

            text_color="#B35A14"
            if self.time_left <= 10
            else CHARCOAL
        )

        if self.time_left == 0:

            self.time_up()

            return

        self.time_left -= 1

        self.timer_id = self.after(
            1000,
            self.update_timer
        )

    # Stop countdown
    def stop_timer(self):

        if self.timer_id is not None:

            self.after_cancel(
                self.timer_id
            )

            self.timer_id = None

    # ==========================================
    # TIME EXPIRED
    # ==========================================

    def time_up(self):

        if self.quiz.answered:
            return

        self.quiz.check_answer(-1)

        self.highlight_answers(-1)

        question = self.quiz.get_question()

        answer = question["options"][
            question["answer"]
        ]

        self.feedback.configure(
            text=f"Time's up! Correct answer: {answer}",
            text_color="#A35419"
        )

        self.next_button.configure(
            state="normal"
        )

    # ==========================================
    # NEXT QUESTION
    # ==========================================

    def next_question(self):

        if not self.quiz.answered:
            return

        self.stop_timer()

        if self.quiz.next_question():

            self.load_question()

        else:

            self.show_results()

    # ==========================================
    # FINAL RESULTS
    # ==========================================

    def show_results(self):

        self.stop_timer()

        self.results_visible = True

        self.navigation.pack_forget()

        for widget in self.content.winfo_children():

            widget.destroy()

        result_card = ctk.CTkFrame(
            self.content,
            fg_color=WHITE,
            corner_radius=0,
            border_width=1,
            border_color=BORDER
        )

        result_card.pack(
            fill="x",
            pady=5
        )

        ctk.CTkLabel(
            result_card,
            text="QUIZ COMPLETED",
            font=("Segoe UI", 14, "bold"),
            text_color=ORANGE
        ).pack(
            pady=(25, 5)
        )

        ctk.CTkLabel(
            result_card,
            text=f"{self.quiz.level} Level",
            font=("Segoe UI", 18, "bold"),
            text_color=MUTED
        ).pack(
            pady=5
        )

        ctk.CTkLabel(
            result_card,
            text="Your Results",
            font=("Segoe UI", 32, "bold"),
            text_color=CHARCOAL
        ).pack(
            pady=5
        )

        total = self.quiz.get_total_questions()

        score = self.quiz.score

        accuracy = self.quiz.get_accuracy()

        ctk.CTkLabel(
            result_card,
            text=f"{score} / {total}",
            font=("Segoe UI", 60, "bold"),
            text_color=ORANGE
        ).pack(
            pady=10
        )

        ctk.CTkLabel(
            result_card,
            text=f"Accuracy: {accuracy}%",
            font=("Segoe UI", 20, "bold"),
            text_color=CHARCOAL
        ).pack(
            pady=5
        )

        # Result statistics
        result_stats = ctk.CTkFrame(
            result_card,
            fg_color="transparent"
        )

        result_stats.pack(
            fill="x",
            padx=25,
            pady=10
        )

        for column in range(2):

            result_stats.grid_columnconfigure(
                column,
                weight=1,
                uniform="result"
            )

        self.create_stat_card(
            result_stats,
            "CORRECT",
            str(score),
            GREEN,
            0
        )

        self.create_stat_card(
            result_stats,
            "INCORRECT OR MISSED",
            str(total - score),
            BEIGE,
            1
        )

        if accuracy >= 80:

            message = "Excellent work!"

        elif accuracy >= 50:

            message = "Good job! Keep practicing."

        else:

            message = "Keep learning and try again!"

        ctk.CTkLabel(
            result_card,
            text=message,
            font=("Segoe UI", 18, "bold"),
            text_color=CHARCOAL,
            wraplength=450
        ).pack(
            pady=15
        )

        # Replay current level
        ctk.CTkButton(
            result_card,
            text="Play Again",
            width=230,
            height=45,
            corner_radius=0,
            fg_color=ORANGE,
            hover_color=ORANGE_HOVER,
            text_color=CHARCOAL,
            font=("Segoe UI", 15, "bold"),
            command=self.restart_quiz
        ).pack(
            pady=5
        )

        # Select different level
        ctk.CTkLabel(
            result_card,
            text="Try another difficulty",
            font=("Segoe UI", 13),
            text_color=MUTED
        ).pack(
            pady=(15, 5)
        )

        result_level_menu = ctk.CTkOptionMenu(
            result_card,

            values=[
                "Beginner",
                "Intermediate",
                "Advanced"
            ],

            command=self.start_new_level,

            width=230,
            height=40,
            corner_radius=0,

            fg_color=BEIGE,
            button_color=ORANGE,
            button_hover_color=ORANGE_HOVER,

            dropdown_fg_color=WHITE,
            dropdown_hover_color=BEIGE,
            dropdown_text_color=CHARCOAL,

            text_color=CHARCOAL,

            font=("Segoe UI", 14, "bold")
        )

        result_level_menu.set(
            self.quiz.level
        )

        result_level_menu.pack(
            pady=(5, 25)
        )

    # ==========================================
    # START NEW LEVEL FROM RESULTS
    # ==========================================

    def start_new_level(self, selected_level):

        self.quiz.set_level(
            selected_level
        )

        self.rebuild_ui()

    # ==========================================
    # RESTART QUIZ
    # ==========================================

    def restart_quiz(self):

        self.stop_timer()

        self.quiz.restart()

        self.rebuild_ui()

    # Rebuild the application interface
    def rebuild_ui(self):

        self.stop_timer()

        self.navigation.destroy()
        self.content.destroy()

        for widget in self.winfo_children():

            widget.destroy()

        self.option_buttons = []
        self.results_visible = False

        self.build_ui()

        self.load_question()

    # ==========================================
    # CLOSE APPLICATION
    # ==========================================

    def close_app(self):

        self.stop_timer()

        self.destroy()
