from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        # Set up window and canvas
        self.window = Tk()
        self.window.title("Trivials")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Button images
        tbut = PhotoImage(file="Day 34/images/true.png")
        fbut = PhotoImage(file="Day 34/images/false.png")

        # Score Counter
        self.score_label = Label(text=f"Score: {self.quiz.score}", fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        # Canvas
        self.canvas = Canvas(width=300, height=250, bg="white", highlightthickness=0)
        self.question_txt = self.canvas.create_text(
            150, 125, width=280, text="Some question...", fill=THEME_COLOR, font=("Arial", 20, "italic"))
        
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # Buttons
        self.true_button = Button(image=tbut, highlightthickness=0, command=lambda: self.tbut_push())
        self.true_button.grid(row=2, column=0)
        self.false_button = Button(image=fbut, highlightthickness=0, command=lambda: self.fbut_push())
        self.false_button.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_txt = self.quiz.next_question()
            self.canvas.itemconfig(self.question_txt, text=q_txt)
        else:
            self.canvas.itemconfig(self.question_txt, text="You've reached the end of the quiz!")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def tbut_push(self):
        # outscore = self.quiz.check_answer('true')
        # self.quiz.score += int(outscore)
        # self.score_label.config(text=f"Score: {self.quiz.score}")
        self.feedback(self.quiz.check_answer('true'))

    def fbut_push(self):
        # outscore = self.quiz.check_answer('false')
        # self.quiz.score += int(outscore)
        # self.score_label.config(text=f"Score: {self.quiz.score}")
        self.feedback(self.quiz.check_answer('false'))

    def feedback(self, is_correct):
        if is_correct:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        self.window.after(1000, self.re_enable)

    def re_enable(self):
        self.true_button.config(state="active")
        self.false_button.config(state="active")
        self.get_next_question()