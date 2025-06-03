package college.afya.main.utils;

public class Utils {

    public static String getStringHour(int value) {
        int hour = value / 60;
        int minute = value % 60;
        return "[" + hour + ":" + String.format("%02d", minute) + "]";
    }

}
