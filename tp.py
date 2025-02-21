import tkinter as tk
from tkinter import PhotoImage, messagebox

def visualize_tables(seq1, seq2, match_score, mismatch_penalty, gap_penalty):
    
    m, n = len(seq1), len(seq2)
    score_matrix = [[0] * (n + 1) for _ in range(m + 1)]
    traceback_matrix = [[[] for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(1, m + 1):
        score_matrix[i][0] = i * gap_penalty
        traceback_matrix[i][0] = ["up"]
    for j in range(1, n + 1):
        score_matrix[0][j] = j * gap_penalty
        traceback_matrix[0][j] = ["left"]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_penalty)
            dell = score_matrix[i - 1][j] + gap_penalty
            ins = score_matrix[i][j - 1] + gap_penalty
            max_score = max(match, dell, ins)

            score_matrix[i][j] = max_score
            traceback_matrix[i][j] = []
            if max_score == match:
                traceback_matrix[i][j].append("diag")
            if max_score == dell:
                traceback_matrix[i][j].append("up")
            if max_score == ins:
                traceback_matrix[i][j].append("left")

    def trace_paths(i, j, current_path):
        if i == 0 and j == 0:
            paths.append(current_path[::-1])
            return
        for direction in traceback_matrix[i][j]:
            if direction == "diag":
                trace_paths(i - 1, j - 1, current_path + [(i, j, "diag")])
            elif direction == "up":
                trace_paths(i - 1, j, current_path + [(i, j, "up")])
            elif direction == "left":
                trace_paths(i, j - 1, current_path + [(i, j, "left")])

    paths = []
    trace_paths(m, n, [])

    alignments = []
    for path in paths:
       aligned_seq1, aligned_seq2 = [], []
       i, j = m, n  
       for (x, y, direction) in reversed(path):  
         if direction == "diag":
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append(seq2[j - 1])
            i, j = i - 1, j - 1
         elif direction == "up":
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append("-")
            i -= 1
         elif direction == "left":
            aligned_seq1.append("-")
            aligned_seq2.append(seq2[j - 1])
            j -= 1
   
       reversed_seq1 = "".join(aligned_seq1)[::-1]
       reversed_seq2 = "".join(aligned_seq2)[::-1]
       alignments.append((reversed_seq1, reversed_seq2 ))
       print("".join(aligned_seq1), "".join(aligned_seq2))
   
   
   ######## user interface ####################
    window = tk.Tk()
    window.title("Needleman-Wunsch Visualization: Full and Solution Tables")

   
    canvas = tk.Canvas(window, width=1000, height=700, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

   
    cell_size = 50
    offset_x1, offset_y = 100, 100  
    offset_x2 = offset_x1 + (n + 2) * cell_size + 50  

    
    canvas.create_text(offset_x1 + (n + 1) * cell_size / 2, offset_y - 30, text="Full Traceback Matrix\n\n", font=("Arial", 16, "bold"))
    for i in range(m + 1):
        for j in range(n + 1):
            x1 = offset_x1 + j * cell_size
            y1 = offset_y + i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")

            
            score = score_matrix[i][j]
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(score), font=("Arial", 12))

           
            for direction in traceback_matrix[i][j]:
                if direction == "diag":  
                    canvas.create_line((x1 + x2) / 2, (y1 + y2) / 2, x1, y1, arrow=tk.LAST, fill="gray")
                elif direction == "up": 
                    canvas.create_line((x1 + x2) / 2, (y1 + y2) / 2, (x1 + x2) / 2, y1, arrow=tk.LAST, fill="gray")
                elif direction == "left":  
                    canvas.create_line((x1 + x2) / 2, (y1 + y2) / 2, x1, (y1 + y2) / 2, arrow=tk.LAST, fill="gray")

   
    canvas.create_text(offset_x2 + (n + 1) * cell_size / 2, offset_y - 30, text="Solution Paths Only\n\n", font=("Arial", 16, "bold"))
    colors = ["red", "blue", "green", "purple", "orange"]  
    for i in range(m + 1):
        for j in range(n + 1):
            x1 = offset_x2 + j * cell_size
            y1 = offset_y + i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")

            
            score = score_matrix[i][j]
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(score), font=("Arial", 12))

   
    for idx, path in enumerate(paths):
        color = colors[idx % len(colors)]
        for (i, j, direction) in path:
            x_center = offset_x2 + j * cell_size + cell_size / 2
            y_center = offset_y + i * cell_size + cell_size / 2

            if direction == "diag":  
                x_end = x_center - cell_size / 2
                y_end = y_center - cell_size / 2
                canvas.create_line(x_center, y_center, x_end, y_end, arrow=tk.LAST, fill=color, width=2)
            elif direction == "up":  
                x_end = x_center
                y_end = y_center - cell_size / 2
                canvas.create_line(x_center, y_center, x_end, y_end, arrow=tk.LAST, fill=color, width=2)
            elif direction == "left":  
                x_end = x_center - cell_size / 2
                y_end = y_center
                canvas.create_line(x_center, y_center, x_end, y_end, arrow=tk.LAST, fill=color, width=2)

    
    for i, char in enumerate("-" + seq1):
        canvas.create_text(offset_x1 - cell_size / 2, offset_y + i * cell_size + cell_size / 2, text=char, font=("Arial", 14))
        canvas.create_text(offset_x2 - cell_size / 2, offset_y + i * cell_size + cell_size / 2, text=char, font=("Arial", 14))

    for j, char in enumerate("-" + seq2):
        canvas.create_text(offset_x1 + j * cell_size + cell_size / 2, offset_y - cell_size / 2, text=char, font=("Arial", 14))
        canvas.create_text(offset_x2 + j * cell_size + cell_size / 2, offset_y - cell_size / 2, text=char, font=("Arial", 14))
    
    optimal_score = score_matrix[m][n]
    
    result_text = f"{len(alignments)} optimal alignments:\n\n optimal score: {optimal_score}\n\n"
    for idx, (aligned_seq1, aligned_seq2) in enumerate(alignments, start=1):
        result_text += f"Alignment {idx}:\n{aligned_seq1}\n{aligned_seq2}\n\n"

    result_label = tk.Label(window, text=result_text, font=("Arial", 12), justify=tk.LEFT, bg="white")
    result_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True,padx=2)

  
    window.mainloop()


