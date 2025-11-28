
import core.panel as PanelCore
from core.panel import Panel
from core.control import Control
import core.control as cc
import wx
import json
import wx.adv




class SystemTrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        # 创建一个简单的图标
        icon = wx.Icon("icon.ico")
        self.SetIcon(icon, "123 Bar")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnLeftClick)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.OnRightClick)

    def OnLeftClick(self, event):
        self.frame.Show()
        self.frame.Restore()
    
    def Exit(self, event):  # 添加 event 参数
        self.frame.Destroy()
    
    def OnRightClick(self, event):
        # 创建一个弹出菜单
        menu = wx.Menu()
        exit_item = wx.MenuItem(menu, wx.ID_EXIT, "Exit")
        menu.Append(exit_item)
        self.Bind(wx.EVT_MENU, self.Exit)
        self.PopupMenu(menu)
        menu.Destroy()

class Bar(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, style=wx.BORDER_NONE|wx.STAY_ON_TOP)

        self.SetTransparent(200)
        # 创建系统托盘图标
        self.tray_icon = SystemTrayIcon(self)
        
        # 绑定关闭事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        # 绑定鼠标事件以支持拖动
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        
        # 设置窗口大小
        self.SetSize((520, 250))
        
        # 获取屏幕尺寸并设置窗口位置到右下角
        screen_width, screen_height = wx.DisplaySize()
        window_width, window_height = self.GetSize()
        
        # 计算右下角位置（留出一些边距）
        x = screen_width - window_width - 20
        y = screen_height - window_height - 60  # 考虑任务栏高度
        self.SetPosition((x, y))
        
        # 初始化拖动相关变量
        self.dragging = False
        self.drag_pos = wx.Point(0, 0)

    def OnLeftDown(self, event):
        # 记录鼠标按下的位置
        self.drag_pos = event.GetPosition()
        self.dragging = True

    def OnLeftUp(self, event):
        self.dragging = False

    def OnMouseMove(self, event):
        if self.dragging:
            # 计算窗口新位置
            current_pos = self.GetPosition()
            mouse_pos = wx.GetMousePosition()
            new_x = mouse_pos.x - self.drag_pos.x
            new_y = mouse_pos.y - self.drag_pos.y
            self.SetPosition((new_x, new_y))

    def OnClose(self, event):
        self.Hide()  # 隐藏窗口而不是关闭
        event.Veto()  # 阻止窗口真正关闭

controls = (cc.ImportControlByJson("core/example.json"))
Panel1 = Panel(controls)

class App(wx.App):
    def OnInit(self):
        self.frame = Panel1.Run()
        self.frame.Show()
        return True
    

if __name__ == "__main__":
    app = App(False)
    app.MainLoop()
