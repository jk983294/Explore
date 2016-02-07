package com.victor.file.searcher

import java.io.File

import com.victor.file.model.{IOObject, FileObject}

import scala.util.control.NonFatal


class FilterChecker(filter: String) {
  val filterAsRegex = filter.r
  def matches(content: String) =
    filterAsRegex findFirstMatchIn content match {
      case Some(_) => true
      case None => false
    }

  // only match file name
  def findMatchedFiles(iOObjects: List[IOObject]) =
    for (iOObject <- iOObjects
          if(iOObject.isInstanceOf[FileObject])
          if(matches(iOObject.name)))
      yield iOObject

  // match file content
  def findMatchedFileContentCount(file : File) = {
    def getFilterMatchCount(content : String) =
      (filterAsRegex findAllIn content).length

    import scala.io.Source
    try {
      val fileSource = Source.fromFile(file)
      try {
        fileSource.getLines().foldLeft(0)(
          (accumulator, line) => accumulator + getFilterMatchCount(line)
        )
      } catch {
        case NonFatal(_) => 0
      } finally {
        fileSource.close()
      }
    } catch {
      case NonFatal(_) => 0
    }
  }

}

object FilterChecker {
  def apply(filter: String) = new FilterChecker(filter)
}
