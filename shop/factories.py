from decimal import Decimal


class ChangeFactory:
    @staticmethod
    def calculate(balance: Decimal, denominations):
        result = []

        for d in denominations:
            count = int(balance // d.value)
            if count:
                result.append((d.value, count))
                balance -= d.value * count

        return result
