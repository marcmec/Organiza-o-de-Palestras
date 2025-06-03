package college.afya.main;

import college.afya.main.utils.Meet;
import college.afya.main.utils.Utils;

import java.io.File;

public class Main {

    public static void main(String[] args) {
        File file = new File("proposals.txt");
        Organizer organizer = new Organizer(file);
        Meet[][] tracks = organizer.getTracks();

        int currentTime = 60 * 9 ;
        currentTime = organizer.printTrack(currentTime, tracks[0]);
        System.out.println(Utils.getStringHour(currentTime) + " - Time to lunch");
        currentTime += 60;
        currentTime = organizer.printTrack(currentTime, tracks[1]);
        System.out.println(Utils.getStringHour(currentTime) + " - Evento de Networking");
    }

}
