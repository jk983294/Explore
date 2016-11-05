package com.victor.sync;


import com.victor.sync.model.FileTreeDiff;
import org.junit.Ignore;
import org.junit.Test;

import java.io.IOException;

public class FileTreeDiffTest {

    @Ignore
    @Test
    public void testDifference() throws IOException {
        String filePath1 = "F:/Data/dummy/test1";
        String filePath2 = "F:/Data/dummy/test2";
        FileTreeDiff diff = new FileTreeDiff(filePath1, filePath2);
        diff.difference();
        System.out.println(diff);
    }
}
