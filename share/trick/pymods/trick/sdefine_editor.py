#!/usr/bin/env python3
"""Simple GUI tool to generate Trick S_define snippets.

This script crawls a models directory for header and source files and
allows a user to add them to an S_define file via a minimal Tkinter GUI.
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Tuple


def crawl_models(directory: str) -> Tuple[List[str], List[str]]:
    """Return relative header and source file paths within *directory*."""
    headers: List[str] = []
    sources: List[str] = []
    for root, _dirs, files in os.walk(directory):
        for name in files:
            rel = os.path.relpath(os.path.join(root, name), directory)
            if name.endswith((".h", ".hh", ".hpp")):
                headers.append(rel)
            elif name.endswith((".c", ".cc", ".cpp", ".cxx")):
                sources.append(rel)
    headers.sort()
    sources.sort()
    return headers, sources


class SDefineEditor(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Trick S_define Editor")
        self.geometry("800x600")
        self.models_dir: str | None = None
        self.headers: List[str] = []
        self.sources: List[str] = []
        self.selected_headers: List[str] = []
        self.selected_sources: List[str] = []
        self._build_ui()

    def _build_ui(self) -> None:
        top = tk.Frame(self)
        top.pack(fill=tk.X)
        tk.Button(top, text="Open Models Directory", command=self._choose_dir).pack(side=tk.LEFT)
        self.dir_label = tk.Label(top, text="")
        self.dir_label.pack(side=tk.LEFT, padx=4)

        lists = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        lists.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(lists)
        tk.Label(left, text="Headers").pack()
        self.header_list = tk.Listbox(left, selectmode=tk.MULTIPLE)
        self.header_list.pack(fill=tk.BOTH, expand=True)
        lists.add(left)

        middle = tk.Frame(lists)
        tk.Label(middle, text="Sources").pack()
        self.source_list = tk.Listbox(middle, selectmode=tk.MULTIPLE)
        self.source_list.pack(fill=tk.BOTH, expand=True)
        lists.add(middle)

        right = tk.Frame(lists)
        tk.Label(right, text="Selected").pack()
        self.selected_list = tk.Listbox(right)
        self.selected_list.pack(fill=tk.BOTH, expand=True)
        lists.add(right)

        buttons = tk.Frame(self)
        buttons.pack(fill=tk.X)
        tk.Button(buttons, text="Add Headers", command=self._add_headers).pack(side=tk.LEFT)
        tk.Button(buttons, text="Add Sources", command=self._add_sources).pack(side=tk.LEFT)

        self.text = tk.Text(self)
        self.text.pack(fill=tk.BOTH, expand=True)

        tk.Button(self, text="Save S_define", command=self._save).pack(side=tk.RIGHT, pady=4, padx=4)

    def _choose_dir(self) -> None:
        directory = filedialog.askdirectory()
        if directory:
            self.models_dir = directory
            self.dir_label.config(text=directory)
            self.headers, self.sources = crawl_models(directory)
            self.header_list.delete(0, tk.END)
            self.source_list.delete(0, tk.END)
            for h in self.headers:
                self.header_list.insert(tk.END, h)
            for s in self.sources:
                self.source_list.insert(tk.END, s)

    def _add_headers(self) -> None:
        for i in self.header_list.curselection():
            header = self.headers[i]
            if header not in self.selected_headers:
                self.selected_headers.append(header)
                self.selected_list.insert(tk.END, f"##include \"{header}\"")
        self._update_text()

    def _add_sources(self) -> None:
        for i in self.source_list.curselection():
            src = self.sources[i]
            if src not in self.selected_sources:
                self.selected_sources.append(src)
                self.selected_list.insert(tk.END, f"    ({src})")
        self._update_text()

    def _update_text(self) -> None:
        lines: List[str] = []
        for h in self.selected_headers:
            lines.append(f"##include \"{h}\"")
        if self.selected_sources:
            lines.append("LIBRARY DEPENDENCIES:")
            lines.append("    (")
            for s in self.selected_sources:
                lines.append(f"      ({s})")
            lines.append("    )")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "\n".join(lines))

    def _save(self) -> None:
        file = filedialog.asksaveasfilename(defaultextension="S_define")
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END))
            messagebox.showinfo("Saved", f"S_define saved to {file}")


def main() -> None:
    SDefineEditor().mainloop()


if __name__ == "__main__":
    main()
