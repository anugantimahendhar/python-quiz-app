
import json
import random
from pathlib import Path


class Quiz:

    def __init__(self):

        file_path = Path(__file__).parent / "questions.json"

        with open(file_path, "r", encoding="utf-8") as file:
            self.all_questions = json.load(file)

        self.levels = [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]

        self.level = "Beginner"

        self.questions = []
        self.current_index = 0
        self.score = 0
        self.answered = False

        self.set_level("Beginner")

    # Change difficulty level
    def set_level(self, level):

        if level not in self.levels:
            raise ValueError("Invalid difficulty level.")

        self.level = level

        self.restart()

    # Load questions of the selected level
    def restart(self):

        self.questions = list(
            self.all_questions[self.level]
        )

        if not self.questions:
            raise ValueError("No questions found.")

        random.shuffle(self.questions)

        self.current_index = 0
        self.score = 0
        self.answered = False

    # Return current question
    def get_question(self):

        return self.questions[self.current_index]

    # Check selected answer
    def check_answer(self, selected_answer):

        if self.answered:
            return False

        self.answered = True

        correct_answer = self.get_question()["answer"]

        if selected_answer == correct_answer:

            self.score += 1

            return True

        return False

    # Move to next question
    def next_question(self):

        if not self.answered:
            return False

        if self.current_index < len(self.questions) - 1:

            self.current_index += 1
            self.answered = False

            return True

        return False

    # Calculate accuracy
    def get_accuracy(self):

        return round(
            self.score / len(self.questions) * 100,
            2
        )

    # Total questions
    def get_total_questions(self):

        return len(self.questions)
