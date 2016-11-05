package com.victor.sync.model;

import com.victor.sync.util.FileHelper;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class FileTreeDiff {

    public FileTree source, target;

    public List<FileNode> newAddedInSource = new ArrayList<>();
    public List<FileNode> updatedInSource = new ArrayList<>();
    public List<FileNode> deletedInSource = new ArrayList<>();

    public FileTreeDiff(FileTree source, FileTree target) {
        this.source = source;
        this.target = target;
    }

    public FileTreeDiff(String sourceDir, String targetDir) throws IOException {
        this.source = new FileTree(sourceDir);
        this.target = new FileTree(targetDir);
        source.collect();
        target.collect();
    }

    public void difference(){
        if(source.isRootValid() && target.isRootValid()){
            Map<String, FileNode> sourceNodes = source.getRelativePath2files();
            Map<String, FileNode> targetNodes = target.getRelativePath2files();

            for(String sourceRelativePath : sourceNodes.keySet()){
                if(!targetNodes.containsKey(sourceRelativePath)){
                    newAddedInSource.add(sourceNodes.get(sourceRelativePath));
                } else {
                    if(FileHelper.isUpdateNeeded(sourceRelativePath)){
                        FileNode sourceNode = sourceNodes.get(sourceRelativePath);
                        FileNode targetNode = targetNodes.get(sourceRelativePath);
                        if(sourceNode.lastModified > targetNode.lastModified){
                            updatedInSource.add(sourceNode);
                        }
                    }
                }
            }

            for(String targetRelativePath : targetNodes.keySet()){
                if(!sourceNodes.containsKey(targetRelativePath)){
                    deletedInSource.add(targetNodes.get(targetRelativePath));
                }
            }
        }
    }

    @Override
    public String toString() {
        return "FileTreeDiff{" +
                "newAddedInSource=" + newAddedInSource +
                ", updatedInSource=" + updatedInSource +
                ", deletedInSource=" + deletedInSource +
                '}';
    }
}
