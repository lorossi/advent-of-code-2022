from re import match


def parse_input() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    with open("input", "r") as f:
        lines = f.read().splitlines()
    regex = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"

    sensors = []
    beacons = []
    for line in lines:
        sx, sy, bx, by = map(int, match(regex, line).groups())
        sensors.append((sx, sy))
        beacons.append((bx, by))

    return sensors, beacons


def part_one() -> int:
    sensors, beacons = parse_input()
    unique_beacons = set(beacons)
    occupied = set()

    y = 2000000
    for s in zip(sensors, beacons):
        sx, sy = s[0]
        bx, by = s[1]

        # distance between sensor and beacon
        dist = abs(sx - bx) + abs(sy - by)
        # distance between sensor and line
        dh = abs(sy - y)
        # find all sensors whose dist is in range of line y
        if dist >= dh:
            # check all values in the y that are in range of the sensor
            dx = dist - dh
            occupied.add((sx - dx, sx + dx))

    lines = sorted(occupied, key=lambda x: x[0])
    # merge lines
    i = 0
    while i < len(lines) - 1:
        if lines[i][1] >= lines[i + 1][0]:
            lines[i] = (lines[i][0], max(lines[i][1], lines[i + 1][1]))
            lines.pop(i + 1)
        else:
            i += 1

    answer = 0
    for line in lines:
        answer += line[1] - line[0] + 1

    for b in unique_beacons:
        if b[1] == y and any(b[0] > line[0] and b[0] < line[1] for line in lines):
            answer -= 1

    return answer


def create_line(m: int, x: int, y: int) -> tuple[float, float]:
    q = y - m * x
    return m, q


def part_two() -> int:
    sensors, beacons = parse_input()
    positive_lines = set()  # y = mx + q
    negative_lines = set()  # y = -mx + q

    for s in zip(sensors, beacons):
        sx, sy = s[0]
        bx, by = s[1]

        # add to the set a list of lines that are just outside the area
        dist = abs(sx - bx) + abs(sy - by) + 1
        # create a line for each sensor
        positive_lines.add(create_line(1, sx - dist, sy))
        positive_lines.add(create_line(1, sx + dist, sy))
        negative_lines.add(create_line(-1, sx, sy - dist))
        negative_lines.add(create_line(-1, sx, sy + dist))

    # compute all the intersections of the lines
    intersections = set()
    for p in positive_lines:
        for n in negative_lines:
            x = (n[1] - p[1]) / 2
            y = p[0] * x + p[1]

            if x < 0 or x > 4000000:
                continue
            if y < 0 or y > 4000000:
                continue

            intersections.add((int(x), int(y)))

    for px, py in intersections:
        found = False

        # check if the point is in range of all sensors
        for s in zip(sensors, beacons):
            sx, sy = s[0]
            bx, by = s[1]

            # distance between sensor and beacon
            beacon_d = abs(sx - bx) + abs(sy - by)
            # distance between sensor and point
            point_d = abs(sx - px) + abs(sy - py)

            if point_d <= beacon_d:
                found = True
                break

        if not found:
            print(px, py)
            return px * 4000000 + py


def main():
    print(f"Part one: {part_one()}")
    print(f"Part two: {part_two()}")


if __name__ == "__main__":
    main()
