package com.victor.file.manipulator

object TestChm2TxtConverter {

  def main(args: Array[String]) {
    val chmConverter = new Chm2TxtConverter("H:\\book\\hieracery\\", "H:\\book\\result\\")
    chmConverter.execute()
//    chmConverter.handleDir("H:\\book\\hieracery\\H1\\1001_03")
//    println(chmConverter.getContent("H:\\book\\hieracery\\H1\\1001_03\\mydoc003.htm"))
  }
}
