package com.victor.file

import java.io.File

import com.victor.file.model.{DirectoryObject, FileObject}
import com.victor.file.searcher.{SearchResultWriter, FilterChecker, Matcher}

object TestMatcher {

   def main(args: Array[String]) {
     val matcher = new Matcher("txt", new File("F:\\Data\\dummy").getCanonicalPath(), true, Some("text"));
     val matchedFiles = matcher.execute()
     println( matchedFiles )
     SearchResultWriter.write2File("F:\\Data\\dummy\\out.txt", matchedFiles)

   }
 }
