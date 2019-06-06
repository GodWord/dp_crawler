import platform
import copy

Keys = {'\b': ["Backspace", "Backspace", "", "", 8, 8, False, False],
        '\t': ["Tab", "Tab", "", "", 9, 9, False, False],
        '\r': ["Enter", "Enter", "\r", "\r", 13, 13, False, True],
        '\u001b': ["Escape", "Escape", "", "", 27, 27, False, False],
        ' ': ["Space", " ", " ", " ", 32, 32, False, True],
        '!': ["Digit1", "!", "!", "1", 49, 49, True, True],
        '"': ["Quote", "\"", "\"", "'", 222, 222, True, True],
        '#': ["Digit3", "#", "#", "3", 51, 51, True, True],
        '$': ["Digit4", "$", "$", "4", 52, 52, True, True],
        '%': ["Digit5", "%", "%", "5", 53, 53, True, True],
        '&': ["Digit7", "&", "&", "7", 55, 55, True, True],
        '\'': ["Quote", "'", "'", "'", 222, 222, False, True],
        '(': ["Digit9", "(", "(", "9", 57, 57, True, True],
        ')': ["Digit0", ")", ")", "0", 48, 48, True, True],
        '*': ["Digit8", "*", "*", "8", 56, 56, True, True],
        '+': ["Equal", "+", "+", "=", 187, 187, True, True],
        ',': ["Comma", ",", ",", ",", 188, 188, False, True],
        '-': ["Minus", "-", "-", "-", 189, 189, False, True],
        '.': ["Period", ".", ".", ".", 190, 190, False, True],
        '/': ["Slash", "/", "/", "/", 191, 191, False, True],
        '0': ["Digit0", "0", "0", "0", 48, 48, False, True],
        '1': ["Digit1", "1", "1", "1", 49, 49, False, True],
        '2': ["Digit2", "2", "2", "2", 50, 50, False, True],
        '3': ["Digit3", "3", "3", "3", 51, 51, False, True],
        '4': ["Digit4", "4", "4", "4", 52, 52, False, True],
        '5': ["Digit5", "5", "5", "5", 53, 53, False, True],
        '6': ["Digit6", "6", "6", "6", 54, 54, False, True],
        '7': ["Digit7", "7", "7", "7", 55, 55, False, True],
        '8': ["Digit8", "8", "8", "8", 56, 56, False, True],
        '9': ["Digit9", "9", "9", "9", 57, 57, False, True],
        ':': ["Semicolon", ":", ":", ";", 186, 186, True, True],
        ';': ["Semicolon", ";", ";", ";", 186, 186, False, True],
        '<': ["Comma", "<", "<", ",", 188, 188, True, True],
        '=': ["Equal", "=", "=", "=", 187, 187, False, True],
        '>': ["Period", ">", ">", ".", 190, 190, True, True],
        '?': ["Slash", "?", "?", "/", 191, 191, True, True],
        '@': ["Digit2", "@", "@", "2", 50, 50, True, True],
        'A': ["KeyA", "A", "A", "a", 65, 65, True, True],
        'B': ["KeyB", "B", "B", "b", 66, 66, True, True],
        'C': ["KeyC", "C", "C", "c", 67, 67, True, True],
        'D': ["KeyD", "D", "D", "d", 68, 68, True, True],
        'E': ["KeyE", "E", "E", "e", 69, 69, True, True],
        'F': ["KeyF", "F", "F", "f", 70, 70, True, True],
        'G': ["KeyG", "G", "G", "g", 71, 71, True, True],
        'H': ["KeyH", "H", "H", "h", 72, 72, True, True],
        'I': ["KeyI", "I", "I", "i", 73, 73, True, True],
        'J': ["KeyJ", "J", "J", "j", 74, 74, True, True],
        'K': ["KeyK", "K", "K", "k", 75, 75, True, True],
        'L': ["KeyL", "L", "L", "l", 76, 76, True, True],
        'M': ["KeyM", "M", "M", "m", 77, 77, True, True],
        'N': ["KeyN", "N", "N", "n", 78, 78, True, True],
        'O': ["KeyO", "O", "O", "o", 79, 79, True, True],
        'P': ["KeyP", "P", "P", "p", 80, 80, True, True],
        'Q': ["KeyQ", "Q", "Q", "q", 81, 81, True, True],
        'R': ["KeyR", "R", "R", "r", 82, 82, True, True],
        'S': ["KeyS", "S", "S", "s", 83, 83, True, True],
        'T': ["KeyT", "T", "T", "t", 84, 84, True, True],
        'U': ["KeyU", "U", "U", "u", 85, 85, True, True],
        'V': ["KeyV", "V", "V", "v", 86, 86, True, True],
        'W': ["KeyW", "W", "W", "w", 87, 87, True, True],
        'X': ["KeyX", "X", "X", "x", 88, 88, True, True],
        'Y': ["KeyY", "Y", "Y", "y", 89, 89, True, True],
        'Z': ["KeyZ", "Z", "Z", "z", 90, 90, True, True],
        '[': ["BracketLeft", "[", "[", "[", 219, 219, False, True],
        '\\': ["Backslash", "\\", "\\", "\\", 220, 220, False, True],
        ']': ["BracketRight", "]", "]", "]", 221, 221, False, True],
        '^': ["Digit6", "^", "^", "6", 54, 54, True, True],
        '_': ["Minus", "_", "_", "-", 189, 189, True, True],
        '`': ["Backquote", "`", "`", "`", 192, 192, False, True],
        'a': ["KeyA", "a", "a", "a", 65, 65, False, True],
        'b': ["KeyB", "b", "b", "b", 66, 66, False, True],
        'c': ["KeyC", "c", "c", "c", 67, 67, False, True],
        'd': ["KeyD", "d", "d", "d", 68, 68, False, True],
        'e': ["KeyE", "e", "e", "e", 69, 69, False, True],
        'f': ["KeyF", "f", "f", "f", 70, 70, False, True],
        'g': ["KeyG", "g", "g", "g", 71, 71, False, True],
        'h': ["KeyH", "h", "h", "h", 72, 72, False, True],
        'i': ["KeyI", "i", "i", "i", 73, 73, False, True],
        'j': ["KeyJ", "j", "j", "j", 74, 74, False, True],
        'k': ["KeyK", "k", "k", "k", 75, 75, False, True],
        'l': ["KeyL", "l", "l", "l", 76, 76, False, True],
        'm': ["KeyM", "m", "m", "m", 77, 77, False, True],
        'n': ["KeyN", "n", "n", "n", 78, 78, False, True],
        'o': ["KeyO", "o", "o", "o", 79, 79, False, True],
        'p': ["KeyP", "p", "p", "p", 80, 80, False, True],
        'q': ["KeyQ", "q", "q", "q", 81, 81, False, True],
        'r': ["KeyR", "r", "r", "r", 82, 82, False, True],
        's': ["KeyS", "s", "s", "s", 83, 83, False, True],
        't': ["KeyT", "t", "t", "t", 84, 84, False, True],
        'u': ["KeyU", "u", "u", "u", 85, 85, False, True],
        'v': ["KeyV", "v", "v", "v", 86, 86, False, True],
        'w': ["KeyW", "w", "w", "w", 87, 87, False, True],
        'x': ["KeyX", "x", "x", "x", 88, 88, False, True],
        'y': ["KeyY", "y", "y", "y", 89, 89, False, True],
        'z': ["KeyZ", "z", "z", "z", 90, 90, False, True],
        '{': ["BracketLeft", "{", "{", "[", 219, 219, True, True],
        '|': ["Backslash", "|", "|", "\\", 220, 220, True, True],
        '}': ["BracketRight", "}", "}", "]", 221, 221, True, True],
        '~': ["Backquote", "~", "~", "`", 192, 192, True, True],
        '\u007f': ["Delete", "Delete", "", "", 46, 46, False, False],
        '¥': ["IntlYen", "¥", "¥", "¥", 220, 220, False, True],
        '\u0102': ["AltLeft", "Alt", "", "", 164, 164, False, False],
        '\u0104': ["CapsLock", "CapsLock", "", "", 20, 20, False, False],
        '\u0105': ["ControlLeft", "Control", "", "", 162, 162, False, False],
        '\u0106': ["Fn", "Fn", "", "", 0, 0, False, False],
        '\u0107': ["FnLock", "FnLock", "", "", 0, 0, False, False],
        '\u0108': ["Hyper", "Hyper", "", "", 0, 0, False, False],
        '\u0109': ["MetaLeft", "Meta", "", "", 91, 91, False, False],
        '\u010a': ["NumLock", "NumLock", "", "", 144, 144, False, False],
        '\u010c': ["ScrollLock", "ScrollLock", "", "", 145, 145, False, False],
        '\u010d': ["ShiftLeft", "Shift", "", "", 160, 160, False, False],
        '\u010e': ["Super", "Super", "", "", 0, 0, False, False],
        '\u0301': ["ArrowDown", "ArrowDown", "", "", 40, 40, False, False],
        '\u0302': ["ArrowLeft", "ArrowLeft", "", "", 37, 37, False, False],
        '\u0303': ["ArrowRight", "ArrowRight", "", "", 39, 39, False, False],
        '\u0304': ["ArrowUp", "ArrowUp", "", "", 38, 38, False, False],
        '\u0305': ["End", "End", "", "", 35, 35, False, False],
        '\u0306': ["Home", "Home", "", "", 36, 36, False, False],
        '\u0307': ["PageDown", "PageDown", "", "", 34, 34, False, False],
        '\u0308': ["PageUp", "PageUp", "", "", 33, 33, False, False],
        '\u0401': ["NumpadClear", "Clear", "", "", 12, 12, False, False],
        '\u0402': ["Copy", "Copy", "", "", 0, 0, False, False],
        '\u0404': ["Cut", "Cut", "", "", 0, 0, False, False],
        '\u0407': ["Insert", "Insert", "", "", 45, 45, False, False],
        '\u0408': ["Paste", "Paste", "", "", 0, 0, False, False],
        '\u0409': ["Redo", "Redo", "", "", 0, 0, False, False],
        '\u040a': ["Undo", "Undo", "", "", 0, 0, False, False],
        '\u0502': ["Again", "Again", "", "", 0, 0, False, False],
        '\u0504': ["Abort", "Cancel", "", "", 0, 0, False, False],
        '\u0505': ["ContextMenu", "ContextMenu", "", "", 93, 93, False, False],
        '\u0507': ["Find", "Find", "", "", 0, 0, False, False],
        '\u0508': ["Help", "Help", "", "", 47, 47, False, False],
        '\u0509': ["Pause", "Pause", "", "", 19, 19, False, False],
        '\u050b': ["Props", "Props", "", "", 0, 0, False, False],
        '\u050c': ["Select", "Select", "", "", 41, 41, False, False],
        '\u050d': ["ZoomIn", "ZoomIn", "", "", 0, 0, False, False],
        '\u050e': ["ZoomOut", "ZoomOut", "", "", 0, 0, False, False],
        '\u0601': ["BrightnessDown", "BrightnessDown", "", "", 216, 0, False, False],
        '\u0602': ["BrightnessUp", "BrightnessUp", "", "", 217, 0, False, False],
        '\u0604': ["Eject", "Eject", "", "", 0, 0, False, False],
        '\u0605': ["LogOff", "LogOff", "", "", 0, 0, False, False],
        '\u0606': ["Power", "Power", "", "", 152, 0, False, False],
        '\u0608': ["PrintScreen", "PrintScreen", "", "", 44, 44, False, False],
        '\u060b': ["WakeUp", "WakeUp", "", "", 0, 0, False, False],
        '\u0705': ["Convert", "Convert", "", "", 28, 28, False, False],
        '\u070d': ["NonConvert", "NonConvert", "", "", 29, 29, False, False],
        '\u0711': ["Lang1", "HangulMode", "", "", 21, 21, False, False],
        '\u0712': ["Lang2", "HanjaMode", "", "", 25, 25, False, False],
        '\u0716': ["Lang4", "Hiragana", "", "", 0, 0, False, False],
        '\u0718': ["KanaMode", "KanaMode", "", "", 21, 21, False, False],
        '\u071a': ["Lang3", "Katakana", "", "", 0, 0, False, False],
        '\u071d': ["Lang5", "ZenkakuHankaku", "", "", 0, 0, False, False],
        '\u0801': ["F1", "F1", "", "", 112, 112, False, False],
        '\u0802': ["F2", "F2", "", "", 113, 113, False, False],
        '\u0803': ["F3", "F3", "", "", 114, 114, False, False],
        '\u0804': ["F4", "F4", "", "", 115, 115, False, False],
        '\u0805': ["F5", "F5", "", "", 116, 116, False, False],
        '\u0806': ["F6", "F6", "", "", 117, 117, False, False],
        '\u0807': ["F7", "F7", "", "", 118, 118, False, False],
        '\u0808': ["F8", "F8", "", "", 119, 119, False, False],
        '\u0809': ["F9", "F9", "", "", 120, 120, False, False],
        '\u080a': ["F10", "F10", "", "", 121, 121, False, False],
        '\u080b': ["F11", "F11", "", "", 122, 122, False, False],
        '\u080c': ["F12", "F12", "", "", 123, 123, False, False],
        '\u080d': ["F13", "F13", "", "", 124, 124, False, False],
        '\u080e': ["F14", "F14", "", "", 125, 125, False, False],
        '\u080f': ["F15", "F15", "", "", 126, 126, False, False],
        '\u0810': ["F16", "F16", "", "", 127, 127, False, False],
        '\u0811': ["F17", "F17", "", "", 128, 128, False, False],
        '\u0812': ["F18", "F18", "", "", 129, 129, False, False],
        '\u0813': ["F19", "F19", "", "", 130, 130, False, False],
        '\u0814': ["F20", "F20", "", "", 131, 131, False, False],
        '\u0815': ["F21", "F21", "", "", 132, 132, False, False],
        '\u0816': ["F22", "F22", "", "", 133, 133, False, False],
        '\u0817': ["F23", "F23", "", "", 134, 134, False, False],
        '\u0818': ["F24", "F24", "", "", 135, 135, False, False],
        '\u0a01': ["Close", "Close", "", "", 0, 0, False, False],
        '\u0a02': ["MailForward", "MailForward", "", "", 0, 0, False, False],
        '\u0a03': ["MailReply", "MailReply", "", "", 0, 0, False, False],
        '\u0a04': ["MailSend", "MailSend", "", "", 0, 0, False, False],
        '\u0a05': ["MediaPlayPause", "MediaPlayPause", "", "", 179, 179, False, False],
        '\u0a07': ["MediaStop", "MediaStop", "", "", 178, 178, False, False],
        '\u0a08': ["MediaTrackNext", "MediaTrackNext", "", "", 176, 176, False, False],
        '\u0a09': ["MediaTrackPrevious", "MediaTrackPrevious", "", "", 177, 177, False, False],
        '\u0a0a': ["New", "New", "", "", 0, 0, False, False],
        '\u0a0b': ["Open", "Open", "", "", 43, 43, False, False],
        '\u0a0c': ["Print", "Print", "", "", 0, 0, False, False],
        '\u0a0d': ["Save", "Save", "", "", 0, 0, False, False],
        '\u0a0e': ["SpellCheck", "SpellCheck", "", "", 0, 0, False, False],
        '\u0a0f': ["AudioVolumeDown", "AudioVolumeDown", "", "", 174, 174, False, False],
        '\u0a10': ["AudioVolumeUp", "AudioVolumeUp", "", "", 175, 175, False, False],
        '\u0a11': ["AudioVolumeMute", "AudioVolumeMute", "", "", 173, 173, False, False],
        '\u0b01': ["LaunchApp2", "LaunchApplication2", "", "", 183, 183, False, False],
        '\u0b02': ["LaunchCalendar", "LaunchCalendar", "", "", 0, 0, False, False],
        '\u0b03': ["LaunchMail", "LaunchMail", "", "", 180, 180, False, False],
        '\u0b04': ["MediaSelect", "LaunchMediaPlayer", "", "", 181, 181, False, False],
        '\u0b05': ["LaunchMusicPlayer", "LaunchMusicPlayer", "", "", 0, 0, False, False],
        '\u0b06': ["LaunchApp1", "LaunchApplication1", "", "", 182, 182, False, False],
        '\u0b07': ["LaunchScreenSaver", "LaunchScreenSaver", "", "", 0, 0, False, False],
        '\u0b08': ["LaunchSpreadsheet", "LaunchSpreadsheet", "", "", 0, 0, False, False],
        '\u0b09': ["LaunchWebBrowser", "LaunchWebBrowser", "", "", 0, 0, False, False],
        '\u0b0c': ["LaunchContacts", "LaunchContacts", "", "", 0, 0, False, False],
        '\u0b0d': ["LaunchPhone", "LaunchPhone", "", "", 0, 0, False, False],
        '\u0b0e': ["LaunchAssistant", "LaunchAssistant", "", "", 153, 0, False, False],
        '\u0c01': ["BrowserBack", "BrowserBack", "", "", 166, 166, False, False],
        '\u0c02': ["BrowserFavorites", "BrowserFavorites", "", "", 171, 171, False, False],
        '\u0c03': ["BrowserForward", "BrowserForward", "", "", 167, 167, False, False],
        '\u0c04': ["BrowserHome", "BrowserHome", "", "", 172, 172, False, False],
        '\u0c05': ["BrowserRefresh", "BrowserRefresh", "", "", 168, 168, False, False],
        '\u0c06': ["BrowserSearch", "BrowserSearch", "", "", 170, 170, False, False],
        '\u0c07': ["BrowserStop", "BrowserStop", "", "", 169, 169, False, False],
        '\u0d0a': ["ChannelDown", "ChannelDown", "", "", 0, 0, False, False],
        '\u0d0b': ["ChannelUp", "ChannelUp", "", "", 0, 0, False, False],
        '\u0d12': ["ClosedCaptionToggle", "ClosedCaptionToggle", "", "", 0, 0, False, False],
        '\u0d15': ["Exit", "Exit", "", "", 0, 0, False, False],
        '\u0d22': ["Guide", "Guide", "", "", 0, 0, False, False],
        '\u0d25': ["Info", "Info", "", "", 0, 0, False, False],
        '\u0d2c': ["MediaFastForward", "MediaFastForward", "", "", 0, 0, False, False],
        '\u0d2d': ["MediaLast", "MediaLast", "", "", 0, 0, False, False],
        '\u0d2f': ["MediaPlay", "MediaPlay", "", "", 0, 0, False, False],
        '\u0d30': ["MediaRecord", "MediaRecord", "", "", 0, 0, False, False],
        '\u0d31': ["MediaRewind", "MediaRewind", "", "", 0, 0, False, False],
        '\u0d43': ["LaunchControlPanel", "Settings", "", "", 154, 0, False, False],
        '\u0d4e': ["ZoomToggle", "ZoomToggle", "", "", 251, 251, False, False],
        '\u0e02': ["AudioBassBoostToggle", "AudioBassBoostToggle", "", "", 0, 0, False, False],
        '\u0f02': ["SpeechInputToggle", "SpeechInputToggle", "", "", 0, 0, False, False],
        '\u1001': ["SelectTask", "AppSwitch", "", "", 0, 0, False, False], }


