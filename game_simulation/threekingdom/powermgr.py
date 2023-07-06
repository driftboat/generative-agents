from .power import Power
class PowerMgr:
    def __init__(self):
        self.powers = {}

    def add_power(self, name, power):
        self.powers[name] = power

    def get_power(self, name):
        return self.powers.get(name)

    def create_powers(self):
        self.add_power("魏",Power(1,"魏"))
        self.add_power("蜀",Power(2,"蜀"))
        self.add_power("吴",Power(3,"吴"))
        self.add_power("张鲁",Power(4,"张鲁"))