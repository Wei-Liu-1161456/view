import tkinter as tk
from tkinter import ttk

class ValidatedSpinbox(ttk.Spinbox):
    def __init__(self, *args, from_=1, to=100, **kwargs):
        """
        初始化带验证的 Spinbox。支持整数和浮点数模式，最大值默认为 100。
        """
        super().__init__(*args, from_=from_, to=to, **kwargs)
        
        # 默认属性
        self._model = 'float'  # 模式：'int' 表示正整数, 'float' 表示最多一位小数
        self.max_value = to    # 最大值（可以在初始化时动态设置）
        self.int_min = from_   # 整数模式下的最小值
        self.float_min = 0.1   # 浮点模式下的最小值
        self.default_value = from_  # 默认初始值为起始值

        # 配置验证命令
        self.configure(validate='key', validatecommand=(self.register(self._validate_input), '%P'))

    @property
    def model(self):
        """获取当前模式 ('int' 或 'float')"""
        return self._model

    @model.setter
    def model(self, value):
        """设置模式 ('int' 或 'float')，并在切换模式时自动重置为默认值"""
        if value in ['int', 'float']:
            self._model = value
            if value == 'int':
                self.configure(from_=self.int_min, increment=1)
                self.set(self.int_min)  # 重置为整数模式的最小值
            elif value == 'float':
                self.configure(from_=self.float_min, increment=0.1)
                self.set(self.default_value)  # 重置为浮点模式的默认值 1
        else:
            raise ValueError("model 属性只能是 'int' 或 'float'")
    
    def _validate_input(self, value_if_allowed):
        """
        根据当前模式验证输入值，自动调整到最大值。
        """
        if value_if_allowed == "":
            return True

        # 整数模式验证
        if self._model == 'int':
            if value_if_allowed.isdigit():  # 仅允许数字
                int_value = int(value_if_allowed)
                if int_value > self.max_value:
                    self.set(self.max_value)
                return int_value >= self.int_min

        # 浮点模式验证
        elif self._model == 'float':
            try:
                # 验证浮点数格式，并限制小数点位数为1
                if value_if_allowed.count('.') <= 1 and all(c.isdigit() or c == '.' for c in value_if_allowed):
                    if '.' in value_if_allowed:
                        decimal_part = value_if_allowed.split('.')[1]
                        # 限制小数点后仅1位数字
                        if len(decimal_part) > 1:
                            return False
                    float_value = float(value_if_allowed)
                    if float_value > self.max_value:
                        self.set(f"{self.max_value:.1f}")
                    return float_value >= self.float_min
            except ValueError:
                return False
        return False

# # 创建 Tkinter 主窗口
# root = tk.Tk()
# root.title("Customizable Spinbox Mode")

# # 初始化 Spinbox
# spinbox = ValidatedSpinbox(root)
# spinbox.pack(padx=20, pady=10)

# # 设置 Spinbox 的模式为整数模式
# spinbox.model = 'int'

# # 添加按钮以切换模式
# def toggle_mode():
#     spinbox.model = 'float' if spinbox.model == 'int' else 'int'

# toggle_button = tk.Button(root, text="Toggle Mode", command=toggle_mode)
# toggle_button.pack(pady=10)

# root.mainloop()
