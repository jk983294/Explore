package com.victor.sync.model;


import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class SyncerConstants {

    public static final long DEFAULT_COPY_BUFFER_SIZE = 64 * 1024 * 1024;

    public static final Set<String> suffixNoUpdateNeeded = new HashSet<>();

    static {
        String[] suffix = {"exe", "pdf", "html", "htm", "rar", "zip", "epub", "jpg"};
        suffixNoUpdateNeeded.addAll(Arrays.asList(suffix));
    }

}
