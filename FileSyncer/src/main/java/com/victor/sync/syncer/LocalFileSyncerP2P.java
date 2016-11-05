package com.victor.sync.syncer;

import com.victor.sync.model.FileNode;
import com.victor.sync.model.FileTree;
import com.victor.sync.model.FileTreeDiff;
import com.victor.sync.util.FileHelper;
import org.apache.commons.collections.CollectionUtils;
import org.apache.log4j.Logger;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 * P2P means after sync, all file tree will be identical, no file get removed, data is the sum of all sub file trees
 */
public class LocalFileSyncerP2P implements Syncer {

    private static final Logger logger = Logger.getLogger(LocalFileSyncerP2P.class);

    public List<List<FileTree>> fileTreeGroups = new ArrayList<>();

    public boolean verbose = false;

    public LocalFileSyncerP2P(List<List<String>> groups) {
        if(CollectionUtils.isNotEmpty(groups)){
            for(List<String> paths : groups){
                if(CollectionUtils.isNotEmpty(groups)){
                    List<FileTree> trees = new ArrayList<>();
                    for(String path : paths){
                        trees.add(new FileTree(path));
                    }
                    fileTreeGroups.add(trees);
                }
            }
        }
    }

    @Override
    public void sync() {
        for(List<FileTree> fileTrees : fileTreeGroups){
            for(FileTree fileTree : fileTrees){
                FileHelper.collect(fileTree);
            }
        }

        for(List<FileTree> fileTrees : fileTreeGroups){
            for(int i = 0; i < fileTrees.size(); i++){
                for(int j = i + 1; j < fileTrees.size(); j++){
                    sync(fileTrees.get(i), fileTrees.get(j));
                    sync(fileTrees.get(j), fileTrees.get(i));
                }
            }
        }
    }

    @Override
    public void setVerbose(boolean verbose) {
        this.verbose = verbose;
    }

    private void sync(FileTree source, FileTree target) {
        FileTreeDiff diff = new FileTreeDiff(source, target);
        diff.difference();

        for (FileNode sourceNode : diff.newAddedInSource){
            FileHelper.copyFile(sourceNode.getPath(), target.getRoot() + sourceNode.relativePath);
        }

        for (FileNode sourceNode : diff.updatedInSource){
            FileHelper.copyFile(sourceNode.getPath(), target.getRoot() + sourceNode.relativePath);
        }

        logger.info(String.format("%s -> %s %d created, %d updated", source.getRoot(), target.getRoot(),
                diff.newAddedInSource.size(), diff.updatedInSource.size()));

        if(verbose){
            if(diff.newAddedInSource.size() > 0){
                logger.info("\ncopied:");
                for (FileNode sourceNode : diff.newAddedInSource){
                    logger.info(target.getRoot() + sourceNode.relativePath);
                }
            }

            if(diff.updatedInSource.size() > 0){
                logger.info("\nupdated:");
                for (FileNode sourceNode : diff.updatedInSource){
                    logger.info(target.getRoot() + sourceNode.relativePath);
                }
            }
        }
    }

}
