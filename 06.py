from collections import deque


def process_data(data):
    lines = data.split("\n")
    orbit_map = {}
    for line in lines:
        k, v = line.split(")")
        if k in orbit_map:
            orbit_map[k].append(v)
        else:
            orbit_map[k] = [v]
    return orbit_map


def recurse_through_planets(total, planet_list, orbit_map):
    for planet in planet_list:
        total += 1
        if planet in orbit_map:
            total = recurse_through_planets(total, orbit_map[planet], orbit_map)
    return total


def part1(data):
    orbit_map = process_data(data)
    total_orbits = 0

    for k, v in orbit_map.items():
        total_orbits = recurse_through_planets(total_orbits, v, orbit_map)

    return total_orbits


def part2(data):
    orbit_map = process_data(data)
    dest, start = None, None
    for k, v in orbit_map.items():
        if "SAN" in v:
            dest = k

        if "YOU" in v:
            start = k

        if dest and start:
            break

    q = deque([(start, 0)])
    visited = set()
    visited.add(start)

    while q:
        planet, steps = q.popleft()
        visited.add(planet)
        if planet == dest:
            minimum_transfers = steps
            break

        for k, v in orbit_map.items():
            if planet in v and k not in visited:
                q.append((k, steps + 1))

            elif k == planet:
                for pl in v:
                    if pl not in visited:
                        q.append((pl, steps + 1))

    return minimum_transfers
