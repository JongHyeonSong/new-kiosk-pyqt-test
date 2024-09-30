class UserButton(QPushButton):

    def __init__(self):
        super(UserButton, self).__init__()
        self._prop = 'false'


        with open('test3.css', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def getter(self):
        return self._prop

    def setter(self, val):
        if self._prop == val:
            return
        self._prop = val
        self.style().polish(self)

    prop = Property(str, fget=getter, fset=setter)