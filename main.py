from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.agents import tool
from openai import OpenAI
import random

_ = load_dotenv()

client = OpenAI()


class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=self.messages)
        return completion.choices[0].message.content


prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

random_outfit_one_garment:
Use the user input and extract type of garment that the user gave and select if it is t_shirt, pants or shoes.
Then give random color for the other two garment that combine with the first garment given by the user.

random_outfit_two_garment:
Use the user input and extract type of garment that the user gave and select if it is t_shirt, pants or shoes.
Then give random color for the other garment that combine with the garments given by the user.

Example session:

Question: I have a blue t-shirt?
Thought: I should select that is a blue t-shirt and output random color that combine for the pants and shoes.
Action: Random outfit one garment: Blue T-shirt
PAUSE

You will be called again with this:

Observation: A black pants and a white shoes combine with the garments given by the user.

You then output:

Answer: A black pants and a white shoes combine perfectly with the garments given that was a blue T-shirt.
""".strip()


def random_outfit_one_garment(user_input):
    garment_type = "t-shirt" if "t-shirt" in user_input else "pants" if "pants" in user_input else "shoes"
    colors = ["red", "blue", "green", "black", "white"]
    random_colors = random.sample(colors, 2)
    return {
        "garment": garment_type,
        "combination": {
            "color_1": random_colors[0],
            "color_2": random_colors[1]
        }
    }


