import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import numpy as np

class KernelFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Kernel Filter Lab")

        self.image = None
        self.gray_np = None
        self.filtered_np = None
        self.target_pos = [0, 0] # [y, x]

        # ---- レイアウト ----
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左パネル
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Button(left_frame, text="画像を読み込む", command=self.load_image).pack(pady=5)
        
        self.canvas_label = tk.Label(left_frame, text="Click to select pixel / Use Arrow Keys")
        self.canvas_label.pack()

        # 画像表示用のキャンバス（クリックイベント用）
        self.img_display = tk.Label(left_frame, bg="gray")
        self.img_display.pack(pady=5)
        self.img_display.bind("<Button-1>", self.on_canvas_click)
        
        # 矢印キーのバインド
        self.root.bind("<KeyPress>", self.on_key_press)

        # 右パネル
        right_frame = tk.Frame(main_frame, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # (1) Kernel 合計値表示
        self.sum_label = tk.Label(right_frame, text="Kernel Sum: 0.0", font=("Arial", 12, "bold"))
        self.sum_label.pack(pady=10)

        # カーネル入力
        tk.Label(right_frame, text="3x3 Kernel").pack()
        self.kernel_entries = []
        k_grid = tk.Frame(right_frame)
        k_grid.pack()
        for r in range(3):
            row = []
            for c in range(3):
                e = tk.Entry(k_grid, width=6, justify="center")
                e.grid(row=r, column=c, padx=2, pady=2)
                e.insert(0, "0")
                e.bind("<KeyRelease>", lambda e: self.update_all()) # 入力時に即更新
                row.append(e)
            self.kernel_entries.append(row)

        # プリセット
        self.presets = {
            "Identity": [[0,0,0],[0,1,0],[0,0,0]],
            "Box Blur": [[1/9]*3]*3,
            "Sharpen": [[0,-1,0],[-1,5,-1],[0,-1,0]],
            "Edge": [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]],
            "Emboss": [[-2,-1,0],[-1,1,1],[0,1,2]],
        }
        self.preset_var = tk.StringVar(value="Identity")
        self.preset_box = ttk.Combobox(right_frame, textvariable=self.preset_var, values=list(self.presets.keys()), state="readonly")
        self.preset_box.pack(pady=5)
        self.preset_box.bind("<<ComboboxSelected>>", self.on_preset_selected)

        # (2) 行列数値表示エリア
        tk.Frame(right_frame, height=2, bg="black").pack(fill=tk.X, pady=10)
        
        self.pos_label = tk.Label(right_frame, text="Position: (0, 0)")
        self.pos_label.pack()

        tk.Label(right_frame, text="Original Pixels (3x3)").pack(pady=(10,0))
        self.src_vals = self.create_val_grid(right_frame)

        tk.Label(right_frame, text="Filtered Pixels (3x3)").pack(pady=(10,0))
        self.dst_vals = self.create_val_grid(right_frame)

        self.set_kernel(self.presets["Identity"])

    def create_val_grid(self, parent):
        frame = tk.Frame(parent, bg="#ddd", padx=2, pady=2)
        frame.pack(pady=5)
        labels = []
        for r in range(3):
            row = []
            for c in range(3):
                l = tk.Label(frame, text="0", width=4, relief="sunken", bg="white")
                l.grid(row=r, column=c, padx=1, pady=1)
                row.append(l)
            labels.append(row)
        return labels

    def set_kernel(self, kernel):
        for r in range(3):
            for c in range(3):
                self.kernel_entries[r][c].delete(0, tk.END)
                self.kernel_entries[r][c].insert(0, f"{kernel[r][c]:.2f}")
        self.update_all()

    def get_kernel(self):
        kernel = np.zeros((3, 3))
        for r in range(3):
            for c in range(3):
                try: kernel[r,c] = float(self.kernel_entries[r][c].get())
                except: kernel[r,c] = 0
        return kernel

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            img = Image.open(path).convert("L")
            img.thumbnail((400, 400))
            self.gray_np = np.array(img, dtype=float)
            self.target_pos = [self.gray_np.shape[0]//2, self.gray_np.shape[1]//2]
            self.update_all()

    def update_all(self, event=None):
        if self.gray_np is None: return
        
        kernel = self.get_kernel()
        self.sum_label.config(text=f"Kernel Sum: {np.sum(kernel):.2f}")

        # 高速化のためScipy等の代わりに簡易実装(表示用なので)
        h, w = self.gray_np.shape
        padded = np.pad(self.gray_np, 1, mode='edge')
        
        # 画面全体をフィルタリング（本来は全体をやるが重い場合は周辺のみも可）
        # ここでは学習用に、表示を更新
        res = np.zeros_like(self.gray_np)
        # ※本来はループだと遅いが説明用コードの構造を維持
        # Pythonの最適化のため、必要な部分だけ計算する手法もありますが
        # ここでは全体を計算
        from scipy.signal import convolve2d
        self.filtered_np = convolve2d(self.gray_np, np.flip(kernel), mode='same', boundary='fill')
        self.filtered_np = np.clip(self.filtered_np, 0, 255)

        self.draw_ui_images()
        self.update_matrix_display()

    def draw_ui_images(self):
        # フィルタ後の画像を表示し、注視点に枠を描く
        display_img = Image.fromarray(self.filtered_np.astype(np.uint8)).convert("RGB")
        draw = ImageDraw.Draw(display_img)
        y, x = self.target_pos
        draw.rectangle([x-2, y-2, x+2, y+2], outline="red", width=2)
        
        tk_img = ImageTk.PhotoImage(display_img)
        self.img_display.image = tk_img
        self.img_display.config(image=tk_img)

    def update_matrix_display(self):
        y, x = self.target_pos
        self.pos_label.config(text=f"Position: (X={x}, Y={y})")
        
        h, w = self.gray_np.shape
        padded_src = np.pad(self.gray_np, 1, mode='constant')
        padded_dst = np.pad(self.filtered_np, 1, mode='constant')

        for r in range(3):
            for c in range(3):
                # 元画像の3x3 (y, xが中心)
                sv = padded_src[y+r, x+c]
                dv = padded_dst[y+r, x+c]
                self.src_vals[r][c].config(text=f"{int(sv)}")
                self.dst_vals[r][c].config(text=f"{int(dv)}")

    def on_canvas_click(self, event):
        self.target_pos = [event.y, event.x]
        self.update_all()

    def on_key_press(self, event):
        if self.gray_np is None: return
        step = 1
        if event.keysym == "Up":    self.target_pos[0] = max(0, self.target_pos[0]-step)
        if event.keysym == "Down":  self.target_pos[0] = min(self.gray_np.shape[0]-1, self.target_pos[0]+step)
        if event.keysym == "Left":  self.target_pos[1] = max(0, self.target_pos[1]-step)
        if event.keysym == "Right": self.target_pos[1] = min(self.gray_np.shape[1]-1, self.target_pos[1]+step)
        self.update_all()

    def on_preset_selected(self, event):
        self.set_kernel(self.presets[self.preset_var.get()])

if __name__ == "__main__":
    root = tk.Tk()
    app = KernelFilterApp(root)
    root.mainloop()