import tkinter as tk
from tkinter import Canvas, Frame, Entry, Button, Scrollbar

class SimpleCanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Test App")

        # Top panel with entry and buttons
        self.top_panel = Frame(self.root)
        self.top_panel.pack()

        self.entry = Entry(self.top_panel, width=10)
        self.entry.pack(side=tk.LEFT)

        self.draw_btn = Button(self.top_panel, text="Draw", command=self.draw_circle)
        self.draw_btn.pack(side=tk.LEFT)

        self.clear_btn = Button(self.top_panel, text="Clear", command=self.clear_canvas)
        self.clear_btn.pack(side=tk.LEFT)

        # Canvas with scrollbar
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = Canvas(self.canvas_frame, width=800, height=600, bg="white", scrollregion=(0, 0, 1600, 1200))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Position tracker for drawing
        self.x = 100
        self.y = 100

    def draw_circle(self):
        try:
            r = int(self.entry.get())
            self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill="lightblue")
            self.canvas.create_text(self.x, self.y, text=str(r))
            self.y += 2 * r + 20  # move down for next shape
        except ValueError:
            pass

    def clear_canvas(self):
        self.canvas.delete("all")
        self.y = 100

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleCanvasApp(root)
    root.mainloop()
