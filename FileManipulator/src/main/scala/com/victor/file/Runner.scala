package com.victor.file

import com.victor.file.searcher.{SearchResultWriter, Matcher}

object Runner extends App {
  def convert2Bool(boolString : String) = List("true", "t") exists( trueVal => trueVal == boolString.toLowerCase)

  val matcher = args match {
    case Array(filter) => new Matcher(filter)
    case Array(filter, rootPath) => new Matcher(filter, rootPath)
    case Array(filter, rootPath, checkSubFolders) => new Matcher(filter, rootPath, convert2Bool(checkSubFolders))
    case Array(filter, rootPath, checkSubFolders, contentFilter, _*) =>
      new Matcher(filter, rootPath, convert2Bool(checkSubFolders), Some(contentFilter))
  }

  val results = matcher.execute()

  println(s"Found ${results.length} matches:")
  args match {
    case Array(_, _, _, _, outputFilePath, _*) => {
      SearchResultWriter.write2File(outputFilePath, results)
      println(s"Results written to $outputFilePath")
    }
    case _ => SearchResultWriter.write2Console(results)
  }

}
