package com.victor.file.searcher

import java.io.File

import com.victor.file.model.{IOObject, DirectoryObject, FileObject}

import scala.annotation.tailrec

/**
 * This is the main entry point for checking the file system via the supplied specs
 * @param filter The filter that will be used to match against the filenames
 * @param rootLocation The starting location to search
 * @param checkSubFolder A boolean denoting whether or not to search all sub-folders
 * @param contentFilter A filter that will be used to match against the file contents
 */
class Matcher(filter: String, val rootLocation : String = new File(".").getCanonicalPath(),
               checkSubFolder : Boolean = false, contentFilter : Option[String] = None) {
  val rootIOObject = FileConverter.convertToIOOject(new File(rootLocation))

  /**
   * this searches for the files that match the supplied specs
   * @return a list of filename, content match count pairs
   */
  def execute() = {
    @tailrec
    def recursiveMatch(files : List[IOObject], currentList: List[FileObject]): List[FileObject] =
      files match {
        case List() => currentList
        case iOObject :: rest =>
          iOObject match {
            case file : FileObject if FilterChecker(filter) matches file.name =>
              recursiveMatch(rest, file :: currentList)
            case directory : DirectoryObject =>
              recursiveMatch(rest ::: directory.children(), currentList)
            case _ => recursiveMatch(rest, currentList)
          }
      }

    val  matchedFiles = rootIOObject match {
      case file : FileObject if FilterChecker(filter) matches file.name => List(file)
      case directory : DirectoryObject =>
        if(checkSubFolder) recursiveMatch(directory.children(), List())
        else FilterChecker(filter) findMatchedFiles directory.children()
      case  _ => List()
    }

    val contentFilteredFiles = contentFilter match {
      case Some(dataFilter) =>
        matchedFiles.map(iOObject =>
          (iOObject, Some(FilterChecker(dataFilter).findMatchedFileContentCount(iOObject.file))))
        .filter(matchTuple=> matchTuple._2.get > 0)
      case None => matchedFiles map (iOObject => (iOObject, None))
    }

    contentFilteredFiles.map{case (iOObject, count) => (iOObject.fullName, count)}
  }
}
