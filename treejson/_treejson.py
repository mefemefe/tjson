from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree
from textual.widgets.tree import TreeNode


class TreeJson(App):
    """A Textual app to visualize JSON data in a tree structure."""

    CSS = """
    Tree {
        padding: 1;
        scrollbar-gutter: stable;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("e", "expand_all", "Expand All"),
        ("c", "collapse_all", "Collapse All"),
    ]

    def __init__(self, json_data: Any, title: str = "JSON Tree"):
        super().__init__()
        self.json_data = json_data
        self.app_title = title

    def compose(self) -> ComposeResult:
        yield Header()
        yield Tree(self.app_title)
        yield Footer()

    def on_mount(self) -> None:
        """Load the JSON data into the tree when the app starts."""
        tree = self.query_one(Tree)
        tree.root.expand()
        self.add_json_node(tree.root, self.json_data)

    def add_json_node(self, node: TreeNode, data: Any) -> None:
        """Recursively adds JSON data to the tree."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    # Create a branch for complex types
                    branch = node.add(f"[bold blue]{key}[/]", expand=False)
                    self.add_json_node(branch, value)
                else:
                    # Add leaf for primitive types
                    node.add_leaf(f"[blue]{key}:[/] [green]{value!r}[/]")
        
        elif isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    # Create a branch for complex items in a list
                    branch = node.add(f"[bold magenta]Item {index}[/]", expand=False)
                    self.add_json_node(branch, item)
                else:
                    # Add leaf for primitive items in a list
                    node.add_leaf(f"[magenta][{index}]:[/] [green]{item!r}[/]")
        else:
            # Fallback for root level primitives
            node.add_leaf(f"[green]{data!r}[/]")

    def action_expand_all(self) -> None:
        tree = self.query_one(Tree)
        tree.root.expand_all()

    def action_collapse_all(self) -> None:
        tree = self.query_one(Tree)
        tree.root.collapse_all()
        tree.root.expand()
