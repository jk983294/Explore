package com.victor.sync;


import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.victor.sync.syncer.LocalFileSyncerP2P;
import com.victor.sync.syncer.Syncer;
import org.junit.Ignore;
import org.junit.Test;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class LocalFileSyncerP2PTest {

    @Ignore
    @Test
    public void testDifference() throws IOException {
//        String filePath1 = "F:/Data/dummy/test1";
//        String filePath2 = "F:/Data/dummy/test2";
//        List<String> files = new ArrayList<>();
//        files.add(filePath1);
//        files.add(filePath2);
//        List<List<String>> groups = new ArrayList<>();
//        groups.add(files);

        InputStream is = this.getClass().getClassLoader().getResourceAsStream("sync.config.json");

        ObjectMapper mapper = new ObjectMapper();
        List<List<String>> groups = mapper.readValue(is, new TypeReference<List<List<String>>>(){});

        Syncer syncer = new LocalFileSyncerP2P(groups);
        syncer.setVerbose(true);
        syncer.sync();
    }
}
