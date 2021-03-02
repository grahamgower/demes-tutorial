import json
import pathlib

example_dir = pathlib.Path("examples")
example_dir.mkdir(exist_ok=True)

with open("tutorial.ipynb") as f:
    data = json.load(f)

for cell in data["cells"]:
    if cell["cell_type"] == "markdown":
        source = cell["source"]
        state = 0
        fp = None
        for line in source:
            if line.startswith("```yaml"):
                state = 1
            elif state == 1:
                if line.startswith("```"):
                    state = 0
                    fp.close()
                    fp = None
                elif fp is None:
                    assert line.startswith("# ")
                    filename = line[1:].strip()
                    fp = open(example_dir / filename, "w")
                else:
                    fp.write(line)

