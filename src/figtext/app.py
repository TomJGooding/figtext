import pyfiglet
import pyperclip
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Input, Label, Select, Static

FIGLET_FONTS = pyfiglet.FigletFont.getFonts()


class FigtextApp(App):
    CSS = """
    Horizontal {
        height: 3;
        margin-bottom: 1;
    }

    Input {
        width: 1fr;
    }

    Label {
        height: 3;
        content-align: center middle;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Text:")
            yield Input("Hello, World!")
        with Horizontal():
            yield Label("Font:")
            yield Select(
                options=((font, font) for font in FIGLET_FONTS),
                value=pyfiglet.DEFAULT_FONT,
            )
        yield Static(id="figlet-output")
        yield Button("Copy to Clipboard", variant="primary")

    @on(Input.Changed)
    def on_input_changed(self) -> None:
        self.update_figlet_output()

    @on(Select.Changed)
    def on_select_changed(self) -> None:
        self.update_figlet_output()

    def update_figlet_output(self) -> None:
        text = self.query_one(Input).value
        font = self.query_one(Select).value
        if text is not None and font is not None:
            figlet_output = pyfiglet.figlet_format(text, str(font))
            self.query_one("#figlet-output", Static).update(figlet_output)

    @on(Button.Pressed)
    def on_button_pressed(self) -> None:
        figlet_output = self.query_one("#figlet-output", Static).renderable
        pyperclip.copy(str(figlet_output))


def run() -> None:
    app = FigtextApp()
    app.run()
