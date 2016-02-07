package com.victor.file

import java.io.File

import com.victor.file.model.{DirectoryObject, FileObject}
import com.victor.file.searcher.{FilterChecker, Matcher}

object TestFilterChecker {

   def main(args: Array[String]) {

     val listOfFiles = List(FileObject(new File("F:\\Data\\mongo\\text.txt")), DirectoryObject(new File("F:\\Data\\MktData")))
     val matchedFiles = FilterChecker("text") findMatchedFiles listOfFiles
     println( matchedFiles )

     val isMatched = FilterChecker("test").findMatchedFileContentCount(new File("F:\\Data\\mongo\\text.txt"))
     println( isMatched )
   }
 }
