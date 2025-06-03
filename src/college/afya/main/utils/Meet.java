package college.afya.main.utils;

public class Meet {

    private final String title;
    private final int arrangeOfTime;

    public Meet(String title, int arrangeOfTime) {
        this.title = title;
        this.arrangeOfTime = arrangeOfTime;
    }

    public String getTitle() {
        return title;
    }

    public int getArrangeOfTime() {
        return arrangeOfTime;
    }


    public int comparer(Meet meet) {
        if(meet.arrangeOfTime > this.arrangeOfTime) {
            return -1;
        }else {
            return 1;
        }
    }
}
