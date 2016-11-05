package com.victor.sync.syncer;

import com.victor.sync.model.FileNode;
import com.victor.sync.model.FileTree;
import com.victor.sync.model.FileTreeDiff;
import com.victor.sync.util.FileHelper;
import org.apache.commons.collections.CollectionUtils;
import org.apache.log4j.Logger;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * MasterSlave means after sync, all slave file tree will be identical with master
 */
public class LocalFileSyncerMasterSlave implements Syncer {

    private static final Logger logger = Logger.getLogger(LocalFileSyncerMasterSlave.class);

    public List<List<FileTree>> fileTreeGroups = new ArrayList<>();

    public boolean verbose = false;

    /**
     * isLastMaster true means the last FileTree is master
     * isLastMaster false means the first FileTree is master
     */
    public boolean isLastMaster = false;

    public LocalFileSyncerMasterSlave(List<List<String>> groups) {
        this(groups, false);
    }

    public LocalFileSyncerMasterSlave(List<List<String>> groups, boolean isLastMaster) {
        this.isLastMaster = isLastMaster;
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
            int first = 1, last = fileTrees.size() - 1;
            FileTree master = fileTrees.get(0);
            if(isLastMaster){
                master = fileTrees.get(last);
                --first;
                --last;
            }

            for(int i = first; i <= last; i++){
                sync(master, fileTrees.get(i));
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

        for (FileNode targetNode : diff.deletedInSource){
            FileHelper.delete(targetNode.getPath());
        }

        logger.info(String.format("%s -> %s %d created, %d updated, %d deleted", source.getRoot(), target.getRoot(),
                diff.newAddedInSource.size(), diff.updatedInSource.size(), diff.deletedInSource.size()));

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

            if(diff.deletedInSource.size() > 0){
                logger.info("\ndeleted:");
                for (FileNode targetNode : diff.deletedInSource){
                    logger.info(targetNode.getPath());
                }
            }
        }
    }

}
