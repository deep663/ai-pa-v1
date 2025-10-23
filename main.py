# main.py
import argparse
from agent.agent import ask_agent
import readline  # nicer CLI on unix
import sys

def repl():
    print("EVA CLI — type 'exit' or Ctrl-C to quit.")
    while True:
        try:
            text = input("You: ").strip()
            if not text:
                continue
            if text.lower() in ("exit", "quit"):
                print("Bye.")
                break
            response = ask_agent(text)
            print("EVA:", response)
        except KeyboardInterrupt:
            print("\nInterrupted — exiting.")
            break
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    repl()
