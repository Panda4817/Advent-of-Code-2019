from typing import List


class Moon:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0

    def __str__(self) -> str:
        return f"pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.velocity_x}, y={self.velocity_y}, z={self.velocity_z}>"

    def update_pos(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.z += self.velocity_z

    def update_velocity(self, x, y, z):
        self.velocity_x += x
        self.velocity_y += y
        self.velocity_z += z

    def pot(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kin(self):
        return abs(self.velocity_x) + abs(self.velocity_y) + abs(self.velocity_z)

    def total(self):
        return self.pot() * self.kin()


class Jupiter:
    def __init__(self, data):
        self.moons: List[Moon] = self.process_data(data)
        self.previous_states = []
        self.length = len(self.moons)
        self.max_steps = 1000
        self.current_steps = 0

    def process_data(self, data: str):
        moons = []
        lines = data.split("\n")
        for line in lines:
            values = line.split(", ")
            x = int(values[0].split("=")[-1])
            y = int(values[1].split("=")[-1])
            z = int(values[2].split("=")[-1][:-1])
            moons.append(Moon(x, y, z))
        return moons

    def total_energy(self):
        total = 0
        for moon in self.moons:
            total += moon.total()
        return total

    def compare_moons(self, i, j):
        x = "x"
        y = "y"
        z = "z"
        update_i = {x: 0, y: 0, z: 0}
        update_j = {x: 0, y: 0, z: 0}
        if self.moons[i].x > self.moons[j].x:
            update_i[x] -= 1
            update_j[x] += 1
        elif self.moons[i].x < self.moons[j].x:
            update_i[x] += 1
            update_j[x] -= 1

        if self.moons[i].y > self.moons[j].y:
            update_i[y] -= 1
            update_j[y] += 1
        elif self.moons[i].y < self.moons[j].y:
            update_i[y] += 1
            update_j[y] -= 1

        if self.moons[i].z > self.moons[j].z:
            update_i[z] -= 1
            update_j[z] += 1
        elif self.moons[i].z < self.moons[j].z:
            update_i[z] += 1
            update_j[z] -= 1

        return {i: update_i, j: update_j}

    def apply_gravity(self):
        x = "x"
        y = "y"
        z = "z"
        for i in range(self.length):
            for j in range(i + 1, self.length):
                u = self.compare_moons(i, j)
                self.moons[i].update_velocity(u[i][x], u[i][y], u[i][z])
                self.moons[j].update_velocity(u[j][x], u[j][y], u[j][z])

    def update_positions(self):
        for moon in self.moons:
            moon.update_pos()

    def print_state(self):
        string = ""
        for moon in self.moons:
            # print(moon)
            string += moon.__str__()
        return string

    def match_prev_state(self, current_state):
        setA = set(self.previous_states)
        setB = set([current_state])
        common = setA.intersection(setB)
        if len(common) == 1:
            return True
        return False

    def simulate(self):
        self.print_state()
        while self.current_steps != self.max_steps:
            # print()
            self.apply_gravity()

            self.update_positions()

            self.current_steps += 1
            self.print_state()

        return self.total_energy()

    def simulate_prev_state(self):
        state = self.print_state()
        if self.match_prev_state(state):
            return self.current_steps
        else:
            self.previous_states.append(state)

        while True:
            # print(self.current_steps)
            self.apply_gravity()

            self.update_positions()

            self.current_steps += 1

            state = self.print_state()
            if self.match_prev_state(state):
                break
            else:
                self.previous_states.append(state)

        return self.current_steps


def part1(data):
    jupiter = Jupiter(data)
    ans = jupiter.simulate()
    return ans


def part2(data):
    jupiter = Jupiter(data)
    ans = jupiter.simulate_prev_state()
    return ans
