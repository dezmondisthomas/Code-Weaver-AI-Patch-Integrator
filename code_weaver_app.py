import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import re
import os
import shutil
from datetime import datetime
import json
import ttkbootstrap as ttk # Import the modern library

# --- CONFIGURATION ---
ARCHIVE_FOLDER = 'archive'

# ===================================================================================
# BACKEND LOGIC (The engine from our previous script - unchanged)
# ===================================================================================
def parse_file_into_blocks(file_content, block_start_keyword='function'):
    blocks = {}
    block_pattern = re.compile(rf'{block_start_keyword}\s+([a-zA-Z0-9_]+)\s*.*?{{')
    first_block_match = block_pattern.search(file_content)
    if not first_block_match:
        return file_content, {}
    header = file_content[:first_block_match.start()]
    matches = list(block_pattern.finditer(file_content))
    for i, match in enumerate(matches):
        block_name = match.group(1)
        start_index = match.end()
        brace_count = 1
        current_pos = start_index
        while brace_count > 0 and current_pos < len(file_content):
            if file_content[current_pos] == '{':
                brace_count += 1
            elif file_content[current_pos] == '}':
                brace_count -= 1
            current_pos += 1
        end_index = current_pos
        full_block_text = file_content[match.start():end_index]
        blocks[block_name] = full_block_text
    return header, blocks

def integrate_code(master_content, patch_content):
    master_header, master_blocks = parse_file_into_blocks(master_content)
    patch_header, patch_blocks = parse_file_into_blocks(patch_content)
    
    final_code = patch_header if patch_header.strip() else master_header
    
    master_block_order = [match.group(1) for match in re.finditer(r'function\s+([a-zA-Z0-9_]+)', master_content)]

    for block_name in master_block_order:
        if block_name in patch_blocks and '/* Unchanged */' not in patch_blocks[block_name]:
            final_code += patch_blocks[block_name] + "\n\n"
        elif block_name in master_blocks:
            final_code += master_blocks[block_name] + "\n\n"
            
    return final_code.strip()

# ===================================================================================
# GUI APPLICATION CLASS (Rebuilt with ttkbootstrap)
# ===================================================================================

class CodeWeaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Weaver 2.0")
        self.root.geometry("1400x850")

        # --- Main Paned Window for Layout ---
        # FIX: Removed invalid 'sashwidth' option
        main_pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        main_pane.pack(fill='both', expand=True, padx=10, pady=10)

        # --- Left Side: Input Frame ---
        input_frame = ttk.Frame(main_pane, padding=10)
        
        # Notebook for switching between input methods
        input_notebook = ttk.Notebook(input_frame)
        input_notebook.pack(fill='both', expand=True)
        
        editor_frame = ttk.Frame(input_notebook, padding=5)
        self.create_editor_view(editor_frame)
        input_notebook.add(editor_frame, text="   Paste Code   ")
        
        file_path_frame = ttk.Frame(input_notebook, padding=10)
        self.create_filepath_view(file_path_frame)
        input_notebook.add(file_path_frame, text="   Select Files   ")
        
        main_pane.add(input_frame)

        # --- Right Side: Result Frame ---
        result_frame = ttk.Frame(main_pane, padding=10)
        ttk.Label(result_frame, text="Integrated Code (Result)", font="-size 12 -weight bold").pack(anchor='w', pady=(0, 5))
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, state='disabled', relief="solid", bd=1)
        self.result_text.pack(fill='both', expand=True)
        main_pane.add(result_frame)
        
        # --- Bottom Frame for Actions ---
        action_frame = ttk.Frame(root, padding=(10, 0, 10, 10))
        action_frame.pack(fill='x')

        self.integrate_button = ttk.Button(action_frame, text="Integrate & Preview", command=self.run_integration_process, bootstyle="primary")
        self.integrate_button.pack(side='left', padx=(0, 10))
        
        self.copy_button = ttk.Button(action_frame, text="Copy Result to Clipboard", command=self.copy_to_clipboard, state='disabled', bootstyle="success")
        self.copy_button.pack(side='left')
        
        self.status_var = tk.StringVar(value="Ready. Paste your code or select files to begin.")
        ttk.Label(action_frame, textvariable=self.status_var, font="-size 9 -slant italic").pack(side='right')

    def create_editor_view(self, parent_frame):
        # FIX: Removed invalid 'sashwidth' option
        editor_pane = ttk.PanedWindow(parent_frame, orient=tk.HORIZONTAL)
        editor_pane.pack(fill='both', expand=True, pady=5)

        master_editor_frame = ttk.Frame(editor_pane)
        ttk.Label(master_editor_frame, text="Master/Original Code").pack(anchor='w')
        self.master_text_editor = scrolledtext.ScrolledText(master_editor_frame, wrap=tk.WORD, relief="solid", bd=1)
        self.master_text_editor.pack(fill='both', expand=True, pady=(5,0))
        editor_pane.add(master_editor_frame)
        
        patch_editor_frame = ttk.Frame(editor_pane)
        ttk.Label(patch_editor_frame, text="Patch/Update Code").pack(anchor='w')
        self.patch_text_editor = scrolledtext.ScrolledText(patch_editor_frame, wrap=tk.WORD, relief="solid", bd=1)
        self.patch_text_editor.pack(fill='both', expand=True, pady=(5,0))
        editor_pane.add(patch_editor_frame)

    def create_filepath_view(self, parent_frame):
        ttk.Label(parent_frame, text="Master/Original File:").grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.master_path_var = tk.StringVar()
        ttk.Entry(parent_frame, textvariable=self.master_path_var).grid(row=0, column=1, sticky='ew')
        ttk.Button(parent_frame, text="Browse...", command=self.browse_master, bootstyle="secondary-outline").grid(row=0, column=2, padx=5)

        ttk.Label(parent_frame, text="Patch/Update File:").grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.patch_path_var = tk.StringVar()
        ttk.Entry(parent_frame, textvariable=self.patch_path_var).grid(row=1, column=1, sticky='ew')
        ttk.Button(parent_frame, text="Browse...", command=self.browse_patch, bootstyle="secondary-outline").grid(row=1, column=2, padx=5)
        
        parent_frame.grid_columnconfigure(1, weight=1)

    def browse_master(self):
        filepath = filedialog.askopenfilename(title="Select Master File", filetypes=[("All files", "*.*")])
        if filepath:
            self.master_path_var.set(filepath)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.master_text_editor.delete(1.0, tk.END)
                    self.master_text_editor.insert(tk.END, f.read())
            except Exception as e:
                messagebox.showerror("File Read Error", f"Could not read master file: {e}")

    def browse_patch(self):
        filepath = filedialog.askopenfilename(title="Select Patch File", filetypes=[("All files", "*.*")])
        if filepath:
            self.patch_path_var.set(filepath)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.patch_text_editor.delete(1.0, tk.END)
                    self.patch_text_editor.insert(tk.END, f.read())
            except Exception as e:
                messagebox.showerror("File Read Error", f"Could not read patch file: {e}")
    
    def run_integration_process(self):
        master_content = self.master_text_editor.get(1.0, tk.END).strip()
        patch_content = self.patch_text_editor.get(1.0, tk.END).strip()

        if not master_content or not patch_content:
            messagebox.showerror("Error", "Both 'Master' and 'Patch' code areas must contain code.")
            return

        self.update_status("Integrating...")
        self.root.update_idletasks()

        try:
            final_code = integrate_code(master_content, patch_content)
            
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, final_code)
            self.result_text.config(state='disabled')
            
            self.copy_button.config(state='normal')
            self.update_status("SUCCESS! Integration complete.")
            
        except Exception as e:
            self.update_status(f"ERROR: {e}")
            messagebox.showerror("Integration Error", f"An error occurred during integration: {e}")

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_text.get(1.0, tk.END))
        self.update_status("Result copied to clipboard!")
        
    def update_status(self, text):
        self.status_var.set(text)


if __name__ == '__main__':
    # Using the "superhero" theme from ttkbootstrap for a modern, dark look
    root = ttk.Window(themename="superhero")
    app = CodeWeaverApp(root)
    root.mainloop()