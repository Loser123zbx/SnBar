import wx

class Control:
    def __init__(self,
                 Type: str,
                 Name: str = "name",
                 Parent: any = None,
                 Sizer: wx.Sizer = None,
                 Label: str = "None",
                 Style: int = 0,  # 改为int类型
                 Event: dict = None):
        
        self.Name = Name
        
        #父类及Sizer
        self.Parent = Parent
        self.Sizer = Sizer
        
        #显示相关
        self.Type = Type
        self.Label = Label
        self.Style = Style
        self.Event = Event or {}

        #位置及大小
        self.Size = (100, 30)  # 设置默认大小
        self.Position = (10, 10)  # 设置默认位置

class Panel:
    def __init__(self, Controls: list[Control]):
        self.Controls = Controls
    
    def Add(self, control: Control) -> None:
        self.Controls.append(control)

    def Remove(self, control: Control) -> None:
        self.Controls.remove(control)

    def Clear(self) -> None:
        self.Controls.clear()

    def Get(self, name: str) -> Control:
        for control in self.Controls:
            if control.Name == name:
                return control
        return None
    
    def Run(self) -> None:
        app = wx.App()
        frame = wx.Frame(None, title="Test Frame", size=(300, 200))
        
        for Acontrol in self.Controls:
            # 从字符串获取控件类
            control_class = getattr(wx, Acontrol.Type)
            # 创建控件实例，使用关键字参数
            control = control_class(
                parent=frame,
                id=wx.ID_ANY,
                label=Acontrol.Label,
                pos=Acontrol.Position,
                size=Acontrol.Size,
                style=Acontrol.Style
            )
            
            # 保存控件实例
            Acontrol.control = control
            
            # 绑定事件
            if Acontrol.Event:
                for event_type, handler in Acontrol.Event.items():
                    event = getattr(wx, event_type)
                    control.Bind(event, handler)
        
        frame.Show()
        app.MainLoop()

if __name__ == '__main__':
    # 创建按钮控件
    button1 = Control(
        Type="Button",
        Name='button1',
        Label="Click Me",
        Style=wx.BORDER_DEFAULT
    )

    button2 = Control(
        Type="Button",
        Name='button1',
        Label="Click Me",
        Style=wx.BORDER_DEFAULT
    )

    
    # 创建面板并添加控件
    panel1 = Panel([button1])
    panel1.Run()
