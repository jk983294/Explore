package com.victor.script.json;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;


public class JsonUsage {

    public void readJsonFile() throws IOException {
        InputStream is = this.getClass().getClassLoader().getResourceAsStream("sync.config.json");
        ObjectMapper mapper = new ObjectMapper();
        List<List<String>> groups = mapper.readValue(is, new TypeReference<List<List<String>>>(){});
    }

}
