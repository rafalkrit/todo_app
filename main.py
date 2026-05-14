import typer

from src.cli.registry import register_commands


app = typer.Typer(name="ToDo App", help="A professional ToDo Cli application.")

register_commands(app)

if __name__ == "__main__":
    app()
