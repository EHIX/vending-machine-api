from collections import Counter

class VendingMachine():
    def __init__(self, coin_count):
        self.denominations = [1, 2, 5, 10, 20, 50, 100, 200] # in pence
        try:
            assert isinstance(coin_count, list)
        except AssertionError:
            print("Warning: input invalid, continuing without change")
            coin_count = [0] * 8
        try:
            assert len(coin_count) == len(self.denominations)
        except AssertionError:
            print("Warning: number of denominations inserted incorrect or missing entries")
            if len(coin_count) < len(self.denominations):
                for i in range(len(self.denominations)-len(coin_count)):
                    coin_count.append(0)
                print("Missing entries have been noted")
            elif len(coin_count) > len(self.denominations):
                print("Surplus entries have been ignored")
        self.cash = dict(zip(self.denominations, coin_count))
        self.collected = self.reset_collection()
        self.inventory = {0:('Cola 330ml', 0.95),
                  1:('Lemonade 330ml', 0.95),
                  2:('Water 500ml', 1.15),
                  3:('Orangeade 500ml', 1.65)}

    def reset_collection(self):
        return dict(zip(self.denominations, [0] * len(self.denominations)))

    def sum_cash(self, v = 0):
        return ("{:.2f}".format(sum([(k * v) for k, v in self.cash.items()]) / 100))

    def sum_collected(self, v = 0):
        return ("{:.2f}".format(sum([(k * v) for k, v in self.collected.items()]) / 100))

    def print_inventory(self):
        for option, (name, price) in self.inventory.items():
            print("{0:<5}{1:20}£{2}".format(option, name, price))

    def insert_coin(self, selection):
        response = ""
        data = "invalid"
        if selection in range(len(self.denominations)):
            self.collected[self.denominations[selection]] += 1
            response = "success"
            data = "{0:.2f}".format(self.denominations[selection]/100)
        else:
            response += "error"
        return {response : data}

    def terminate(self):
        response = ""
        number_of_coins = sum(self.collected.values())
        if number_of_coins > 0:
            response += "refund"
            coins = ["{:.2f}".format(k/100) for k, v in self.collected.items() for j in range(v)]
            data = dict(zip(range(len(coins)), coins))
            self.collected = self.reset_collection()
        else:
            response += "error"
            data = None
        return {response: {"coins": data}}

    def calculate_change(self, change):
        coin_count = [0] * (change + 1)
        coins_used = [0] * (change + 1)
        for i in range(change + 1):
            count = i
            new_coin = 1
            for j in [c for c in self.denominations if c <= i]:
                if coin_count[i-j] + 1 < count:
                    count = coin_count[i-j] + 1
                    new_coin = j
            coin_count[i] = count
            coins_used[i] = new_coin

        optimum_coins=[]
        coin = change
        while coin > 0:
            this_coin = coins_used[coin]
            optimum_coins.append(this_coin)
            coin = coin - this_coin
        return optimum_coins

    def increase_total(self):
        for k, v in self.collected.items():
            self.cash[k] += v

    def decrease_total(self, coins, report=True):
        data = []
        for c in coins:
            self.cash[c] -= 1
            data.append("{:.2f}".format(c/100))
        if data:
            return dict(zip(range(len(data)), data))

    def can_allocate(self, coins):
        flag = True
        count = Counter(coins)
        missing_coins = [k for k in count.keys() if self.cash[k] < count[k]]
        if missing_coins:
            flag = False
        return flag

    def select(self, option):
        response = ''
        data = {}
        transact = True
        if option in self.inventory.keys():
            item_name, price = self.inventory[option]
            collected_total = sum([(k * v) for k, v in self.collected.items()]) / 100
            if collected_total < price:
                transact = False
                response += "underfunded"
                data = None
                # print("Deposited £{0:.2f}, item costs £{1:.2f}".format(collected_total, price))
            else:
                # Increase amounts in cash, inserted coins can be used when making change
                self.increase_total()
                change_amount = int(round(collected_total - price, 2) * 100)
                if change_amount:
                    # Calculate combination of coins required
                    coins_used = self.calculate_change(change_amount)
                    # Check whether combination of coins can be dispensed
                    if self.can_allocate(coins_used):
                        change = self.decrease_total(coins_used)
                        data.update({"change": change})
                    else:
                        # Cannot dispense correct change, cancelling transation
                        self.decrease_total([k for (k, v) in self.collected.items() for j in range(v)], False)
                        response += "transaction"
                        data = self.terminate()
                        transact = False
                if transact:
                    # Reset collected amount of cash, dispense item
                    self.collected = self.reset_collection()
                    data.update({"item" : item_name.lower()})
                    response += "transation"
        else:
            transact = False
            response += "invalid"
        return {"success" if transact else "error" : {response : data}}
