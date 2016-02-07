package com.victor.file.searcher

import java.io._

object SearchResultWriter {

  def write2File(filePath : String, results : List[(String, Option[Int])]) = {
    val fileWriter = new FileWriter(filePath)
    val printWriter = new PrintWriter(fileWriter)
    try
      for((fileName, countOption) <- results)
        printWriter.println(getString(fileName, countOption))
    finally {
      printWriter.close()
      fileWriter.close()
    }
  }

  def write2Console(results : List[(String, Option[Int])]) =
    for((fileName, countOption) <- results)
      println(getString(fileName, countOption))

  private def getString(fileName : String, countOption: Option[Int]) =
    countOption match {
      case Some(count) => s"\t$fileName -> $count"
      case None => s"\t$fileName"
    }
}
