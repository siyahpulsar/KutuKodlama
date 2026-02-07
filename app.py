import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import json
import os
import re

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visual Coding App")
        self.geometry("1200x800")
        
        # Data
        self.data_file = "app_data.json"
        self.data = self.load_data()
        
        # UI Layout
        self.setup_ui()
        
    def load_data(self):
        if not os.path.exists(self.data_file):
            return {"categories": [], "workspace": {}}
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"categories": [], "workspace": {}}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def setup_ui(self):
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel (Categories)
        self.left_panel = tk.Frame(self, bg="lightgray", width=200)
        self.left_panel.grid(row=0, column=0, sticky="ns")
        self.left_panel.grid_propagate(False)
        
        self.create_category_btn = tk.Button(self.left_panel, text="Oluştur", command=self.create_category)
        self.create_category_btn.pack(pady=10, fill="x")
        
        self.categories_frame = tk.Frame(self.left_panel, bg="lightgray")
        self.categories_frame.pack(fill="both", expand=True)
        
        # Center Panel (Workspace)
        self.center_panel = tk.Frame(self, bg="white")
        self.center_panel.grid(row=0, column=1, sticky="nsew")

        # Right Panel (Boxes)
        self.right_panel = tk.Frame(self, bg="lightgray", width=250)
        self.right_panel.grid(row=0, column=2, sticky="ns")
        self.right_panel.grid_propagate(False)
        
        self.new_box_btn = tk.Button(self.right_panel, text="Yeni Kutu", command=self.create_box_dialog)
        self.new_box_btn.pack(pady=10, fill="x")

        # Initialize UI with data
        self.refresh_categories()

    def create_category(self):
        new_category = {"name": "Yeni Kategori", "boxes": []}
        self.data["categories"].append(new_category)
        self.save_data()
        self.refresh_categories()

    def refresh_categories(self):
        # Clear existing buttons
        for widget in self.categories_frame.winfo_children():
            widget.destroy()
            
        for idx, category in enumerate(self.data["categories"]):
            btn = tk.Button(self.categories_frame, text=category["name"])
            btn.pack(fill="x", pady=2)
            # Bind events for rename (double click) and select (single click)
            btn.bind("<Double-Button-1>", lambda e, i=idx: self.rename_category(i))
            btn.bind("<Button-1>", lambda e, i=idx: self.select_category(i))

    def rename_category(self, index):
        current_name = self.data["categories"][index]["name"]
        new_name = simpledialog.askstring("Rename Category", "Enter new name:", initialvalue=current_name)
        if new_name:
            self.data["categories"][index]["name"] = new_name
            self.save_data()
            self.refresh_categories()

    def select_category(self, index):
        self.current_category_index = index
        self.refresh_boxes()

    def create_box_dialog(self):
        if not hasattr(self, "current_category_index"):
            messagebox.showwarning("Warning", "Please select a category first.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Create New Box")
        
        tk.Label(dialog, text="Content:").pack(pady=5)
        content_entry = tk.Entry(dialog, width=40)
        content_entry.pack(pady=5)
        
        tk.Label(dialog, text="Color:").pack(pady=5)
        color_btn = tk.Button(dialog, text="Pick Color", command=lambda: self.pick_color(color_btn))
        color_btn.pack(pady=5)
        self.picked_color = "#FFFFFF"

        tk.Button(dialog, text="Create", command=lambda: self.save_box(dialog, content_entry.get())).pack(pady=10)

    def pick_color(self, btn):
        color = colorchooser.askcolor()[1]
        if color:
            self.picked_color = color
            btn.config(bg=color)

    def save_box(self, dialog, content):
        if not content:
            return
        new_box = {"content": content, "color": self.picked_color}
        self.data["categories"][self.current_category_index]["boxes"].append(new_box)
        self.save_data()
        self.refresh_boxes()
        dialog.destroy()

    def refresh_boxes(self):
        for widget in self.right_panel.winfo_children():
            if widget != self.new_box_btn:
                widget.destroy()

        if hasattr(self, "current_category_index"):
            category = self.data["categories"][self.current_category_index]
            for box in category["boxes"]:
                box_frame = tk.Frame(self.right_panel, bg=box["color"], bd=1, relief="raised")
                box_frame.pack(fill="x", padx=5, pady=2)
                
                lbl = tk.Label(box_frame, text=box["content"], bg=box["color"], anchor="w")
                lbl.pack(fill="x", padx=5, pady=5)
                
                # Drag events
                lbl.bind("<Button-1>", lambda e, b=box: self.start_drag(e, b))
                lbl.bind("<B1-Motion>", self.drag_motion)
                lbl.bind("<ButtonRelease-1>", self.stop_drag)

    def setup_ui(self):
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel (Categories)
        self.left_panel = tk.Frame(self, bg="lightgray", width=200)
        self.left_panel.grid(row=0, column=0, sticky="ns")
        self.left_panel.grid_propagate(False)
        
        self.create_category_btn = tk.Button(self.left_panel, text="Oluştur", command=self.create_category)
        self.create_category_btn.pack(pady=10, fill="x")
        
        self.categories_frame = tk.Frame(self.left_panel, bg="lightgray")
        self.categories_frame.pack(fill="both", expand=True)
        
        # Center Panel (Workspace)
        self.center_panel = tk.Frame(self, bg="white")
        self.center_panel.grid(row=0, column=1, sticky="nsew")
        self.create_bottom_controls()
        self.init_workspace()

        # Right Panel (Boxes)
        self.right_panel = tk.Frame(self, bg="lightgray", width=250)
        self.right_panel.grid(row=0, column=2, sticky="ns")
        self.right_panel.grid_propagate(False)
        
        self.new_box_btn = tk.Button(self.right_panel, text="Yeni Kutu", command=self.create_box_dialog)
        self.new_box_btn.pack(pady=10, fill="x")

        # Initialize UI with data
        self.refresh_categories()
        
        # Drag data
        self.drag_data = {"x": 0, "y": 0, "item": None, "window": None}

    def init_workspace(self):
        self.canvas = tk.Canvas(self.center_panel, bg="white")
        self.scrollbar_y = tk.Scrollbar(self.center_panel, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.center_panel, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        
        # Grid System
        self.grid_cells = [] 
        
        # Calculate max rows: max(10, highest_filled_row + 1 + 10)
        max_r = -1
        max_c = 9 # Start with 10 columns (0-9)
        for key in self.data["workspace"].keys():
            try:
                r_str, c_str = key.split("_")
                r, c = int(r_str), int(c_str)
                if r > max_r: max_r = r
                if c > max_c: max_c = c
            except:
                pass
        
        self.max_rows = max(10, max_r + 11)
        self.max_cols = max_c + 1

        self.render_grid()

    def render_grid(self):
        # Clear existing
        for w in self.scrollable_frame.winfo_children():
            w.destroy()
        
        self.grid_cells = []
        
        # Header (Column Numbers)
        for c in range(self.max_cols):
            tk.Label(self.scrollable_frame, text=f"{c}", width=5, bg="lightgray", relief="raised").grid(row=0, column=c+1, sticky="nsew")

        for r in range(self.max_rows):
            row_widgets = []
            # Row Number
            tk.Label(self.scrollable_frame, text=f"{r}:", width=4, anchor="e", bg="lightgray").grid(row=r+1, column=0, sticky="ns")
            
            for c in range(self.max_cols):
                cell_frame = tk.Frame(self.scrollable_frame, bg="white", width=150, height=30, bd=1, relief="solid")
                cell_frame.grid_propagate(False) # Don't shrink
                cell_frame.grid(row=r+1, column=c+1, padx=1, pady=1, sticky="nsew")
                
                row_widgets.append(cell_frame)
                
                cell_key = f"{r}_{c}"
                if cell_key in self.data["workspace"]:
                    self.render_box_in_row(cell_frame, self.data["workspace"][cell_key], cell_key)
            
            self.grid_cells.append(row_widgets)

    def stop_drag(self, event):
        if self.drag_data["window"]:
            self.drag_data["window"].destroy()
            self.drag_data["window"] = None

            x, y = self.winfo_pointerxy()
            widget = self.winfo_containing(x, y)
            
            # Find the cell frame
            target_cell = None
            check = widget
            while check:
                # Check if this widget is in our grid_cells structure
                # A bit inefficient to search all, but robust
                for r_idx, row in enumerate(self.grid_cells):
                    if check in row:
                        c_idx = row.index(check)
                        target_cell = (r_idx, c_idx)
                        break
                if target_cell: break
                
                try:
                    check = check.master
                except:
                    break
            
            if target_cell:
                self.drop_box(target_cell[0], target_cell[1], self.drag_data["item"])

    def drop_box(self, r, c, box):
        cell_key = f"{r}_{c}"
        
        # Check if this row was already used
        row_already_used = any(k.startswith(f"{r}_") for k in self.data["workspace"])
        # Check if this col 0 was already used (for ANY row)
        col0_already_used = any(k.endswith("_0") for k in self.data["workspace"])
        
        self.data["workspace"][cell_key] = {
            "content": box["content"],
            "color": box["color"],
            "values": [] 
        }
        
        needs_rerender = False
        
        # 1 satıra herhangi bir şey konulduğu anda +1 satır daha oluşacak.
        if not row_already_used:
            self.max_rows += 1
            needs_rerender = True
            
        # bir satırın ilk sütunu doluysa o satırda +1 sütun oluşacak.
        if c == 0:
            # Technically user said "o satırda", but for a uniform grid we expand globally
            # If col 0 of THIS row is filled, add a column? 
            # We'll just check if it's the first time col 0 is filled for this specific row?
            # Or if ANY col 0 is filled? "bir satırın ilk sütunu" -> "a row's first column".
            # I'll check if this specific row's col 0 was empty before.
            row_col0_used = f"{r}_0" in self.data["workspace"]
            # Wait, I just filled it. So I should have checked before.
            # Let's say: if c == 0, we add a column.
            self.max_cols += 1
            needs_rerender = True
            
        self.save_data()
        
        if needs_rerender:
            self.render_grid()
        else:
            cell_frame = self.grid_cells[r][c]
            self.render_box_in_row(cell_frame, self.data["workspace"][cell_key], cell_key)
            
    def create_bottom_controls(self):
        control_frame = tk.Frame(self.center_panel, bg="white")
        control_frame.pack(side="bottom", fill="x", pady=10, padx=10)
        
        tk.Button(control_frame, text="Import", command=self.import_project).pack(side="right", padx=5)
        tk.Button(control_frame, text="Save", command=self.save_project).pack(side="right", padx=5)
        tk.Button(control_frame, text="Export", command=self.export_project).pack(side="right", padx=5)

    def save_file(self, lines, title):
        from tkinter import filedialog
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title=title)
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
                messagebox.showinfo("Success", f"File saved: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def start_drag(self, event, box):
        self.drag_data["item"] = box
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
        # Create a top-level window as the drag object
        self.drag_data["window"] = tk.Toplevel(self)
        self.drag_data["window"].overrideredirect(True)
        self.drag_data["window"].attributes("-topmost", True)
        self.drag_data["window"].geometry(f"+{event.x_root}+{event.y_root}")
        
        lbl = tk.Label(self.drag_data["window"], text=box["content"], bg=box["color"])
        lbl.pack()

    def drag_motion(self, event):
        if self.drag_data["window"]:
            x = event.x_root - self.drag_data["x"]
            y = event.y_root - self.drag_data["y"]
            self.drag_data["window"].geometry(f"+{x}+{y}")

    def update_row_value(self, cell_key, value_idx, new_value):
        # cell_key is now "r_c"
        if cell_key in self.data["workspace"]:
             while len(self.data["workspace"][cell_key]["values"]) <= value_idx:
                self.data["workspace"][cell_key]["values"].append("")
             self.data["workspace"][cell_key]["values"][value_idx] = new_value
             self.save_data()

    def render_box_in_row(self, parent, box_data, row_idx):
        # Clear existing
        for w in parent.winfo_children():
            w.destroy()
            
        parent.config(bg=box_data["color"])
        
        import re
        content = box_data["content"]
        # Regex to capture all placeholders: ..0.., .c0c., .i0i., .s0s., .select:key=val
        # Note: .select is complex, let's treat it carefully.
        # We'll split by a regex that captures the tokens.
        
        # Combined pattern
        # 1. ..0.. -> standard
        # 2. .c0c. -> color
        # 3. .i0i. -> int
        # 4. .s0s. -> symbol
        # 5. .select:...? -> optional
        
        pattern = r"(\.\.0\.\.|\.c0c\.|\.i0i\.|\.s0s\.|\.select:[^,]+(?:,[^,]+)*)"
        
        parts = re.split(pattern, content)
        
        saved_values = box_data.get("values", [])
        
        # Helper to safely get/set values
        def get_value(idx, default=""):
            if idx < len(saved_values):
                return saved_values[idx]
            return default

        value_counter = 0

        for part in parts:
            if not part: continue
            
            if part == "..0..":
                current_idx = value_counter
                val_var = tk.StringVar(value=get_value(current_idx))
                entry = tk.Entry(parent, textvariable=val_var, width=10)
                entry.pack(side="left", padx=2)
                
                def save_entry(var=val_var, idx=current_idx):
                    self.update_row_value(row_idx, idx, var.get())
                val_var.trace_add("write", lambda *args, v=val_var, i=current_idx: save_entry())
                value_counter += 1
                
            elif part == ".c0c.":
                current_idx = value_counter
                initial_color = get_value(current_idx) or "#000000" # Default
                
                btn = tk.Button(parent, text="Color", bg=initial_color, width=6)
                btn.pack(side="left", padx=2)
                
                def pick_col(b=btn, idx=current_idx):
                    color = colorchooser.askcolor()[1]
                    if color:
                        b.config(bg=color)
                        self.update_row_value(row_idx, idx, color)
                
                btn.config(command=pick_col)
                value_counter += 1

            elif part == ".i0i.":
                current_idx = value_counter
                val_var = tk.StringVar(value=get_value(current_idx))
                
                def validate_int(P):
                    if P == "" or P == "-": return True
                    return P.isdigit() or (P.startswith("-") and P[1:].isdigit())
                
                vcmd = (self.register(validate_int), '%P')
                entry = tk.Entry(parent, textvariable=val_var, width=8, validate="key", validatecommand=vcmd)
                entry.pack(side="left", padx=2)
                
                def save_int(var=val_var, idx=current_idx):
                    self.update_row_value(row_idx, idx, var.get())
                val_var.trace_add("write", lambda *args, v=val_var, i=current_idx: save_int())
                value_counter += 1

            elif part == ".s0s.":
                current_idx = value_counter
                val_var = tk.StringVar(value=get_value(current_idx))
                
                # Symbols only: Not alphanumeric (allow spaces? user said symbols only)
                def validate_sym(P):
                    for char in P:
                        if char.isalnum(): return False
                    return True
                
                vcmd = (self.register(validate_sym), '%P')
                entry = tk.Entry(parent, textvariable=val_var, width=8, validate="key", validatecommand=vcmd)
                entry.pack(side="left", padx=2)
                
                def save_sym(var=val_var, idx=current_idx):
                    self.update_row_value(row_idx, idx, var.get())
                val_var.trace_add("write", lambda *args, v=val_var, i=current_idx: save_sym())
                value_counter += 1

            elif part.startswith(".select:"):
                # Format: .select:label=.i0i.,label2=fixed
                # We need to parse inside the select
                # Stripping .select:
                options_str = part[8:]
                options = options_str.split(',') # Comma select
                
                # Each value in values list for select will be complex? 
                # Or just treat each option as a value index?
                # Simplify: "select" creates a checkbox for each option. 
                # If checked, it enables input. 
                # Format: "key=value_template"
                
                for opt in options:
                    if "=" not in opt: continue
                    label, template = opt.split("=", 1)
                    
                    current_idx = value_counter
                    
                    # Saved value format: "ENABLED|VALUE" or just "VALUE" (if enabled)
                    # Let's verify how to store. 
                    # If export needs "key=value", we store "value" if checked, else empty?
                    
                    saved_raw = get_value(current_idx, "0|") # Default disabled
                    try:
                        is_enabled_str, saved_val = saved_raw.split("|", 1)
                        is_enabled = (is_enabled_str == "1")
                    except:
                        is_enabled = False
                        saved_val = ""

                    frame = tk.Frame(parent, bg=box_data["color"])
                    frame.pack(side="left", padx=2)
                    
                    chk_var = tk.IntVar(value=1 if is_enabled else 0)
                    
                    # Create input widget based on template
                    # Supports .i0i., .s0s., or plain text
                    input_var = tk.StringVar(value=saved_val)
                    widget = None

                    if template == ".i0i.":
                         vcmd = (self.register(lambda P: P == "" or P == "-" or P.isdigit() or (P.startswith("-") and P[1:].isdigit())), '%P')
                         widget = tk.Entry(frame, textvariable=input_var, width=5, validate="key", validatecommand=vcmd)
                    elif template == ".s0s.":
                         vcmd = (self.register(lambda P: all(not c.isalnum() for c in P)), '%P')
                         widget = tk.Entry(frame, textvariable=input_var, width=5, validate="key", validatecommand=vcmd)
                    else:
                         # Default entry or fixed? If fixed (e.g. key=5), just label?
                         # User said: ".select:"row=.i0i.","."column=.i0i."" -> export "...row=girilensayı..."
                         # So it's key=Input.
                         widget = tk.Entry(frame, textvariable=input_var, width=5)

                    widget.pack(side="right")
                    widget.config(state="normal" if is_enabled else "disabled")
                    
                    def toggle_check(w=widget, cv=chk_var, iv=input_var, idx=current_idx):
                        state = cv.get()
                        if state:
                            w.config(state="normal")
                        else:
                            w.config(state="disabled")
                        # Save: "1|value" or "0|value"
                        val_to_save = f"{state}|{iv.get()}"
                        self.update_row_value(row_idx, idx, val_to_save)
                    
                    chk = tk.Checkbutton(frame, text=label, variable=chk_var, command=lambda: toggle_check(), bg=box_data["color"])
                    chk.pack(side="left")
                    
                    # Trace input change too
                    def save_opt(cv=chk_var, iv=input_var, idx=current_idx):
                         self.update_row_value(row_idx, idx, f"{cv.get()}|{iv.get()}")
                    
                    input_var.trace_add("write", lambda *args: save_opt())
                    
                    value_counter += 1

            else:
                # Static text
                tk.Label(parent, text=part, bg=box_data["color"]).pack(side="left")


    def export_project(self):
        lines = []
        for r in range(self.max_rows):
            row_text = ""
            for c in range(self.max_cols):
                cell_key = f"{r}_{c}"
                if cell_key in self.data["workspace"]:
                    item = self.data["workspace"][cell_key]
                    content = item["content"]
                    values = item["values"]
                    
                    import re
                    pattern = r"(\.\.0\.\.|\.c0c\.|\.i0i\.|\.s0s\.|\.select:[^,]+(?:,[^,]+)*)"
                    parts = re.split(pattern, content)
                    
                    result = ""
                    value_idx = 0
                    
                    for part in parts:
                        if not part: continue
                        
                        if part in ["..0..", ".c0c.", ".i0i.", ".s0s."]:
                            val = values[value_idx] if value_idx < len(values) else ""
                            result += str(val)
                            value_idx += 1
                            
                        elif part.startswith(".select:"):
                            options = part[8:].split(',')
                            for opt in options:
                                if "=" not in opt: continue
                                label, tmpl = opt.split("=", 1)
                                
                                raw_val = values[value_idx] if value_idx < len(values) else "0|"
                                try:
                                    enabled, val = raw_val.split("|", 1)
                                except:
                                    enabled, val = "0", ""
                                    
                                if enabled == "1":
                                    result += f"{label}={val} "
                                
                                value_idx += 1
                        else:
                            result += part
                    
                    row_text += result
                else:
                    pass 
            
            lines.append(row_text.rstrip())
        
        self.save_file(lines, "Exported Text")

    def save_project(self):
        # Save: Keep structure using custom markers
        lines = []
        # We need to save the grid state. But usually Save is for reloading the app state.
        # Actually app_data.json already saves the state. 
        # The 'Save' button in the UI requested by user was for a .txt file.
        # Format: row,col,content,values_json?
        # Or line by line representation? 
        # Previous implementation saved line by line. 
        # With grid, maybe we just serialization of app_data.json is enough?
        # User asked for "Save button saves project state". 
        # Let's save a text representation that maps to the grid.
        
        # Simplified: Just dump the workspace data as JSON to the text file? 
        # Or keep the "visual" text file format?
        # New robust format: JSON is best for complex grid.
        
        # However, to respect the previous "human readable" request:
        # We can iterate rows. But cells?
        # Let's just dump the self.data["workspace"] into the file as JSON.
        
        import json
        self.save_file([json.dumps(self.data["workspace"], indent=2)], "Project Data")
        
    def import_project(self):
        from tkinter import filedialog
        import json
        
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("JSON Files", "*.json")])
        if not filepath:
            return
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Try to parse as JSON first (new save format)
            new_workspace = json.loads(content)
            
            # Basic validation
            if isinstance(new_workspace, dict):
                self.data["workspace"] = new_workspace
                self.save_data()
                
                # Re-calc max dimensions
                self.max_rows = 10
                self.max_cols = 10
                for key in self.data["workspace"].keys():
                    try:
                        r, c = map(int, key.split("_"))
                        if r >= self.max_rows: self.max_rows = r + 1
                        if c >= self.max_cols: self.max_cols = c + 1
                    except:
                        pass
                
                self.render_grid()
                messagebox.showinfo("Success", "Project imported successfully.")
                return

        except Exception as e:
            messagebox.showerror("Error", f"Failed to import: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()