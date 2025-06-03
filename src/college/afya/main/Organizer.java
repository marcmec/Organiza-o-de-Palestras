package college.afya.main;

import college.afya.main.utils.Meet;
import college.afya.main.utils.Utils;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class Organizer {

    private final Meet[] meets;

    public Organizer(File file) {
        try {
            this.meets = load(file);
            if(this.meets.length == 0) {
                throw new RuntimeException("Nenhuma reunião foi criada!");
            }
        }catch (IOException e) {
            throw new RuntimeException("Arquivo não encontrado!");
        }
    }

    public Meet[] getMeets() {
        return this.meets;
    }

    public Meet[][] getTracks() {
        Arrays.sort(meets, Meet::comparer);
        List<Meet> current = new ArrayList<>(List.of(this.meets));

        List<List<Meet>> trackA = new ArrayList<>();
        backtrack(current, 0, new ArrayList<>(), 0, trackA, 3 * 60);
        int indexTrackA = new Random(System.currentTimeMillis()).nextInt(trackA.size());
        current.removeAll(trackA.get(indexTrackA));

        List<List<Meet>> trackB = new ArrayList<>();
        backtrack(current, 0, new ArrayList<>(), 0, trackB, 4 * 60);

        return new Meet[][] {
                trackA.get(indexTrackA).toArray(new Meet[0]),
                trackB.getFirst().toArray(new Meet[0])
        };
    }

    public int printTrack(int currentTime, Meet[] track) {
        for(Meet meet : track) {
            System.out.println(Utils.getStringHour(currentTime) + " - " + meet.getTitle() + " [" + meet.getArrangeOfTime() + "min]");
            currentTime += meet.getArrangeOfTime();
        }
        return currentTime;
    }

    private void backtrack(List<Meet> valores, int indice, List<Meet> atual, int soma, List<List<Meet>> out, int period) {
        if (soma > period)
            return;
        if (soma == period) {
            out.add(new ArrayList<>(atual));
            return;
        }
        for (int i = indice; i < valores.size(); i++) {
            Meet valor = valores.get(i);
            atual.add(valor);
            backtrack(valores, i + 1, atual, soma + valor.getArrangeOfTime(), out, period);
            atual.removeLast();
        }
    }

    private Meet[] load(File file) throws IOException {
        List<Meet> meets = new ArrayList<>();
        BufferedReader br = new BufferedReader(new FileReader(file));
        String line;
        while ((line = br.readLine()) != null) {
            String[] words = line.split(" ");
            String time = words[words.length-1];
            String title = line.replace(time, "");
            int arrangeOfTime;
            if(time.equals("lightning")) {
                arrangeOfTime = 5;
            }else {
                arrangeOfTime = Integer.valueOf(time.replace("min", ""));
            }
            meets.add(new Meet(title, arrangeOfTime));
        }
        return meets.toArray(new Meet[0]);
    }

}
