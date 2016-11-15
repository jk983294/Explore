package com.victor.script.concurrent.time;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.TimeUnit;

/**
 * TimeUnit
 */
public class TimeUnitUsage {

    public static void main(String[] args) throws ParseException {
        testUnitConvert();
        testTimeDuration();
        testSleep();
    }

    static void testUnitConvert(){
        long seconds = 120;
        long minutes = TimeUnit.MINUTES.convert(seconds, TimeUnit.SECONDS);
        System.out.println(seconds + " seconds equals to " + minutes + "minutes.");

        minutes = TimeUnit.SECONDS.toMinutes(seconds);
        System.out.println(seconds + " seconds equals to " + minutes + "minutes.\n");
    }

    static void testTimeDuration() throws ParseException {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd");

        Date beginDate = sdf.parse("2011/12/1");
        Date endDate = sdf.parse("2012/1/9");
        long days = TimeUnit.MILLISECONDS.toDays(endDate.getTime() - beginDate.getTime());

        System.out.println("beginDate: " + sdf.format(beginDate));
        System.out.println("endDate: " + sdf.format(endDate));
        System.out.println("duration: " + days + " days");
    }

    static void testSleep(){
        try {
            TimeUnit.SECONDS.sleep(5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}