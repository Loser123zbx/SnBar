import wx
import wx.adv
import json
import sys
import os

class SystemTrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        icon = wx.Icon("icon.ico")
        self.SetIcon(icon, "123 Bar")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnLeftClick)

    def OnLeftClick(self, event):
        self.frame.Show()
        self.frame.Restore()

class Bar(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, style=wx.BORDER_NONE|wx.STAY_ON_TOP)
        
        # 创建系统托盘图标
        self.tray_icon = SystemTrayIcon(self)
        
        # 绑定关闭事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        # 绑定鼠标事件以支持拖动
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        
        # 绑定鼠标滚轮事件用于调节透明度
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        
        # 设置窗口大小
        self.SetSize((520, 250))
        
        # 获取屏幕尺寸并设置窗口位置到右下角
        screen_width, screen_height = wx.DisplaySize()
        window_width, window_height = self.GetSize()
        x = screen_width - window_width - 20
        y = screen_height - window_height - 60
        self.SetPosition((x, y))
        
        # 初始化拖动相关变量
        self.dragging = False
        self.drag_pos = wx.Point(0, 0)
        
        # 设置初始透明度
        self.SetTransparent(200)
        
        # 创建一个面板来放置控件
        self.panel = wx.Panel(self)
        
        # 从配置文件加载控件
        self.load_controls()

    def load_controls(self):
        # 获取配置文件路径
        config_path = os.path.join(os.path.dirname(__file__), 'controls.json')
        
        try:
            # 读取配置文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 创建控件
            for control_config in config['controls']:
                self.create_control(control_config)
                
        except Exception as e:
            print(f"Error loading controls: {e}")

    def create_control(self, config):
        control_type = config['type']
        
        # 基本参数
        params = {
            'parent': self.panel,
            'pos': wx.Point(*config['pos']),
            'size': wx.Size(*config['size'])
        }
        
        # 添加特定参数
        if 'label' in config:
            params['label'] = config['label']
        if 'value' in config:
            params['value'] = config['value']
        if 'style' in config:
            params['style'] = config['style']
        
        # 创建控件
        control = None
        if control_type == 'wx.StaticText':
            control = wx.StaticText(**params)
        elif control_type == 'wx.Button':
            control = wx.Button(**params)
            if 'event' in config:
                # 绑定事件
                event_handler = getattr(self, config['event'], None)
                if event_handler:
                    control.Bind(wx.EVT_BUTTON, event_handler)
        elif control_type == 'wx.TextCtrl':
            control = wx.TextCtrl(**params)
        # 可以继续添加其他控件类型
        
        return control

    # 示例事件处理函数
    def on_button_click(self, event):
        wx.MessageBox("Button clicked!", "Info")

    def OnLeftDown(self, event):
        self.drag_pos = event.GetPosition()
        self.dragging = True

    def OnLeftUp(self, event):
        self.dragging = False

    def OnMouseMove(self, event):
        if self.dragging:
            current_pos = self.GetPosition()
            mouse_pos = wx.GetMousePosition()
            new_x = mouse_pos.x - self.drag_pos.x
            new_y = mouse_pos.y - self.drag_pos.y
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
        self.Hide()
        event.Veto()

class App(wx.App):
    def OnInit(self):
        self.frame = Bar()
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = App(False)
    app.MainLoop()
