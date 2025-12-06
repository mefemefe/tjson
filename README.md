## T-JSON (TreeJSON / TUI-JSON)
### Traverse a JSON using a collapsible Tree
#### Will show 2 Trees side by side if 2 inputs are passed.
![Screenshot](screenshot.png)
---

## Install 
`pip install -e .`

## Usage:
`treejson <json_file_or_json_string> OPTIONAL:<json_file_or_json_string2>`

### With file:
`treejson example.json`

### With string:
`treejson '{"test": {"test2": "test3"}}'`

### Two files:
`treejson 1.json 2.json`


### Bindings
`q` QUIT

`SPACE` COLLAPSE/EXPAND

`e` EXPANDALL

`d` EXPAND BOTH TREES

`c` COLLAPSEALL

`f` COLLAPSE BOTH TREES

`s` SEARCH (find next node that matches query, if no match, searches from root)
