from datetime import datetime, timedelta

def parse_duration(s):
    s = s.strip().lower()
    if s == "lightning":
        return 5
    elif s.endswith("min"):
        return int(s[:-3])
    else:
        return 0 

def format_time(dt):
    return dt.strftime("%H:%M")

def schedule_talks(talks):
    morning_start = datetime.strptime("09:00", "%H:%M")
    afternoon_start = datetime.strptime("13:00", "%H:%M")

    morning_time_left = 180
    afternoon_time_left = 210

    schedule = []

    current_time = morning_start

    i = 0
    n = len(talks)

    while i < n:
        dur = parse_duration(talks[i].split()[-1])
        if dur <= morning_time_left:
            schedule.append((format_time(current_time), talks[i]))
            current_time += timedelta(minutes=dur)
            morning_time_left -= dur
            i += 1
        else:
            break

    schedule.append(("12:00", "Almoço"))
    current_time = afternoon_start
    while i < n:
        dur = parse_duration(talks[i].split()[-1])
        if dur <= afternoon_time_left:
            schedule.append((format_time(current_time), talks[i]))
            current_time += timedelta(minutes=dur)
            afternoon_time_left -= dur
            i += 1
        else:
            break
    schedule.append(("16:30", "Evento de Networking"))

    return schedule, i

def main():
    with open("proposals.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    talks = [line for line in lines if line.lower() not in ("almoço", "evento de networking")]
    track_a_schedule, index_a = schedule_talks(talks)

    track_b_schedule, index_b = schedule_talks(talks[index_a:])

    print("Track A:")
    for time, talk in track_a_schedule:
        print(f"{time} {talk}")

    print("\nTrack B:")
    for time, talk in track_b_schedule:
        print(f"{time} {talk}")

if __name__ == "__main__":
    main()