def get_key(r):
    key = Keys[r]
    key = {
        'code': key[0],
        'key': key[1],
        'text': key[2],
        'unmodified': key[3],
        'nativeVirtualKeyCode': key[4],
        'windowsVirtualKeyCode': key[5],
        'shift': key[6],
        'print': key[7],
        'autoRepeat': False,
        'isKeypad': False,
        'isSystemKey': False,
    }
    return key


KeyType = {'KeyDown': 'keyDown',
           'KeyUp': 'keyUp',
           'RawKeyDown': 'rawKeyDown',
           'KeyChar': 'char'}

Modifier = {
    'ModifierNone': 0,
    'ModifierAlt': 1,
    'ModifierCtrl': 2,
    'ModifierMeta': 4,
    'ModifierShift': 8,
}


class DispatchKeyEvent:
    def __init__(self, **kwargs):
        self.type = kwargs.pop('type', None)
        self.modifiers = kwargs.pop('modifiers', None)
        self.text = kwargs.pop('text', None)
        self.unmodifiedText = kwargs.pop('unmodifiedText', None)
        self.timestamp = kwargs.pop('timestamp', None)
        self.keyIdentifier = kwargs.pop('keyIdentifier', None)
        self.code = kwargs.pop('code', None)
        self.key = kwargs.pop('key', None)
        self.windowsVirtualKeyCode = kwargs.pop('windowsVirtualKeyCode', None)
        self.nativeVirtualKeyCode = kwargs.pop('nativeVirtualKeyCode', None)
        self.autoRepeat = kwargs.pop('autoRepeat', None)
        self.isKeypad = kwargs.pop('isKeypad', None)
        self.isSystemKey = kwargs.pop('isSystemKey', None)
        self.location = kwargs.pop('location', None)

    def to_params(self):
        ret = dict()
        for x in self.__dict__.keys():
            if self.__dict__[x] is not None:
                ret[x] = self.__dict__[x]
        # print(ret)
        return ret


def encode_key_events(r):
    if r == '\n':
        r = '\r'
    v = get_key(r)

    keyDown = DispatchKeyEvent(**v)
    keyDown.text = None
    if platform.system() == "darwin":
        keyDown.nativeVirtualKeyCode = 0

    if v['shift']:
        keyDown.modifiers = Modifier['ModifierShift']
    keyUp = copy.deepcopy(keyDown)
    keyDown.type, keyUp.type = KeyType['KeyDown'], KeyType['KeyUp']

    keyChar = None
    if v['print']:
        keyChar = copy.deepcopy(keyDown)
        keyChar.type = KeyType['KeyChar']
        keyChar.text = v['text']
        keyChar.unmodifiedText = v['unmodified']
        keyChar.nativeVirtualKeyCode = ord(r)
        keyChar.windowsVirtualKeyCode = ord(r)
    if keyChar:
        return [keyDown, keyChar, keyUp]
    return [keyDown, keyUp]
