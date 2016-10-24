package com.victor.script.exception;

import java.io.*;

public class RAII {

    public static void main(String[] args) {
        /**
         * resource must implement AutoCloseable
         */
        try (BufferedReader reader = new BufferedReader(new FileReader("^~!@#$&*()_non-exist"))){
            String line = reader.readLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
