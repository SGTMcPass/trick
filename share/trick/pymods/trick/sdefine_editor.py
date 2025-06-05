#!/usr/bin/env python3

from dataclasses import dataclass, field
@dataclass
class SimObject:
    """Representation of a Trick SimObject."""

    name: str
    instance: str
    members: List[Tuple[str, str]] = field(default_factory=list)
    jobs: List[Tuple[str, str]] = field(default_factory=list)


        self.simobjects: List[SimObject] = []
        sim_frame = tk.Frame(lists)
        tk.Label(sim_frame, text="Sim Objects").pack()
        self.sim_list = tk.Listbox(sim_frame)
        self.sim_list.pack(fill=tk.BOTH, expand=True)
        lists.add(sim_frame)

        tk.Button(buttons, text="New SimObject", command=self._new_simobject).pack(side=tk.LEFT)
        tk.Button(buttons, text="Add to SimObject", command=self._add_to_simobject).pack(side=tk.LEFT)
"""Simple GUI tool to generate Trick ``S_define`` snippets.

This script crawls a models directory for header files and allows a user
to select the headers and classes found within to compose ``S_define``
content via a minimal Tkinter GUI.

"""

from __future__ import annotations

import os
import tkinter as tk

from tkinter import filedialog, messagebox, simpledialog
from typing import Dict, List, Tuple
import re


def crawl_models(directory: str) -> List[str]:
    """Return relative header file paths within *directory*.

    Directories whose names start with ``SIM_`` as well as any symbolic
    links are ignored while crawling.
    """
    headers: List[str] = []
    for root, dirs, files in os.walk(directory, followlinks=False):
        # remove simulation directories and symlinked directories from walk
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith("SIM_") and not os.path.islink(os.path.join(root, d))
        ]
        for name in files:
            full = os.path.join(root, name)
            if os.path.islink(full):
                continue
            if name.endswith((".h", ".hh", ".hpp")):
                rel = os.path.relpath(full, directory)
                headers.append(rel)
    headers.sort()
    return headers


def parse_header_classes(path: str) -> List[str]:
    """Return class names defined in *path*."""
    pattern = re.compile(r"^\s*(?:class|struct)\s+(\w+)\b")
    classes: List[str] = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                m = pattern.match(line)
                if m:
                    name = m.group(1)
                    if name not in classes:
                        classes.append(name)
    except OSError:
        pass
    return classes



