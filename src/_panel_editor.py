import wx
import os

def OpenLink(link: str) -> None:
    wx.LaunchDefaultBrowser(link)


def OpenFile(path: str) -> None:
    wx.LaunchDefaultApplication(path)

def OpenFolder(path: str) -> None:
    wx.LaunchDefaultApplication(path)

def RunCommand(command: str) -> None:
    os.system(command)

def OpenApp(app: str) -> None:
    wx.LaunchDefaultApplication(app)

def RunPythonCode(code: str) -> None:
    exec(code)



class Control:
    def __init__(self,
                 Type: str,
                 Name: str = "name",
                 Parent: any = None,
                 Sizer: wx.Sizer = None,
                 Label: str = "None",
                 Style: list = [],
                 Event: dict = None,
                 Size: tuple = (50, 20),
                 Position: tuple = (10, 10)):
        self.Name = Name
        self.Parent = Parent
        self.Sizer = Sizer
        self.Type = Type
        self.Label = Label
        self.Style = Style
        self.Event = Event or {}
        self.Size = Size
        self.Position = Position

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
        
        for Acontrol in self.Controls:
            # 从字符串获取控件类
            control_class = getattr(wx, Acontrol.Type)
            # 创建控件实例
            control = control_class(
                parent=self.frame,
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
            "EVT_BUTTON": lambda event: OpenLink("https://www.bilibili.com/")
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
            "EVT_BUTTON": lambda event: RunCommand("cmd")
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
            "EVT_BUTTON": lambda event: OpenFolder("D:/")
        }
    )

    cts = [button1, button2, button3]

    # 创建面板并添加控件
    panel1 = Panel(cts)
    panel1.Run()
