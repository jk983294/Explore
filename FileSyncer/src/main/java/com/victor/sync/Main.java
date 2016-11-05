package com.victor.sync;


import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.victor.sync.syncer.LocalFileSyncerMasterSlave;
import com.victor.sync.syncer.LocalFileSyncerP2P;
import com.victor.sync.syncer.Syncer;
import org.apache.commons.cli.*;
import org.apache.log4j.Logger;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class Main {

    private static final Logger logger = Logger.getLogger(Main.class);

    public static void main(String[] args) {
        Option local = new Option("l", "Local Mode");
        Option ms = new Option("ms", "Master Slave Mode");
        Option p2p = new Option("p2p", "P2P Mode");
        Option reverse = new Option("r", "last file is master");
        Option verbose = new Option("v", "verbose");

        Options options = new Options();
        options.addOption( local );
        options.addOption( ms );
        options.addOption( p2p );
        options.addOption( reverse );
        options.addOption( verbose );

        CommandLineParser parser = new GnuParser();
        CommandLine cmd = null;
        try {
            cmd = parser.parse( options, args );
        }
        catch( ParseException exp ) {
            logger.error("Parsing Arguments failed!" , exp);
        }

        if(cmd != null && cmd.hasOption("l")) {
            InputStream is = cmd.getClass().getClassLoader().getResourceAsStream("sync.config.json");

            ObjectMapper mapper = new ObjectMapper();
            List<List<String>> groups = null;

            try {
                groups = mapper.readValue(is, new TypeReference<List<List<String>>>(){});
            } catch (IOException e) {
                logger.error("Read Config failed!" , e);
            }

            boolean isVerbose = false;
            if(cmd.hasOption("v")){
                isVerbose = true;
            }

            Syncer syncer = null;

            if(cmd.hasOption("ms")) {
                boolean isLastMaster = false;
                if(cmd.hasOption("r")){
                    isLastMaster = true;
                }
                syncer = new LocalFileSyncerMasterSlave(groups, isLastMaster);
            } else if(cmd.hasOption("p2p")) {
                syncer = new LocalFileSyncerP2P(groups);
            }

            if(syncer != null){
                syncer.setVerbose(isVerbose);
                syncer.sync();
            }

        }
    }

}