class SDefineEditor(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Trick S_define Editor")
        self.geometry("800x600")
        self.models_dir: str | None = None
        self.headers: List[str] = []

        self.selected_headers: List[str] = []
        self.selected_classes: List[Tuple[str, str]] = []
        self.class_header_map: Dict[str, str] = {}
        self.header_class_cache: Dict[str, List[str]] = {}

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

        self.header_list.bind("<<ListboxSelect>>", self._update_class_list)
        lists.add(left)

        class_frame = tk.Frame(lists)
        tk.Label(class_frame, text="Classes").pack()
        self.class_list = tk.Listbox(class_frame, selectmode=tk.MULTIPLE)
        self.class_list.pack(fill=tk.BOTH, expand=True)
        lists.add(class_frame)


        right = tk.Frame(lists)
        tk.Label(right, text="Selected").pack()
        self.selected_list = tk.Listbox(right)
        self.selected_list.pack(fill=tk.BOTH, expand=True)
        lists.add(right)

        buttons = tk.Frame(self)
        buttons.pack(fill=tk.X)
        tk.Button(buttons, text="Add Headers", command=self._add_headers).pack(side=tk.LEFT)
        tk.Button(buttons, text="Add Classes", command=self._add_classes).pack(side=tk.LEFT)


        self.text = tk.Text(self)
        self.text.pack(fill=tk.BOTH, expand=True)

        tk.Button(self, text="Save S_define", command=self._save).pack(side=tk.RIGHT, pady=4, padx=4)

    def _choose_dir(self) -> None:
        directory = filedialog.askdirectory()
        if directory:
            self.models_dir = directory
            self.dir_label.config(text=directory)

            self.headers = crawl_models(directory)
            self.header_list.delete(0, tk.END)
            for h in self.headers:
                self.header_list.insert(tk.END, h)
            self.class_list.delete(0, tk.END)
            self.class_header_map.clear()


    def _add_headers(self) -> None:
        for i in self.header_list.curselection():
            header = self.headers[i]
    def _new_simobject(self) -> None:
        """Create a new SimObject."""
        cname = simpledialog.askstring("SimObject Class", "SimObject class name")
        if not cname:
            return
        instance = simpledialog.askstring("Instance Name", "SimObject instance name")
        if not instance:
            return
        so = SimObject(cname, instance)
        self.simobjects.append(so)
        self.sim_list.insert(tk.END, f"{cname} ({instance})")
        self._update_text()

    def _current_simobject(self) -> SimObject | None:
        sel = self.sim_list.curselection()
        if not sel:
            messagebox.showwarning("Select", "Select a SimObject")
            return None
        return self.simobjects[sel[0]]

    def _add_to_simobject(self) -> None:
        if not self.models_dir:
            return
        simobj = self._current_simobject()
        if not simobj:
            return
        for i in self.class_list.curselection():
            cls = self.class_list.get(i)
            header = self.class_header_map.get(cls)
            if header and header not in self.selected_headers:
                self.selected_headers.append(header)
                self.selected_list.insert(tk.END, f"##include \"{header}\"")
            var = simpledialog.askstring("Member Name", f"Variable name for {cls}")
            if not var:
                continue
            simobj.members.append((cls, var))
            # Ask for common job calls
            if messagebox.askyesno("Job", f"Add default_data job for {var}?"):
                simobj.jobs.append(("default_data", f"{var}.default_data()"))
            if messagebox.askyesno("Job", f"Add initialization job for {var}?"):
                simobj.jobs.append(("initialization", f"{var}.state_init()"))
            if messagebox.askyesno("Job", f"Add derivative job for {var}?"):
                simobj.jobs.append(("derivative", f"{var}.state_deriv()"))
            if messagebox.askyesno("Job", f"Add integration job for {var}?"):
                simobj.jobs.append(("integration", f"trick_ret = {var}.state_integ()"))
        self._update_text()

        for so in self.simobjects:
            lines.append("")
            lines.append(f"class {so.name} : public Trick::SimObject {{")
            lines.append("    public:")
            for cls, var in so.members:
                lines.append(f"        {cls} {var};")
            lines.append(f"        {so.name}() {{")
            for phase, call in so.jobs:
                lines.append(f"            (\"{phase}\") {call} ;")
            lines.append("        }")
            lines.append("};")
            lines.append(f"{so.name} {so.instance};")
            if header not in self.selected_headers:
                self.selected_headers.append(header)
                self.selected_list.insert(tk.END, f"##include \"{header}\"")
        self._update_text()


    def _update_class_list(self, _event: tk.Event | None = None) -> None:
        """Add classes from the currently selected headers to the list."""
        if not self.models_dir:
            return
        for i in self.header_list.curselection():
            header = self.headers[i]
            if header not in self.header_class_cache:
                self.header_class_cache[header] = parse_header_classes(
                    os.path.join(self.models_dir, header)
                )
            for cls in self.header_class_cache[header]:
                if cls not in self.class_header_map:
                    self.class_header_map[cls] = header
                    self.class_list.insert(tk.END, cls)

    def _add_classes(self) -> None:
        if not self.models_dir:
            return
        for i in self.class_list.curselection():
            cls = self.class_list.get(i)
            header = self.class_header_map.get(cls)
            if header and header not in self.selected_headers:
                self.selected_headers.append(header)
                self.selected_list.insert(tk.END, f"##include \"{header}\"")
            name = simpledialog.askstring("Instance Name", f"Instance name for {cls}")
            if name:
                self.selected_classes.append((cls, name))
                self.selected_list.insert(tk.END, f"{cls} {name} ;")

        self._update_text()

    def _update_text(self) -> None:
        lines: List[str] = []
        for h in self.selected_headers:
            lines.append(f"##include \"{h}\"")

        for cls, name in self.selected_classes:
            lines.append(f"{cls} {name} ;")

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
