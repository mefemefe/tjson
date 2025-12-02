from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree
from .search_screen import SearchScreen, Search
from ..controller.search import find_first_match, focus_node
from ..controller.build_tree import build_tree


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
        ("s", "search", "Search"),
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
        build_tree(tree.root, self.json_data)

    def action_expand_all(self) -> None:
        tree = self.query_one(Tree)
        tree.root.expand_all()

    def action_collapse_all(self) -> None:
        tree = self.query_one(Tree)
        tree.root.collapse_all()
        tree.root.expand()
    
    def action_search(self) -> None:
        self.push_screen(SearchScreen())
    
    def on_search(self, event: Search) -> None:
        query = event.query
        tree = self.query_one(Tree)
        node = find_first_match(tree.root, query)
        if node:
            focus_node(tree, node)
            self.set_focus(tree)
