#!/usr/bin/env python3
import os
import ast
from pathlib import Path

SRC_ROOT = Path("src/personal_agent")
DOC_PATH = Path("docs/design/subsystems_responsbility.md")


def extract_docstring_from_init(init_path):
    if not init_path.exists():
        return "subsystem responsibility to be added"
    with open(init_path, "r", encoding="utf-8") as f:
        node = ast.parse(f.read())
        return ast.get_docstring(node) or "subsystem responsibility to be added"


def extract_api_info(api_dir):
    api_info = []
    if not api_dir.exists():
        return api_info
    for py_file in api_dir.glob("*.py"):
        with open(py_file, "r", encoding="utf-8") as f:
            node = ast.parse(f.read())
        for class_node in [n for n in node.body if isinstance(n, ast.ClassDef)]:
            class_doc = ast.get_docstring(class_node) or ""
            methods = []
            for item in class_node.body:
                if isinstance(item, ast.FunctionDef):
                    sig = f"{item.name}({', '.join(arg.arg for arg in item.args.args if arg.arg != 'self')})"
                    doc = ast.get_docstring(item) or ""
                    methods.append((sig, doc))
            api_info.append(
                {"class": class_node.name, "class_doc": class_doc, "methods": methods}
            )
    return api_info


def main():
    lines = ["# 子系统职责与接口一览\n"]
    for subdir in SRC_ROOT.iterdir():
        if not subdir.is_dir() or subdir.name.startswith("__"):
            continue
        init_path = subdir / "__init__.py"
        responsibility = extract_docstring_from_init(init_path)
        lines.append(f"## {subdir.name}\n")
        lines.append(f"**职责**：{responsibility}\n")
        api_dir = subdir / "api"
        api_info = extract_api_info(api_dir)
        if not api_info:
            lines.append("_无 API 接口定义_\n")
        else:
            for cls in api_info:
                lines.append(f"### 接口类：{cls['class']}\n")
                if cls["class_doc"]:
                    lines.append(f"{cls['class_doc']}\n")
                for sig, doc in cls["methods"]:
                    lines.append(f"- `{sig}`\n")
                    if doc:
                        lines.append(f"  - {doc.replace(chr(10), '  ')}\n")
        lines.append("\n---\n")
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DOC_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"文档已生成：{DOC_PATH}")


if __name__ == "__main__":
    main()
