
# WxPython Control Customization Guide

## Basic Control Types

### 1. Button (wx.Button)
```json
{
    "Type": "Button",
    "Name": "btnOK",
    "Label": "OK",
    "Size": [100, 30],
    "Position": [10, 10],
    "Style": ["wx.ALIGN_CENTER", "wx.BU_EXACTFIT"]
}
```
Documentation: [wx.Button](https://docs.wxpython.org/wx.Button.html)

### 2. Text Control (wx.TextCtrl)
```json
{
    "Type": "TextCtrl",
    "Name": "txtInput",
    "Label": "",
    "Size": [200, 25],
    "Position": [10, 50],
    "Style": ["wx.TE_PROCESS_ENTER", "wx.BORDER_SUNKEN"]
}
```
Documentation: [wx.TextCtrl](https://docs.wxpython.org/wx.TextCtrl.html)

### 3. Static Text (wx.StaticText)
```json
{
    "Type": "StaticText",
    "Name": "lblMessage",
    "Label": "Message",
    "Size": [100, 20],
    "Position": [10, 90],
    "Style": ["wx.ALIGN_LEFT"]
}
```
Documentation: [wx.StaticText](https://docs.wxpython.org/wx.StaticText.html)

### 4. Checkbox (wx.CheckBox)
```json
{
    "Type": "CheckBox",
    "Name": "chkAuto",
    "Label": "Auto Save",
    "Size": [120, 20],
    "Position": [10, 130],
    "Style": []
}
```
Documentation: [wx.CheckBox](https://docs.wxpython.org/wx.CheckBox.html)

### 5. Radio Button (wx.RadioButton)
```json
{
    "Type": "RadioButton",
    "Name": "rbOption1",
    "Label": "Option 1",
    "Size": [100, 20],
    "Position": [10, 170],
    "Style": ["wx.RB_GROUP"]
}
```
Documentation: [wx.RadioButton](https://docs.wxpython.org/wx.RadioButton.html)

## Layout Managers

### 1. Horizontal Layout (wx.BoxSizer - Horizontal)
```json
{
    "Type": "Panel",
    "Name": "panelMain",
    "Sizer": "wx.BoxSizer(wx.HORIZONTAL)",
    "Size": [300, 200],
    "Position": [10, 10]
}
```

### 2. Vertical Layout (wx.BoxSizer - Vertical)
```json
{
    "Type": "Panel",
    "Name": "panelMain",
    "Sizer": "wx.BoxSizer(wx.VERTICAL)",
    "Size": [300, 200],
    "Position": [10, 10]
}
```

Documentation: [wx.Sizer](https://docs.wxpython.org/wx.Sizer.html)

## Event Handling

### 1. Button Click Event
```json
{
    "Type": "Button",
    "Name": "btnOK",
    "Event": {
        "wx.EVT_BUTTON": {
            "RunPythonCode": "print('Button clicked')"
        }
    }
}
```

### 2. Text Input Event
```json
{
    "Type": "TextCtrl",
    "Name": "txtInput",
    "Event": {
        "wx.EVT_TEXT_ENTER": {
            "RunCommand": "notepad"
        }
    }
}
```

### 3. Mouse Event
```json
{
    "Type": "Panel",
    "Name": "panelMain",
    "Event": {
        "wx.EVT_LEFT_DOWN": {
            "RunPythonCode": "print('Left mouse button pressed')"
        }
    }
}
```

## Style Combinations

### 1. Button Style Combination
```json
{
    "Type": "Button",
    "Name": "btnOK",
    "Style": [
        "wx.ALIGN_CENTER",
        "wx.BU_EXACTFIT",
        "wx.BORDER_NONE"
    ]
}
```

### 2. Text Control Style Combination
```json
{
    "Type": "TextCtrl",
    "Name": "txtInput",
    "Style": [
        "wx.TE_PROCESS_ENTER",
        "wx.TE_MULTILINE",
        "wx.BORDER_SUNKEN"
    ]
}
```

## Complete Example

```json
[
    {
        "Type": "Panel",
        "Name": "mainPanel",
        "Sizer": "wx.BoxSizer(wx.VERTICAL)",
        "Size": [300, 200],
        "Position": [10, 10],
        "Controls": [
            {
                "Type": "StaticText",
                "Name": "lblTitle",
                "Label": "Please enter information",
                "Size": [100, 20],
                "Position": [10, 10],
                "Style": ["wx.ALIGN_CENTER"]
            },
            {
                "Type": "TextCtrl",
                "Name": "txtInput",
                "Size": [200, 25],
                "Position": [10, 40],
                "Style": ["wx.TE_PROCESS_ENTER"],
                "Event": {
                    "wx.EVT_TEXT_ENTER": {
                        "RunPythonCode": "print('Input: ' + self.txtInput.GetValue())"
                    }
                }
            },
            {
                "Type": "Button",
                "Name": "btnOK",
                "Label": "OK",
                "Size": [100, 30],
                "Position": [10, 80],
                "Style": ["wx.ALIGN_CENTER"],
                "Event": {
                    "wx.EVT_BUTTON": {
                        "RunCommand": "echo 'OK button clicked'"
                    }
                }
            }
        ]
    }
]
```

## Important Notes

1. All control types must use class names defined in wxPython
2. Style constants must be prefixed with "wx."
3. Event types must use complete wxPython event constant names
4. Layout managers must be defined in parent controls
5. Control coordinates and dimensions are relative to the parent control
6. When using RunPythonCode, you can access current control properties and methods through self

For more detailed control information and style options, please refer to the official wxPython documentation: [wxPython Documentation](https://docs.wxpython.org/)