
import heapq
import sys

COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOMS = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
ROOM_INDEX = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
ALLOWED_HALL_POS = [0, 1, 3, 5, 7, 9, 10]

def parse(lines):
    norm = [line.ljust(13, ' ') for line in lines]
    depth = len(norm) - 3  # 2 для 5 строк, 4 для 7 строк
    rooms = []
    for i in range(4):
        col = []
        for j in range(2, 2 + depth):
            col.append(norm[j][3 + 2 * i])
        rooms.append(tuple(col))
    return ("." * 11, tuple(rooms))

def is_goal(state):
    hallway, rooms = state
    for i, room in enumerate(rooms):
        goal = "ABCD"[i]
        if any(c != goal for c in room):
            return False
    return hallway == "..........."

def next_moves(state):
    hallway, rooms = state
    moves = []
    depth = len(rooms[0])

    for i, room in enumerate(rooms):
        goal_type = "ABCD"[i]
        if all(c == '.' or c == goal_type for c in room):
            continue
        for d, c in enumerate(room):
            if c != '.':
                break
        pos = ROOMS[goal_type]
        for dir in (-1, 1):
            p = pos
            while 0 <= p + dir < 11 and hallway[p + dir] == '.':
                p += dir
                if p in ALLOWED_HALL_POS:
                    new_h = list(hallway)
                    new_h[p] = c
                    new_rooms = [list(r) for r in rooms]
                    new_rooms[i][d] = '.'
                    dist = abs(p - pos) + d + 1
                    moves.append((
                        (''.join(new_h), tuple(tuple(rr) for rr in new_rooms)),
                        dist * COST[c]
                    ))
    for i, c in enumerate(hallway):
        if c == '.':
            continue
        target_room = ROOM_INDEX[c]
        target_pos = ROOMS[c]
        if any(x != '.' and x != c for x in rooms[target_room]):
            continue
        step = 1 if target_pos > i else -1
        if all(hallway[j] == '.' for j in range(i + step, target_pos + step, step) if j != target_pos):
            for d in reversed(range(depth)):
                if rooms[target_room][d] == '.':
                    new_h = list(hallway)
                    new_h[i] = '.'
                    new_rooms = [list(r) for r in rooms]
                    new_rooms[target_room][d] = c
                    dist = abs(target_pos - i) + d + 1
                    moves.append((
                        (''.join(new_h), tuple(tuple(rr) for rr in new_rooms)),
                        dist * COST[c]
                    ))
                    break
    return moves

def solve(lines: list[str]) -> int:
    start = parse(lines)
    pq = [(0, start)]
    best = {start: 0}

    while pq:
        cost, state = heapq.heappop(pq)
        if is_goal(state):
            return cost
        if cost > best[state]:
            continue
        for nstate, move_cost in next_moves(state):
            new_cost = cost + move_cost
            if new_cost < best.get(nstate, float('inf')):
                best[nstate] = new_cost
                heapq.heappush(pq, (new_cost, nstate))
    return -1

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    result = solve(lines)
    print(result)

if __name__ == "__main__":
    main()
