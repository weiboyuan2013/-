import tkinter as tk

def create_gui():
    root = tk.Tk()
    root.title("比赛计分系统")
    root.geometry("500x250")  # 扩大窗口尺寸
    
    # 初始化分数
    scores = {
        "team1": tk.IntVar(value=0),
        "team2": tk.IntVar(value=0)
    }

    def update_score(team, delta):
        new_score = scores[team].get() + delta
        if new_score >= 0:
            scores[team].set(new_score)

    # 左侧队伍信息
    team1_frame = tk.LabelFrame(root, text="队伍一")
    team1_frame.grid(row=0, column=0, padx=20, pady=10)
    
    # 原有名称输入框
    tk.Label(team1_frame, text="名称：").pack()
    team1_entry = tk.Entry(team1_frame)
    team1_entry.pack()
    
    # 新增分数显示和按钮
    tk.Label(team1_frame, text="分数", font=("Arial", 12)).pack(pady=5)
    tk.Label(team1_frame, textvariable=scores["team1"], 
            font=("Arial", 24, "bold")).pack()
    btn_frame = tk.Frame(team1_frame)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="-", command=lambda: update_score("team1", -1), 
            width=4).pack(side=tk.LEFT, padx=2)
    tk.Button(btn_frame, text="+", command=lambda: update_score("team1", 1), 
            width=4).pack(side=tk.LEFT, padx=2)

    # 右侧队伍信息（结构同左侧）
    team2_frame = tk.LabelFrame(root, text="队伍二")
    team2_frame.grid(row=0, column=1, padx=20, pady=10)
    
    tk.Label(team2_frame, text="名称：").pack()
    team2_entry = tk.Entry(team2_frame)
    team2_entry.pack()
    
    # 新增分数显示和按钮
    tk.Label(team2_frame, text="分数", font=("Arial", 12)).pack(pady=5)
    tk.Label(team2_frame, textvariable=scores["team2"], 
            font=("Arial", 24, "bold")).pack()
    btn_frame = tk.Frame(team2_frame)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="-", command=lambda: update_score("team2", -1), 
            width=4).pack(side=tk.LEFT, padx=2)
    tk.Button(btn_frame, text="+", command=lambda: update_score("team2", 1), 
            width=4).pack(side=tk.LEFT, padx=2)

    root.mainloop()

if __name__ == "__main__":
    create_gui()