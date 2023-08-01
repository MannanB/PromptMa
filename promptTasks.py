from colorama import Fore
from halo import Halo
from GPT import get_completion

class PromptTask:
    def __init__(self, prompt_file):
        self.prompt_file = prompt_file
        self.loading_text = "Generating response"
        self.success_text = "Response generated"
        self.required = []
        
        try:
            with open("./prompts/"+self.prompt_file+"/prompt.txt", "r") as f:
                self.prompt = f.read()
            with open("./prompts/"+self.prompt_file+"/role.txt", "r") as f:
                self.role = f.read()
        except FileNotFoundError:
            print(Fore.RED + f"Error: Prompt {self.prompt} not found. Skipping")

    def run(self, **kwargs):
        for r in self.required:
            if r not in kwargs:
                print(Fore.RED + f"Error: {r} is required for the prompt {self.prompt_file}")
                exit()

        spinner = Halo(text=self.loading_text, spinner='dots', placement='right')
        spinner.start()
        print()
        try:
            prompt = self.prompt[:]
            for k, v in kwargs.items():
                prompt = prompt.replace(f"{{{k}}}", v)
            response = get_completion(self.role, prompt)
            spinner.succeed(self.success_text)
            return response
        except Exception as e:
            spinner.fail("Failed to generate response")
            print(Fore.RED + "Error: " + str(e))
            exit()

class QuestionsTask(PromptTask):
    def __init__(self):
        super().__init__("questions")
        self.loading_text = "Generating questions"
        self.success_text = "Questions generated"
        self.required = ["prompt"]

class AddQATask(PromptTask):
    def __init__(self):
        super().__init__("addqa")
        self.loading_text = "Generating better prompt"
        self.success_text = "Prompt generated"
        self.required = ["prompt", "questions_block"]

    def run(self, **kwargs):
        questions_block = '<questions>\n'
        for q, a in kwargs["qas"]:
            if not a:
                continue
            questions_block += f'    <questionanswer>\n        <question>{q}</question>\n        <answer>{a}</answer>\n    </questionanswer>\n'
        questions_block += '</questions>\n'
        del kwargs["qas"]
        return super().run(questions_block=questions_block, **kwargs)

class PlannerTask(PromptTask):
    def __init__(self):
        super().__init__("planner")
        self.loading_text = "Generating a plan"
        self.success_text = "Plan generated"
        self.required = ["prompt"]