import heapq
import sys

COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOMS = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
ROOM_INDEX = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
ALLOWED_HALL_POS = [0, 1, 3, 5, 7, 9, 10]

def parse(lines):
    depth = len(lines) - 2
    rooms = []
    for i in range(4):
        col = []
        for j in range(2, 2 + depth):
            col.append(lines[j][3 + 2*i])
        rooms.append(tuple(col))
    return ("." * 11, tuple(rooms))

def is_goal(state):
    hallway, rooms = state
    if any(c != '.' for c in hallway):
        return False
    for i, room in enumerate(rooms):
        goal = "ABCD"[i]
        for c in room:
            if c != goal:
                return False
    return True

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
        for direction in (-1, 1):
            p = pos
            while 0 <= p + direction < 11 and hallway[p + direction] == '.':
                p += direction
                if p in ALLOWED_HALL_POS:
                    new_hallway = list(hallway)
                    new_hallway[p] = c
                    new_rooms = [list(r) for r in rooms]
                    new_rooms[i][d] = '.'
                    dist = abs(p - pos) + d + 1
                    new_state = (''.join(new_hallway), tuple(tuple(rr) for rr in new_rooms))
                    moves.append((new_state, dist * COST[c]))

    for i, c in enumerate(hallway):
        if c == '.':
            continue
        target_room_idx = ROOM_INDEX[c]
        target_pos = ROOMS[c]
        room = rooms[target_room_idx]
        if any(x != '.' and x != c for x in room):
            continue
        step = 1 if target_pos > i else -1
        blocked = False
        for j in range(i + step, target_pos + step, step):
            if 0 <= j < 11 and hallway[j] != '.' and j not in [2, 4, 6, 8]:
                blocked = True
                break
        if blocked:
            continue
        for d in reversed(range(depth)):
            if room[d] == '.':
                new_hallway = list(hallway)
                new_hallway[i] = '.'
                new_rooms = [list(r) for r in rooms]
                new_rooms[target_room_idx][d] = c
                dist = abs(target_pos - i) + d + 1
                new_state = (''.join(new_hallway), tuple(tuple(rr) for rr in new_rooms))
                moves.append((new_state, dist * COST[c]))
                break
    return moves

def solve(lines):
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
    lines = [line.rstrip('\n') for line in sys.stdin]
    lines = [line for line in lines if line.strip() != ''][:5]
    result = solve(lines)
    print(result)

if __name__ == "__main__":
    main()