def open_visualization():
    try:
        seq1 = seq1_entry.get().strip()
        seq2 = seq2_entry.get().strip()
        match_score = int(match_entry.get())
        mismatch_penalty = int(mismatch_entry.get())
        gap_penalty = int(gap_entry.get())

        if not seq1 or not seq2:
            raise ValueError("Sequences cannot be empty.")

        root.destroy()  
        visualize_tables(seq1, seq2, match_score, mismatch_penalty, gap_penalty)

    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Error: {e}")


root = tk.Tk()
root.title("Needleman-Wunsch Input")
root.geometry("600x400")  
root.resizable(False, False)  

background_image = PhotoImage(file="adn1.pgm")  
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)  


tk.Label(root, text="Sequence 1:", font=("Arial", 18), bg="lightblue").grid(row=0, column=0, padx=10, pady=5)
seq1_entry = tk.Entry(root, font=("Arial", 18))
seq1_entry.grid(row=0, column=1, padx=10, pady=8)

tk.Label(root, text="Sequence 2:", font=("Arial", 18), bg="lightblue").grid(row=1, column=0, padx=10, pady=5)
seq2_entry = tk.Entry(root, font=("Arial", 18))
seq2_entry.grid(row=1, column=1, padx=10, pady=8)

tk.Label(root, text="Match ", font=("Arial", 18), bg="lightblue").grid(row=2, column=0, padx=10, pady=5)
match_entry = tk.Entry(root, font=("Arial", 18))
match_entry.insert(0, "1")  
match_entry.grid(row=2, column=1, padx=10, pady=8)

tk.Label(root, text="Mismatch :", font=("Arial", 18), bg="lightblue").grid(row=3, column=0, padx=10, pady=5)
mismatch_entry = tk.Entry(root, font=("Arial", 18))
mismatch_entry.insert(0, "-1")  
mismatch_entry.grid(row=3, column=1, padx=10, pady=8)

tk.Label(root, text="Gap :", font=("Arial", 18), bg="lightblue").grid(row=4, column=0, padx=10, pady=5)
gap_entry = tk.Entry(root, font=("Arial", 18))
gap_entry.insert(0, "-1")  
gap_entry.grid(row=4, column=1, padx=10, pady=8)

tk.Button(root, text="Visualize", font=("Arial", 18), command=open_visualization).grid(row=5, column=0, columnspan=2, pady=60)

root.mainloop()

