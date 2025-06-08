from datetime import timedelta, datetime
import re

MORNING_SESSION_DURATION = 180
AFTERNOON_MIN_DURATION = 180
AFTERNOON_MAX_DURATION = 240

class Talk:
    def __init__(self, title, duration):
        self.title = title
        self.duration = 5 if duration == "lightning" else int(duration.replace("min", ""))

    def __repr__(self):
        return f"{self.title} {self.duration}min"

def parse_talks(file_path):
    talks = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            match = re.match(r"(.*)\s(\d+min|lightning)$", line)
            if match:
                title, duration = match.groups()
                talks.append(Talk(title, duration))
    return talks

def schedule_session(talks, max_duration):
    scheduled, remaining = [], talks[:]
    time_left = max_duration
    for talk in sorted(talks, key=lambda t: -t.duration):
        if talk.duration <= time_left:
            scheduled.append(talk)
            remaining.remove(talk)
            time_left -= talk.duration
    return scheduled, remaining

def format_time(start_time, duration):
    return (start_time + timedelta(minutes=duration)).time()

def format_schedule(track_num, morning, afternoon):
    result = [f"Track {track_num}:"]
    current_time = datetime.strptime("09:00", "%H:%M")
    for talk in morning:
        result.append(f"{current_time.strftime('%H:%M')} {talk.title} {talk.duration}min")
        current_time += timedelta(minutes=talk.duration)

    result.append("12:00 Almoço")
    current_time = datetime.strptime("13:00", "%H:%M")
    for talk in afternoon:
        result.append(f"{current_time.strftime('%H:%M')} {talk.title} {talk.duration}min")
        current_time += timedelta(minutes=talk.duration)

    networking_time = current_time if current_time.hour >= 16 else datetime.strptime("16:00", "%H:%M")
    result.append(f"{networking_time.strftime('%H:%M')} Evento de Networking\n")
    return "\n".join(result)

def schedule_conference(talks):
    tracks = []
    while talks:
        morning, remaining = schedule_session(talks, MORNING_SESSION_DURATION)
        talks = remaining
        afternoon, talks = schedule_session(talks, AFTERNOON_MAX_DURATION)
        tracks.append((morning, afternoon))
    return tracks

def main():
    talks = parse_talks("proposals.txt")
    tracks = schedule_conference(talks)
    for i, (morning, afternoon) in enumerate(tracks, 1):
        print(format_schedule(i, morning, afternoon))

if __name__ == "__main__":
    main()
