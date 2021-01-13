class Robot1:
    def __init__(self, power):
        self._power = power

    power = property()

    @power.setter  # обрабатывает приходящее значение и устанавливает в self._power
    def power(self, value):
        if value < 0:
            self._power = 0
        else:
            self._power = value

    @power.getter  # берет существующее значение из self._power
    def power(self):
        return self._power

    @power.deleter  # выполняет действие при удалении значения self._power
    def power(self):
        print("If you delete power, it's make robot useless")
        del self._power


terminator = Robot1(100)
terminator.power = -20
print(terminator.power)
del terminator.power

# если @property изменяет только чтение атрибута, то его можно записать проще


class Robot2:
    def __init__(self, power):
        self._power = power

    @property
    def power(self):
        # любые полезные действия с power
        return self._power
