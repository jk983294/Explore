package com.victor.sync;


import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.victor.sync.syncer.LocalFileSyncerMasterSlave;
import com.victor.sync.syncer.Syncer;
import org.junit.Ignore;
import org.junit.Test;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class LocalFileSyncerMasterSlaveTest {

    @Ignore
    @Test
    public void testDifference() throws IOException {
        InputStream is = this.getClass().getClassLoader().getResourceAsStream("sync.config.json");

        ObjectMapper mapper = new ObjectMapper();
        List<List<String>> groups = mapper.readValue(is, new TypeReference<List<List<String>>>(){});

        Syncer syncer = new LocalFileSyncerMasterSlave(groups, true);
        syncer.setVerbose(true);
        syncer.sync();
    }
}
