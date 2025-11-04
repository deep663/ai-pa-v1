import click
from agent.agent import ask_agent
import sys
from rich.console import Console

@click.group()
def cli():
    """EVA CLI"""
    pass

@cli.command()
@click.argument('text', nargs=-1)
def chat(text):
    """Start a chat with EVA."""
    console = Console()
    if not text:
        # Interactive mode
        console.print("[bold cyan]EVA CLI[/bold cyan] — type 'exit' or Ctrl-C to quit.")
        while True:
            try:
                text_input = console.input("[bold green]You: [/bold green]").strip()
                if not text_input:
                    continue
                if text_input.lower() in ("exit", "quit"):
                    console.print("[bold cyan]Bye.[/bold cyan]")
                    break
                with console.status("[bold yellow]EVA is thinking...[/bold yellow]"):
                    response = ask_agent(text_input)
                console.print(f"[bold blue]EVA:[/] {response}")
            except KeyboardInterrupt:
                console.print("\n[bold cyan]Interrupted — exiting.[/bold cyan]")
                break
            except Exception as e:
                console.print(f"[bold red]Error:[/] {e}")
    else:
        # Command-line mode
        with console.status("[bold yellow]EVA is thinking...[/bold yellow]"):
            response = ask_agent(" ".join(text))
        console.print(f"[bold blue]EVA:[/] {response}")

if __name__ == "__main__":
    cli()
