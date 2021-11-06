class Factory:
    def __init__(self, data) -> None:
        self.reactions, self.fuel = self.process_data(data)

    def process_data(self, data: str):
        reactions = {}
        lines = data.split("\n")
        for line in lines:
            values = line.split(" => ")
            product = values[1].split()
            reactants = []
            reactors = values[0].split(", ")
            for r in reactors:
                if r == "":
                    continue
                reactant = r.split()
                reactants.append((int(reactant[0]), reactant[1]))
            reactions[(int(product[0]), product[1])] = reactants

            if (1, "FUEL") == (int(product[0]), product[1]):
                fuel = reactants
        return reactions, fuel

    def recurse(self, name, amount, produced, total):
        if name not in produced:
            produced[name] = {"made": 0, "needed": amount}
        else:
            produced[name]["needed"] += amount

        diff = produced[name]["needed"] - produced[name]["made"]
        if diff > 0:
            amount = diff

            for k, v in self.reactions.items():
                if k[1] == name:

                    made = k[0]
                    multiplyer = 1

                    while (made * multiplyer) < amount:
                        multiplyer += 1

                    for (a, n) in v:
                        if n == "ORE":
                            num = a * multiplyer
                            total += num

                        else:
                            total, produced = self.recurse(
                                n, a * multiplyer, produced, total
                            )
                    produced[name]["made"] += made * multiplyer
                    break

        return total, produced

    def how_many_ore(self, produced={}):
        ore_count = 0
        for r in self.fuel:
            name = r[1]
            amount = r[0]
            if name == "ORE":
                ore_count += amount
            else:
                ore_count, produced = self.recurse(name, amount, produced, ore_count)
        # print(produced)
        return ore_count, produced


def part1(data):
    factory = Factory(data)
    return factory.how_many_ore()


def part2(data):
    factory = Factory(data)
    total_ore = 0
    fuel = 0
    produced = {}
    while total_ore < 1000000000000:
        num, produced = factory.how_many_ore(produced)
        for k, v in produced.items():
            produced[k]["made"] -= produced[k]["needed"]
            produced[k]["needed"] = 0
        total_ore += num
        if total_ore > 1000000000000:
            break
        fuel += 1
    return fuel
