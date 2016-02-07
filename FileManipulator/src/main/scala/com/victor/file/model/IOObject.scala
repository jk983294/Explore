package com.victor.file.model

import java.io.File

import com.victor.file.searcher.FileConverter

import scala.util.control.NonFatal

trait IOObject {
  val file : File
  val name = file.getName()
  val fullName = try file.getAbsolutePath() catch {case NonFatal(_) => name}
}

case class DirectoryObject(file: File) extends IOObject{
  def children() =
    try
      file.listFiles().toList map(file => FileConverter convertToIOOject(file))
    catch{
      case _ : NullPointerException => List()
    }
}

case class FileObject(file: File) extends IOObject
