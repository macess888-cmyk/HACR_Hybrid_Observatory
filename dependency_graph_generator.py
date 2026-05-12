import ast
import json
import os

ROOT_DIR = "."
OUTPUT_FILE = "dependency_graph_report.json"

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "Outputs",
    "Outputs_Normalized"
}

nodes = []
edges = []

python_files = []

for root, dirs, files in os.walk(ROOT_DIR):
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file).replace("\\", "/").lstrip("./")
            python_files.append(path)

module_names = {
    os.path.splitext(os.path.basename(path))[0]: path
    for path in python_files
}

for path in python_files:
    nodes.append(path)

    with open(path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            continue

    for item in ast.walk(tree):
        imported = None

        if isinstance(item, ast.Import):
            for alias in item.names:
                imported = alias.name.split(".")[0]

                if imported in module_names:
                    edges.append({
                        "source": path,
                        "target": module_names[imported],
                        "type": "import"
                    })

        elif isinstance(item, ast.ImportFrom):
            if item.module:
                imported = item.module.split(".")[0]

                if imported in module_names:
                    edges.append({
                        "source": path,
                        "target": module_names[imported],
                        "type": "from_import"
                    })

report = {
    "lens": "DEPENDENCY_GRAPH_GENERATOR",
    "status": "TRACEABLE",
    "score": len(edges),
    "observer_mode": True,
    "summary": "Generates a static source dependency graph from Python imports.",
    "nodes": nodes,
    "edges": edges,
    "findings": [
        {
            "python_files_detected": len(nodes),
            "internal_edges_detected": len(edges)
        }
    ],
    "non_claims": [
        "Not runtime monitoring",
        "Not execution control",
        "Not certification",
        "Not full architectural validation"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{OUTPUT_FILE} -> TRACEABLE")
print(f"Python files: {len(nodes)}")
print(f"Internal dependency edges: {len(edges)}")