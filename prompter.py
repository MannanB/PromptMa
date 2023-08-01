import os
from colorama import init
from colorama import Fore, Back, Style
from halo import Halo
import time
from promptTasks import QuestionsTask, AddQATask, PlannerTask

init()
os.system('cls')
print()

while True:

    raw_prompt = input(Fore.GREEN + "Input the prompt to be optimized: " + Fore.RESET + Fore.BLUE)

    questions2answer = QuestionsTask().run(prompt=raw_prompt)

    questions = []
    for question in questions2answer.split("\n"):
        if question != "" and ("<" not in question) and ("end" not in question.lower()):
            questions.append(question)

    print(Fore.YELLOW + "\nAnswer the following questions to help improve the prompt. If you don't know the answer or the question is irrelevant, just press enter." + Fore.RESET)

    qas = []
    for question in questions:
        answer = input(Fore.CYAN + question + " > " + Fore.RESET)
        qas.append([question, answer])
    
    specific_prompt = AddQATask().run(qas=qas, prompt=raw_prompt)

    print(Fore.GREEN + "\nSpecified prompt: " + Fore.RESET + Fore.MAGENTA + specific_prompt + Fore.RESET + "\n")


    plan = PlannerTask().run(prompt=specific_prompt)
    print(plan)
    print()

    planned_prompt = specific_prompt + "\n\nTo accomplish this, please follow the steps below:\n" + plan
    print(Fore.GREEN + "\nPlanned prompt: " + Fore.RESET + Fore.MAGENTA + planned_prompt + Fore.RESET + "\n")


    input(Fore.GREEN + "\nEnter to try again")
    print()