import tkinter as tk
from tkinter import ttk, messagebox

class AdvancedSportsScorer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("运动会记分系统")
        self.window.geometry("800x600")
        
        # 项目配置字典
        self.sports_config = {
            "跑步": {"unit": "秒", "reverse": False},
            "跳绳": {"unit": "次", "reverse": True},
            "仰卧起坐": {"unit": "次", "reverse": True},
            "实心球": {"unit": "米", "reverse": True},
            "团体速度": {"unit": "秒", "reverse": False}
        }
        
        # 初始化数据结构
        self.records = {sport: {} for sport in self.sports_config}
        self.current_sport = tk.StringVar(value="跑步")
        
        self.create_widgets()
        self.update_rankings()
        self.window.mainloop()

    def create_widgets(self):
        # 主布局容器
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 左侧输入面板
        left_panel = tk.Frame(main_frame)
        self.create_input_panel(left_panel)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        # 右侧排行榜面板
        right_panel = tk.Frame(main_frame)
        self.create_ranking_panel(right_panel)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 底部功能区
        self.create_info_button()

    def create_input_panel(self, parent):
        """创建输入控制面板"""
        input_frame = tk.LabelFrame(parent, text="成绩录入")
        
        # 项目选择按钮组
        sport_selector = tk.Frame(input_frame)
        for idx, sport in enumerate(self.sports_config):
            btn = tk.Radiobutton(sport_selector, 
                               text=sport,
                               variable=self.current_sport,
                               value=sport,
                               command=self.update_input_labels)
            btn.grid(row=idx//3, column=idx%3, padx=5, pady=2)
        sport_selector.pack(pady=10)

        # 动态输入标签
        self.input_labels = tk.Frame(input_frame)
        self.team_label = tk.Label(self.input_labels, text="团队名称：")
        self.name_label = tk.Label(self.input_labels, text="选手姓名：")
        self.value_label = tk.Label(self.input_labels)
        self.team_entry = tk.Entry(self.input_labels)
        self.name_entry = tk.Entry(self.input_labels)
        self.value_entry = tk.Entry(self.input_labels)
        self.input_labels.pack(pady=10)

        # 按钮组
        btn_frame = tk.Frame(input_frame)
        tk.Button(btn_frame, text="提交成绩", command=self.submit_score).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="完成录入", command=self.show_final_rank).pack(side=tk.LEFT, padx=5)
        btn_frame.pack(pady=10)

        input_frame.pack(fill=tk.Y)

    def create_ranking_panel(self, parent):
        """创建排行榜面板"""
        rank_frame = tk.LabelFrame(parent, text="实时排行榜")
        
        # 带滚动条表格
        container = tk.Frame(rank_frame)
        canvas = tk.Canvas(container, height=400)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.tree = ttk.Treeview(canvas, columns=("排名", "名称", "成绩"), show="headings")
        
        # 配置滚动区域
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0,0), window=self.tree, anchor="nw")
        
        # 布局组件
        self.tree.heading("排名", text="排名")
        self.tree.heading("名称", text="名称")
        self.tree.heading("成绩", text="成绩")
        container.pack(fill=tk.BOTH, expand=True)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        rank_frame.pack(fill=tk.BOTH, expand=True)

    def update_input_labels(self):
        """根据所选项目更新输入提示"""
        sport = self.current_sport.get()
        config = self.sports_config[sport]

        # 清空旧组件
        for widget in self.input_labels.winfo_children():
            widget.pack_forget()

        # 团体项目显示团队输入框
        if sport == "团体速度":
            self.team_label.pack(side=tk.TOP, fill=tk.X)
            self.team_entry.pack(side=tk.TOP, fill=tk.X)
        else:
            self.team_label.pack_forget()
            self.team_entry.pack_forget()

        # 通用输入项
        self.name_label.pack(side=tk.TOP, fill=tk.X)
        self.name_entry.pack(side=tk.TOP, fill=tk.X)
        self.value_label.config(text=f"成绩（{config['unit']}）:")
        self.value_label.pack(side=tk.TOP, fill=tk.X)
        self.value_entry.pack(side=tk.TOP, fill=tk.X)

    def submit_score(self):
        """处理成绩提交"""
        sport = self.current_sport.get()
        name = self.name_entry.get()
        value = self.value_entry.get()
        
        try:
            # 数值验证
            value = float(value)
            if value <= 0:
                raise ValueError("成绩必须大于0")

            # 团体项目处理
            if sport == "团体速度":
                team = self.team_entry.get()
                if not team:
                    raise ValueError("必须填写团队名称")
                identifier = f"{team} - {name}"
            else:
                identifier = name

            # 存储记录
            self.records[sport][identifier] = value
            self.clear_inputs()
            self.update_rankings()
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))

    def clear_inputs(self):
        """清空所有输入框"""
        self.team_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

    def update_rankings(self):
        """更新排行榜数据"""
        for child in self.tree.get_children():
            self.tree.delete(child)
            
        sport = self.current_sport.get()
        config = self.sports_config[sport]
        sorted_items = sorted(self.records[sport].items(),
                             key=lambda x: x[1],
                             reverse=config["reverse"])
        
        for rank, (name, score) in enumerate(sorted_items[:10], 1):
            self.tree.insert("", tk.END, values=(
                rank,
                name,
                f"{score}{config['unit']}"
            ))

    def show_final_rank(self):
        """显示完整排名"""
        sport = self.current_sport.get()
        config = self.sports_config[sport]
        sorted_data = sorted(self.records[sport].items(),
                           key=lambda x: x[1],
                           reverse=config["reverse"])
        
        result = f"【{sport}项目最终排名】\n"
        for idx, (name, score) in enumerate(sorted_data, 1):
            result += f"{idx}. {name}: {score}{config['unit']}\n"
            if idx >= 20:  # 显示前20名
                break
        
        popup = tk.Toplevel()
        popup.title("最终排名")
        tk.Label(popup, text=result, justify=tk.LEFT, font=("宋体", 12)).pack(padx=20, pady=20)
        tk.Button(popup, text="导出结果", command=lambda: self.export_data(sport)).pack(pady=10)

    def create_info_button(self):
        """创建底部功能区"""
        footer = tk.Frame(self.window)
        tk.Button(footer, text="系统说明", command=self.show_info).pack(side=tk.LEFT, padx=10)
        tk.Button(footer, text="数据重置", command=self.reset_data).pack(side=tk.LEFT, padx=10)
        footer.pack(side=tk.BOTTOM, pady=10)

    def show_info(self):
        """显示系统信息"""
        info_text = """运动会记分系统功能说明：
        
1. 支持5种比赛项目：
   - 跑步（计时赛）
   - 跳绳（计数赛）
   - 仰卧起坐（计数赛）
   - 实心球（测距赛）
   - 团体速度（团队计时赛）
2. 每个项目的成绩录入方式：
   - 跑步：输入跑步时间（秒）
   - 跳绳：输入跳绳次数（次）
   - 仰卧起坐：输入仰卧起坐次数（次）
版本：v1.0.0
感谢您的使用！
作者：韦博源
"""
        
        messagebox.showinfo("系统信息", info_text)

    def reset_data(self):
        """重置所有数据"""
        if messagebox.askyesno("确认", "确定要清空所有比赛数据吗？"):
            for sport in self.records:
                self.records[sport].clear()
            self.update_rankings()

    def export_data(self, sport):
        """导出数据到文件"""
        with open(f"{sport}_成绩.txt", "w", encoding="utf-8") as f:
            f.write(f"{sport}项目成绩单\n")
            f.write("排名\t名称\t成绩\n")
            config = self.sports_config[sport]
            sorted_data = sorted(self.records[sport].items(),
                               key=lambda x: x[1],
                               reverse=config["reverse"])
            for idx, (name, score) in enumerate(sorted_data, 1):
                f.write(f"{idx}\t{name}\t{score}{config['unit']}\n")
        messagebox.showinfo("导出成功", f"{sport}数据已保存到当前目录")

if __name__ == "__main__":
    AdvancedSportsScorer()
