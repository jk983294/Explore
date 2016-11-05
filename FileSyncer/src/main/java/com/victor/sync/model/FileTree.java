package com.victor.sync.model;

import org.apache.commons.collections.CollectionUtils;
import org.apache.commons.lang3.StringUtils;

import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

public class FileTree {

    public String root;

    public boolean isRootValid = false;

    public Map<String, FileNode> relativePath2files;

    public Set<String> excludeFiles;        // when collect, exclude those files under this root tree

    public FileTree(String root) {
        if(StringUtils.isEmpty(root)){
            throw new IllegalArgumentException("unacceptable root");
        }

        if(!root.endsWith("/")){
            root = root + "/";
        }
        this.root = root;
    }

    public void collect() throws IOException {
        relativePath2files = new TreeMap<>();
        File rootFile = new File(root);
        isRootValid = rootFile.exists() && rootFile.isDirectory();
        if(isRootValid){
            collect(rootFile);
        }
    }

    private void collect(File file) throws IOException {
        if ( file.isDirectory() ) {
            for(File f : file.listFiles()){
                if(CollectionUtils.isEmpty(excludeFiles) || !excludeFiles.contains(f.getCanonicalPath())){
                    collect(f);
                }
            }
        } else if(!file.isHidden() && file.canRead() && file.canWrite() && file.isFile()){
            if(CollectionUtils.isEmpty(excludeFiles) || !excludeFiles.contains(file.getCanonicalPath())){
                String fullPath = file.getCanonicalPath();
                String relative = fullPath.substring(root.length());
                FileNode node = new FileNode(fullPath, relative, file.lastModified(), file.length());
                relativePath2files.put(relative, node);
            }
        }
    }

    public String getRoot() {
        return root;
    }

    public void setRoot(String root) {
        this.root = root;
    }

    public boolean isRootValid() {
        return isRootValid;
    }

    public void setRootValid(boolean isRootValid) {
        this.isRootValid = isRootValid;
    }

    public Map<String, FileNode> getRelativePath2files() {
        return relativePath2files;
    }

    public void setRelativePath2files(Map<String, FileNode> relativePath2files) {
        this.relativePath2files = relativePath2files;
    }

    public Set<String> getExcludeFiles() {
        return excludeFiles;
    }

    public void setExcludeFiles(Set<String> excludeFiles) {
        this.excludeFiles = excludeFiles;
    }
}
