package com.victor.file.searcher

import java.io.File

import com.victor.file.model.{FileObject, DirectoryObject}

object FileConverter {
  def convertToIOOject(file : File) =
    if(file.isDirectory) DirectoryObject(file)
    else FileObject(file)
}
