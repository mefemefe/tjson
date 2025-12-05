## TREEJSON
### Traverse a JSON using a collapsible Tree 
![Screenshot](screenshot.png)
---

## Install 
`pip install -e .`

## Usage:
`treejson <json_file_or_json_string>`

### With file:
`treejson example.json`

### With string:
`treejson '{"test": {"test2": "test3"}}'`


### Bindings
`q` QUIT

`e` EXPANDALL

`c` COLLAPSEALL

`s` SEARCH (find next node that matches query, if no match, searches from root)