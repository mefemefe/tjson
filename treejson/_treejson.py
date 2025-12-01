from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree
from textual.widgets.tree import TreeNode
from ._search import SearchScreen, Search


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
    
    def action_search(self) -> None:
        self.push_screen(SearchScreen())
    
    def on_search(self, event: Search) -> None:
        query = event.query
        node = self.find_first_match(self.query_one(Tree).root, query)
        if node:
            self.focus_node(node)

    def find_first_match(self, node: TreeNode[Any], query: str) -> TreeNode[Any] | None:
        """Depth-first search for partial label match."""
        if query in node.label.plain.lower():
            return node
        for child in node.children:
            match = self.find_first_match(child, query)
            if match:
                return match
        return None

    def focus_node(self, node: TreeNode[Any]) -> None:
        """Expand path and set cursor."""
        tree: Tree[Any] = self.query_one(Tree)
        current = node
        while current.parent and not current.parent.is_expanded:
            current.parent.expand()
            current = current.parent
        tree.move_cursor(node)
        if not node.allow_expand:
            tree.move_cursor(node)
        else:
            node.expand()
        self.set_focus(tree)
