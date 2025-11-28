import wx
import os

try:
    import core.control as cc
    from core.control import Control
except ImportError:
    import control as cc
    from control import Control

class Panel:
    def __init__(self, Controls: list[Control]):
        self.Controls = Controls
        self.dragging = False
        self.drag_pos = wx.Point(0, 0)
    
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

    def OnLeftDown(self, event):
        self.drag_pos = event.GetPosition()
        self.dragging = True

    def OnLeftUp(self, event):
        self.dragging = False

    def OnMouseMove(self, event):
        if self.dragging:
            pos = event.GetPosition()
            frame_pos = self.frame.GetPosition()
            new_x = frame_pos.x + pos.x - self.drag_pos.x
            new_y = frame_pos.y + pos.y - self.drag_pos.y
            self.frame.SetPosition((new_x, new_y))

    def OnMouseWheel(self, event):
        current_alpha = self.frame.GetTransparent()
        rotation = event.GetWheelRotation()
        if rotation > 0:
            new_alpha = min(255, current_alpha + 10)
        else:
            new_alpha = max(30, current_alpha - 10)
        self.frame.SetTransparent(new_alpha)
        event.Skip()

    def OnClose(self, event):
        self.Hide()  # 隐藏窗口而不是关闭
        event.Veto()  # 阻止窗口真正关闭

    def Run(self) -> None:
        app = wx.App()
        self.frame = wx.Frame(None, style=wx.BORDER_NONE|wx.STAY_ON_TOP)
        self.frame.SetSize((520, 250))
        self.frame.SetTransparent(200)
        
        # 获取屏幕尺寸并设置窗口位置到右下角
        screen_width, screen_height = wx.DisplaySize()
        window_width, window_height = self.frame.GetSize()
        x = screen_width - window_width - 20
        y = screen_height - window_height - 60
        self.frame.SetPosition((x, y))
        
        # 绑定事件处理函数到frame
        self.frame.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.frame.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.frame.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.frame.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        
        def _parse_style_item(item):
            """解析单个 style 项，支持 int 或 wx 常量名字符串。"""
            # 已经是整数常量
            if isinstance(item, int):
                return item
            # 字符串常量，尝试从 wx 模块中获取
            if isinstance(item, str):
                name = item
                # 支持传入 'wx.BORDER_DEFAULT' 或 'BORDER_DEFAULT'
                if name.startswith("wx."):
                    name = name.split(".", 1)[1]
                # 先尝试原名，然后尝试大写
                for candidate in (name, name.upper()):
                    if hasattr(wx, candidate):
                        return getattr(wx, candidate)
                raise TypeError(f"样式常量 '{item}' 在 wx 中不存在")
            raise TypeError(f"不支持的 style 类型: {type(item)!r}")

        def _combine_style(style_field):
            """把 Style 字段（可以是 int、str、list/tuple 混合）合并为单个整数 style 标志。"""
            if style_field is None:
                return 0
            # 直接是整数
            if isinstance(style_field, int):
                return style_field
            # 如果是字符串，解析单条
            if isinstance(style_field, str):
                return _parse_style_item(style_field)
            # 如果是可迭代（list/tuple），对每一项解析后按位或
            if isinstance(style_field, (list, tuple)):
                combined = 0
                for it in style_field:
                    combined |= _parse_style_item(it)
                return combined
            # 其它类型不支持
            raise TypeError(f"无法解析的 Style 字段类型: {type(style_field)!r}")

        for Acontrol in self.Controls:
            try:
                # 从字符串获取控件类，如果不存在抛出 AttributeError
                try:
                    control_class = getattr(wx, Acontrol.Type)
                except AttributeError:
                    raise Exception(f"控件类型 {Acontrol.Type} 不存在")

                # 解析 style 字段并传给控件构造器
                try:
                    combined_style = _combine_style(Acontrol.Style)
                except TypeError as e:
                    raise Exception(str(e))

                # 创建控件实例；许多 wx 控件 接受 label/pos/size/style
                control = control_class(
                    parent=self.frame,
                    id=wx.ID_ANY,
                    label=Acontrol.Label,
                    pos=Acontrol.Position,
                    size=Acontrol.Size,
                    style=combined_style,
                )
            except Exception:
                # 把异常向上抛出，便于定位问题
                raise
            
            # 保存控件实例
            Acontrol.control = control
            
            # 绑定事件
            if Acontrol.Event:
                for event_type, handler in Acontrol.Event.items():
                    event = getattr(wx, event_type)
                    control.Bind(event, handler)
        
        self.frame.Show()
        app.MainLoop()

if __name__ == '__main__':
    # 创建按钮控件
    button1 = Control(
        Type="Button",
        Name='button1',
        Label="打开B站",
        Style=wx.BORDER_DEFAULT,
        Position = (10,10),
        Size = (100, 30),
        Event={
            "EVT_BUTTON": lambda event: cc.OpenLink("https://www.bilibili.com/")
        }
    )
    button2 = Control(
        Type="Button",
        Name='button2',
        Label="打开CMD",
        Style=wx.BORDER_DEFAULT,
        Position = (10,50),
        Size = (100, 30),
        Event={
            "EVT_BUTTON": lambda event: cc.RunCommand("cmd")
        }
    )
    button3 = Control(
        Type="Button",
        Name='button3',
        Label="打开D:/",
        Style=wx.BORDER_DEFAULT,
        Position = (10,90),
        Size = (100, 30),
        Event={
            "EVT_BUTTON": lambda event: cc.OpenFolder("D:/")
        }
    )

    cts = [button1, button2, button3]

    # 创建面板并添加控件
    panel1 = Panel(cts)
    panel1.Run()
