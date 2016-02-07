package com.victor.file.manipulator

import java.io.{FileInputStream, InputStream, PrintWriter, File}

import com.victor.file.model.{DirectoryObject, IOObject}
import com.victor.file.searcher.{Matcher, FileConverter}


class Chm2TxtConverter(val sourceRoot: String, val targetRoot : String) {

  def toSource(inputStream:InputStream): scala.io.BufferedSource = {
    import java.nio.charset.Charset
    import java.nio.charset.CodingErrorAction
    val decoder = Charset.forName("GBK").newDecoder()
    decoder.onMalformedInput(CodingErrorAction.IGNORE)
    scala.io.Source.fromInputStream(inputStream)(decoder)
  }

  def getContent(path: String): String = {
    def extractContent(lines: List[String], start:Int, end: Int) = {
      lines.slice(start, end).reduceLeft(_+_).replaceAll("(<BR><BR>|</tr>)", "\r\n").replaceAll("&nbsp;", " ").replaceAll("<[^>]*>", "")
    }
    val source = toSource(new FileInputStream(path))
    val lines = try source.getLines().toList finally source.close()
    val rangesStart = lines.zipWithIndex.filter{ case (line, index) => line.contains("<font size=\"4\">") }.map(_._2)
    val rangesEnd = lines.zipWithIndex.filter{ case (line, index) => line.contains("HTMLBUILERPART") }.map(_._2)

    if(rangesStart.length > 0 && rangesEnd.length > 0){
      extractContent(lines, rangesStart(0), rangesEnd.last + 1) + "\r\n\r\n"
    } else if(rangesEnd.length >= 2){
      extractContent(lines, rangesEnd(0), rangesEnd.last + 1) + "\r\n\r\n"
    } else {
      println(rangesStart, rangesEnd, path)
      "\r\n\r\n"
    }
  }

  def writeFile(path: String, content: String) = {
    val file = new File(path)
    file.getParentFile().mkdirs()
    val writer = new PrintWriter(file)
    writer.write(content)
    writer.close()
  }

  def handleDir(dir: String): Unit ={
    val matcher1 = new Matcher("mydoc.*htm", new File(dir).getCanonicalPath());
    val matchedFiles1 = matcher1.execute()
    val results : List[String] = matchedFiles1.map{case (filePath, count) => filePath}.sorted
    if(results.length > 0){
      writeFile(dir.replace(sourceRoot, targetRoot)+".txt", results.map(path => getContent(path)).reduceLeft(_+_))
    }
  }

  def execute() = {
    def recursiveHandle(files : List[IOObject]):Any =
      files.foreach(iOObject =>
        iOObject match {
          case directory : DirectoryObject =>
            handleDir(iOObject.fullName)
            recursiveHandle(directory.children())
          case _ => None
        }
      )

    val rootIOObject = FileConverter.convertToIOOject(new File(sourceRoot))
    recursiveHandle(List(rootIOObject))

  }
}
