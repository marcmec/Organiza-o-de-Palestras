using System.Text.RegularExpressions;
using maurice.domain;

public class Program
{
    static void Main()
    {
        var path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Assets", "proposals.txt");
        var lines = File.ReadAllLines(path);
        var talks = new List<maurice.domain.Task>();

        foreach (var line in lines)
        {
            if (string.IsNullOrWhiteSpace(line)) continue;

            var match = Regex.Match(line, @"(.*)\s(\d+min|lightning)$");
            if (!match.Success) continue;

            string title = match.Groups[1].Value.Trim();
            string durationStr = match.Groups[2].Value;

            int duration = durationStr == "lightning" ? 5 : int.Parse(durationStr.Replace("min", ""));
            talks.Add(new maurice.domain.Task { Title = title, Duration = duration });
        }

        var sortedTalks = talks.OrderByDescending(t => t.Duration).ToList();
        var tracks = new List<Track>();
        int trackCount = 0;

        while (sortedTalks.Count > 0)
        {
            var track = new Track { Name = $"Track {(char)('A' + trackCount)}" };
            var remainingTalks = new List<maurice.domain.Task>(sortedTalks);

            foreach (var talk in remainingTalks)
            {
                if (track.TryAddTalk(talk))
                    sortedTalks.Remove(talk);
            }

            track.FinalizeTrack();
            tracks.Add(track);
            trackCount++;
        }

        string result = "Palestras:\n\n";
        foreach (var track in tracks)
        {
            result += track.Format();
        }

        string baseDir = AppDomain.CurrentDomain.BaseDirectory;
        string projectRoot = Path.GetFullPath(Path.Combine(baseDir, "..", "..", ".."));
        string outputDir = Path.Combine(projectRoot, "output");
        string fileName = $"agenda_formatada.txt";
        string outputPath = Path.Combine(outputDir, fileName);

        if (File.Exists(outputPath))
        {
            string timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
            fileName = $"agenda_formatada.txt{timestamp}";
            outputPath = Path.Combine(outputDir, fileName);
        }

        File.WriteAllText(outputPath, result);
        Console.Clear();
    }
}
