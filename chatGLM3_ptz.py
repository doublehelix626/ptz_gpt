from openai import OpenAI
import re
import argparse
from PTZWrapper import *
import math
import numpy as np
import os
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument("--prompt", type=str, default="prompts/ptz_basic.txt")
parser.add_argument("--sysprompt", type=str, default="system_prompts/ptz_basic.txt")
args = parser.parse_args()
use_stream = False

base_url = ""
client = OpenAI(api_key="EMPTY", base_url=base_url)
print("Initializing ChatGLM3...")

with open(args.sysprompt, "r", encoding="utf-8") as f:
    sysprompt = f.read()

chat_history = [
    {
        "role": "system",
        "content": sysprompt
    },
    {
        "role": "user",
        "content": "以1的速度向右运动2秒"
    },
    {
        "role": "assistant",
        "content": """```python
PTZController.pan_move(1,2)
```

这段代码使用了 `PTZController.pan_move(speed=1,times=2)` 这个方法，使得ptz球机以1的速度向右转动了2秒。其中1为方法中speed的参数，2为方法中times的参数。"""
    }
]

print(f"Done.")
code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)


def ask(prompt):
    chat_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    response = client.chat.completions.create(
        model="chatglm3-6b",
        messages=chat_history,
        stream=use_stream)
    if response:
        if use_stream:
            for chunk in response:
                print(chunk.choices[0].delta.content)
        else:
            content = response.choices[0].message.content
    else:
        print("Error:", response.status_code)
    chat_history.append(
        {
            "role": "assistant",
            "content": response.choices[0].message.content,
        }
    )
    return chat_history[-1]["content"]


def extract_python_code(content):
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        full_code = "\n".join(code_blocks)

        if full_code.startswith("python"):
            full_code = full_code[7:]

        return full_code
    else:
        return None


class colors:  # You may need to change color settings
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


print(f"Initializing PTZ...")
PTZController = PTZController()
print(f"Done.")

with open(args.prompt, "r", encoding="utf-8") as f:
    prompt = f.read()

ask(prompt)
print("Welcome to the ptz chatbot! I am ready to help you with your ptz‘s questions and commands.")

while True:
    try:
        question = input(colors.YELLOW + "PTZ> " + colors.ENDC)

        if question == "!quit" or question == "!exit":
            break

        if question == "!clear":
            os.system("cls")
            continue

        response = ask(question)
        print("chatbot:"+f"\n{response}\n")
        try:
            code = extract_python_code(response)
            if code is not None:
                print("Please wait while I run the code in ptz...")
                exec(extract_python_code(response))
                print("Done!\n")
        except Exception as e:
            print(e)
            if chat_history[-1]["role"] =="user":
                chat_history = chat_history[:-1]
            chat_history = chat_history[:-2]
    except Exception as e:
        print(e)
