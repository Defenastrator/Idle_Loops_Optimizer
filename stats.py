def arith_total(x: int) -> int:
    return ((x+1)*x)//2


class ProgressBar(object):
    __slots__ = ("base_exp_requirement", "level_cap", "_exp", "_level")

    def __init__(self, level,
                 experience: float = None,
                 base_exp_requirement: int = 100,
                 level_cap: int = None):
        self.base_exp_requirement = base_exp_requirement
        self.level_cap = float("inf") if level_cap is None else level_cap
        if experience is None:
            if isinstance(level, tuple):
                level, experience = level
            else:
                level, experience = 0, experience
        self.lvl = level
        self.exp = experience

    def _bound_exp(self):
        if self._exp < 0:
            while self._exp < 0:
                self._exp += self.prev_level_exp
                self._level -= 1
                if self.level == 0:
                    if self._exp < 0:
                        self._exp = 0
                    break
        elif self._level == self.level_cap:
            self._exp = 0
        else:
            nx_exp = self.level_up_exp
            while self._exp >= nx_exp:
                self._exp -= nx_exp
                self._level += 1
                if self._level == self.level_cap:
                    self._exp = 0.0
                    break
                nx_exp = self.level_up_exp

    @property
    def lvl(self) -> int:
        return self._level

    @lvl.setter
    def lvl(self, lvl):
        if lvl < 0 or int(lvl) != lvl:
            raise ValueError("level must be an integer >= 0")
        self._level = min(int(lvl), self.level_cap)
        self._bound_exp()

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, val):
        self._exp = val
        self._bound_exp()

    level = lvl
    experience = exp

    @property
    def total_exp(self):
        return arith_total(self.level) * self.exp

    @total_exp.setter
    def total_exp(self, value):
        self._level = 0
        self.exp = value

    @property
    def level_up_exp(self) -> int:
        return (self.level + 1) * self.base_exp_requirement

    @property
    def prev_level_exp(self) -> int:
        return self.level * self.base_exp_requirement

    @property
    def percent(self):
        return self.exp / self.level_up_exp

    def __iadd__(self, other):
        self.exp += other

    def __isub__(self, other):
        self.exp -= other

    def __int__(self):
        return self.level

    def __float__(self):
        return self.total_exp

    def tuple(self):
        return self.level, self.exp

    def _compare_value(self, other):
        if isinstance(other, (tuple, ProgressBar)):
            return self.tuple()
        elif isinstance(other, int):
            return self.level
        elif isinstance(other, float):
            return self.total_exp
        else:
            return NotImplemented

    def __eq__(self, o):
        c = self._compare_value(o)
        return c if c is NotImplemented else c == o

    def __ne__(self, o):
        c = self._compare_value(o)
        return c if c is NotImplemented else c != o

    def __lt__(self, o):
        c = self._compare_value(o)
        return c if c is NotImplemented else c < o

    def __le__(self, o):
        c = self._compare_value(o)
        return c if c is NotImplemented else c <= o

    def __gt__(self, o):
        c = self._compare_value(o)
        return c if c is NotImplemented else c > o

    def __ge__(self, o):
        c = self._compare_value(o)
        return c if c is NotImplemented else c >= o

    def __str__(self):
        return f"(level: {}"


class Stat(object):
    __slots__ = ("name", "exp", "talent", "souls")

    def __init__(self, name, exp, talent, stones):
        self.name = name
