package com.victor.sync.model;

/**
 * file node represent a leaf file node, not a directory
 */
public class FileNode {

    public String relativePath;         // relative relativePath to root
    public String path;                 // absolute path
    public long lastModified;
    public long fileSize;

    public FileNode(String path, String relativePath, long lastModified, long fileSize) {
        this.path = path;
        this.relativePath = relativePath;
        this.lastModified = lastModified;
        this.fileSize = fileSize;
    }

    public String getRelativePath() {
        return relativePath;
    }

    public void setRelativePath(String relativePath) {
        this.relativePath = relativePath;
    }

    public long getLastModified() {
        return lastModified;
    }

    public void setLastModified(long lastModified) {
        this.lastModified = lastModified;
    }

    public long getFileSize() {
        return fileSize;
    }

    public void setFileSize(long fileSize) {
        this.fileSize = fileSize;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof FileNode)) return false;

        FileNode node = (FileNode) o;

        if (relativePath != null ? !relativePath.equals(node.relativePath) : node.relativePath != null) return false;

        return true;
    }

    @Override
    public int hashCode() {
        return relativePath != null ? relativePath.hashCode() : 0;
    }

    @Override
    public String toString() {
        return "FileNode{" +
                "relativePath='" + relativePath + '\'' +
                ", path='" + path + '\'' +
                ", lastModified=" + lastModified +
                ", fileSize=" + fileSize +
                '}';
    }
}