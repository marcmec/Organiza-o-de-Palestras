namespace maurice.domain;

public class Track
{
    public string? Name { get; set; }
    public List<(TimeSpan, string)> Schedule { get; } = new();
    public TimeSpan CurrentTime { get; set; } = new TimeSpan(9, 0, 0);
    private bool addedLunch = false;

    public bool TryAddTalk(Task talk)
    {
        var endTime = CurrentTime.Add(TimeSpan.FromMinutes(talk.Duration));
        if (CurrentTime < new TimeSpan(12, 0, 0) && endTime <= new TimeSpan(12, 0, 0))
        {
            Schedule.Add((CurrentTime, $"{talk.Title} {talk.Duration}min"));
            CurrentTime = endTime;
            return true;
        }
        else if (!addedLunch && CurrentTime < new TimeSpan(13, 0, 0))
        {
            AddFixed("Almoço", new TimeSpan(12, 0, 0));
            CurrentTime = new TimeSpan(13, 0, 0);
            return TryAddTalk(talk);
        }
        else if (CurrentTime >= new TimeSpan(13, 0, 0) && endTime <= new TimeSpan(17, 0, 0))
        {
            Schedule.Add((CurrentTime, $"{talk.Title} {talk.Duration}min"));
            CurrentTime = endTime;
            return true;
        }

        return false;
    }

    public void FinalizeTrack()
    {
        if (!Schedule.Any(s => s.Item2 == "Almoço"))
        {
            AddFixed("Almoço", new TimeSpan(12, 0, 0));
        }

        if (CurrentTime < new TimeSpan(17, 0, 0))
            CurrentTime = new TimeSpan(17, 0, 0);

        Schedule.Add((CurrentTime, "Evento de Networking"));
    }

    private void AddFixed(string title, TimeSpan time)
    {
        Schedule.Add((time, title));
        if (title == "Almoço") addedLunch = true;
    }

    public string Format()
    {
        var output = $"{Name}:\n";
        foreach (var (time, title) in Schedule.OrderBy(s => s.Item1))
        {
            output += $"{time:hh\\:mm} {title}\n";
        }
        return output + "\n";
    }
}
