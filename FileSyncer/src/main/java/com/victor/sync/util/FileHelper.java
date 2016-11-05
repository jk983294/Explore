package com.victor.sync.util;

import com.victor.sync.model.FileTree;
import com.victor.sync.model.SyncerConstants;
import org.apache.commons.lang3.StringUtils;
import org.apache.log4j.Logger;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.channels.FileChannel;


/**
 * Utility class for synchronizing files/directories.
 */
public abstract class FileHelper {

    private static final Logger logger = Logger.getLogger(FileHelper.class);

    public static void copyFile(String src, String dest) {
        copyFile(new File(src), new File(dest));
    }

    public static void copyFile(File srcFile, File destFile) {
        if(!destFile.exists()){
            File parent = destFile.getParentFile();
            if(!parent.exists()){
                parent.mkdirs();
            }
        }

        String src = "", dest = "";

        try (FileInputStream is = new FileInputStream( srcFile );
             FileOutputStream os = new FileOutputStream( destFile, false )) {
            src = srcFile.getCanonicalPath();
            dest = destFile.getCanonicalPath();
            FileChannel iChannel = is.getChannel();
            FileChannel oChannel = os.getChannel();
            long doneBytes = 0L;
            long todoBytes = srcFile.length();
            while ( todoBytes != 0L ) {
                long iterationBytes = Math.min( todoBytes, SyncerConstants.DEFAULT_COPY_BUFFER_SIZE );
                long transferredLength = oChannel.transferFrom( iChannel, doneBytes, iterationBytes );
                if ( iterationBytes != transferredLength ) {
                    throw new IOException("Error during file transfer: expected " + iterationBytes
                            + " bytes, only " + transferredLength + " bytes copied.");
                }
                doneBytes += transferredLength;
                todoBytes -= transferredLength;
            }

            boolean successTimestampOp = destFile.setLastModified( srcFile.lastModified() );
            if ( !successTimestampOp ) {
                logger.warn(String.format("Could not change timestamp for %s ", src));
            }
        } catch (IOException e) {
            logger.error(String.format("Could not copy file from %s -> %s ", src, dest), e);
        }
    }

    public static void delete(String file) {
        delete(new File(file));
    }

    public static void delete(File file) {
        if ( file.isDirectory() ) {
            for ( File subFile : file.listFiles() ) {
                delete( subFile );
            }
        }
        if ( file.exists() ) {
            if ( !file.delete() ) {
                logger.warn(String.format("Could not delete file for %s ", file.getAbsolutePath()));
            }
        }
    }

    public static void collect(FileTree tree){
        try {
            tree.collect();
        } catch (IOException e) {
            logger.error("error when collect for " + tree.getRoot(), e);
        }
    }

    public static boolean isUpdateNeeded(String path){
        if(StringUtils.isEmpty(path)) return true;

        int dot = path.lastIndexOf(".");
        if(dot < 0) return true;

        String suffix = path.substring(dot + 1).toLowerCase();
        return !SyncerConstants.suffixNoUpdateNeeded.contains(suffix);
    }
}
