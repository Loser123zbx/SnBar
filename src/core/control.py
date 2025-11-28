import wx
import os
import json

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
    

def ImportControlByJson(json_path: str) -> list[Control]:
    Controls : list[Control] = [ ]
    with open(json_path, "r") as f:
        data = json.load(f)
        print(data)
        for control in data:
            _parent = control.get("Parent")
            _type = control.get("Type")
            _name = control.get("Name")
            _label = control.get("Label")
            _style = control.get("Style")
            _event = control.get("Event")
            _size :tuple = tuple(control.get("Size"))
            _position :tuple = tuple(control.get("Position"))
            _sizer = control.get("Sizer")
            try:
                _control : Control = Control(Type = _type, Name = _name, Parent= _parent, 
                                Sizer = _sizer, Label = _label, Style = _style,
                                Size = _size, Position = _position)
                events_tmp = {}
                for event_name, event_handler in _event.items():
                    for _func , _value in event_handler.items():
                        if _func == "OpenLink":
                            events_tmp[event_name] = lambda evt, link=_value: OpenLink(link)
                        elif _func == "OpenFile":
                            events_tmp[event_name] = lambda evt, path=_value: OpenFile(path)
                        elif _func == "OpenFolder":
                            events_tmp[event_name] = lambda evt, path=_value: OpenFolder(path)
                        elif _func == "RunCommand":
                            events_tmp[event_name] = lambda evt, command=_value: RunCommand(command)
                        elif _func == "OpenApp":
                            events_tmp[event_name] = lambda evt, app=_value: OpenApp(app)
                        elif _func == "RunPythonCode":
                            events_tmp[event_name] = lambda evt, code=_value: RunPythonCode(code)
                print(events_tmp)
                 
                _control.Event = events_tmp

            except TypeError:
                raise TypeError("Control Type Error")
                
            Controls.append(_control)

    return Controls

if __name__ == "__main__":
    try:
        import core.panel as cp
        from core.panel import Panel
    except:
        import panel as cp
        from panel import Panel

    print(ImportControlByJson("example.json"))
    
    Controls = (ImportControlByJson("example.json"))
    
    print(Controls)

    Panel1 = Panel(Controls)
    Panel1.Run()


    
