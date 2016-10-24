package com.victor.script.exception;


import java.io.*;

public class CatchMultipleException {

    public static void main(String[] args) {
        FileOutputStream file = null;
        try {
            file = new FileOutputStream("^~!@#$&*()_non-exist");
            ObjectOutputStream oos = new ObjectOutputStream(file);
            oos.defaultWriteObject();
            oos.flush();
        } catch (FileNotFoundException | NotActiveException e){
            System.out.println("swallow FileNotFoundException");
        } catch (IOException e) {
            System.out.println("swallow IOException");
        } finally {
            if(file != null){
                try {
                    file.close();
                } catch (IOException e) {
                    System.out.println("swallow file.close()");
                }
            }
        }
    }
}
