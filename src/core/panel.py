import wx
import wx.adv
import os
from typing import List
try:
    import core.control as cc
    from core.control import Control
except ImportError:
    import control as cc
    from control import Control


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
    
    def Exit(self, event):
        try:
            self.frame.Destroy()
            exit()
        except Exception as e:
            print(f"Error during exit: {e}")
            exit()
    
    def OnRightClick(self, event):
        # 创建一个弹出菜单
        menu = wx.Menu()
        exit_item = wx.MenuItem(menu, wx.ID_EXIT, "Exit")
        menu.Append(exit_item)
        self.Bind(wx.EVT_MENU, self.Exit)
        self.PopupMenu(menu)
        menu.Destroy()

class Panel(wx.Frame):
    def __init__(self, Controls, parent=None):
        if not wx.GetApp():
            self.app = wx.App()
        else:
            self.app = wx.GetApp()
        wx.Frame.__init__(self, parent, style=wx.BORDER_NONE|wx.STAY_ON_TOP)
        
        self.Controls = Controls
        self.SetTransparent(200)
        self.SetBackgroundColour("#392652")
        
        # 创建系统托盘图标
        self.tray_icon = SystemTrayIcon(self)
        
        # 绑定事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        
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
        
        # 创建控件
        self._create_controls()

    def _create_controls(self):
        def _parse_style_item(item):
            """解析单个 style 项，支持 int 或 wx 常量名字符串。"""
            if isinstance(item, int):
                return item
            if isinstance(item, str):
                name = item
                if name.startswith("wx."):
                    name = name.split(".", 1)[1]
                for candidate in (name, name.upper()):
                    if hasattr(wx, candidate):
                        return getattr(wx, candidate)
                raise TypeError(f"样式常量 '{item}' 在 wx 中不存在")
            raise TypeError(f"不支持的 style 类型: {type(item)!r}")

        def _combine_style(style_field):
            """把 Style 字段（可以是 int、str、list/tuple 混合）合并为单个整数 style 标志。"""
            if style_field is None:
                return 0
            if isinstance(style_field, int):
                return style_field
            if isinstance(style_field, str):
                return _parse_style_item(style_field)
            if isinstance(style_field, (list, tuple)):
                combined = 0
                for it in style_field:
                    combined |= _parse_style_item(it)
                return combined
            raise TypeError(f"无法解析的 Style 字段类型: {type(style_field)!r}")

        for Acontrol in self.Controls:
            try:
                try:
                    control_class = getattr(wx, Acontrol.Type)
                except AttributeError:
                    raise Exception(f"控件类型 {Acontrol.Type} 不存在")

                try:
                    combined_style = _combine_style(Acontrol.Style)
                except TypeError as e:
                    raise Exception(str(e))

                
                if Acontrol.Type == "StaticBitmap":
                # StaticBitmap 使用不同的参数
                    control = control_class(
                        parent=self,
                        bitmap=wx.Bitmap(Acontrol.Label),  # 使用 Label 参数作为位图路径
                        pos=Acontrol.Position,
                        size=Acontrol.Size,
                    )
                else:
                    # 其他控件使用标准创建方式
                    control = control_class(
                        parent=self,
                        id=wx.ID_ANY,
                        label=Acontrol.Label,
                        pos=Acontrol.Position,
                        size=Acontrol.Size,
                        style=combined_style,
                    )
                Acontrol.control = control
                
                if Acontrol.Event:
                    for event_type, handler in Acontrol.Event.items():
                        event = getattr(wx, event_type)
                        control.Bind(event, handler)
            except Exception:
                raise

    def OnLeftDown(self, event):
        self.drag_pos = event.GetPosition()
        self.dragging = True

    def OnLeftUp(self, event):
        self.dragging = False

    def OnMouseMove(self, event):
        if self.dragging:
            pos = event.GetPosition()
            frame_pos = self.GetPosition()
            new_x = frame_pos.x + pos.x - self.drag_pos.x
            new_y = frame_pos.y + pos.y - self.drag_pos.y
            self.SetPosition((new_x, new_y))

    def OnMouseWheel(self, event):
        current_alpha = self.GetTransparent()
        rotation = event.GetWheelRotation()
        if rotation > 0:
            new_alpha = min(255, current_alpha + 10)
        else:
            new_alpha = max(30, current_alpha - 10)
        self.SetTransparent(new_alpha)
        event.Skip()

    def OnClose(self, event):
        self.Hide()  # 隐藏窗口而不是关闭
        event.Veto()  # 阻止窗口真正关闭

    def Run(self) -> None:
        app = wx.App()
        self.Show()
        app.MainLoop()

if __name__ == '__main__':
    cts = cc.ImportControlByJson("core/example.json")
    panel1 = Panel(cts)
    panel1.Run()

