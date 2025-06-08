import re
from datetime import datetime, timedelta

MORNING_LIMIT = 180
AFTERNOON_MIN = 180
AFTERNOON_MAX = 240

def read_input(filepath):
    talks = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            title, duration = parse_line(line.strip())
            if title and duration:
                talks.append((title, duration))
    return talks

def parse_line(line):
    match = re.match(r"(.+)\s(\d+min|lightning)$", line)
    if not match:
        return None, None
    title, time_str = match.groups()
    duration = 5 if time_str == "lightning" else int(time_str.replace("min", ""))
    return title, duration

def allocate_block(talks, max_duration):
    block, total = [], 0
    used = [False] * len(talks)
    for _ in range(len(talks)):
        for i, (title, duration) in enumerate(talks):
            if not used[i] and total + duration <= max_duration:
                block.append((title, duration))
                used[i] = True
                total += duration
    remaining = [(t, d) for (t, d), u in zip(talks, used) if not u]
    return block, remaining

def format_block(block, start_time):
    result = []
    current = datetime.strptime(start_time, "%H:%M")
    for title, duration in block:
        result.append(f"{current.strftime('%H:%M')} {title} {duration}min")
        current += timedelta(minutes=duration)
    return result, current

def build_tracks(talks):
    tracks = []
    while talks:
        morning, talks = allocate_block(talks, MORNING_LIMIT)
        afternoon, talks = allocate_block(talks, AFTERNOON_MAX)
        tracks.append((morning, afternoon))
    return tracks

def print_schedule(tracks):
    for i, (morning, afternoon) in enumerate(tracks, 1):
        print(f"Track {i}:")
        m_block, _ = format_block(morning, "09:00")
        print("\n".join(m_block))
        print("12:00 Almoço")
        a_block, end_time = format_block(afternoon, "13:00")
        print("\n".join(a_block))
        networking = max(end_time, datetime.strptime("16:00", "%H:%M"))
        print(f"{networking.strftime('%H:%M')} Evento de Networking\n")

if __name__ == "__main__":
    input_talks = read_input("proposals.txt")
    full_tracks = build_tracks(input_talks)
    print_schedule(full_tracks)
