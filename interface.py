from os import linesep
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Header, Footer,Rule,Static

# Create an interface to fill the necessary data for an Invoice
# the system should be usable with different fetching mehtods, file input(csv,json),database, or others
# the form shoudl be intuitive to fill
# fields should remember earlier values to fill faster in subsequent times
#
class Invoice_app(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "style.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.header=Header()
        yield self.header
        with Horizontal(id="titleRow"):
            yield Static("Business info", classes="header")
            yield Button("Brows")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Invoicer"
        # self.sub_title = "With title and sub-title"


if __name__ == "__main__":
    app = Invoice_app()
    app.run()
