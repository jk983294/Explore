package com.victor.lib.commons.io;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.Writer;
import java.net.URL;
import java.util.Arrays;
import java.util.List;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.io.LineIterator;

public class IOdemo {

	public static void IOUtilsDemo() throws Exception {
		System.out.println("---------------IOUtilsDemo------------------");
		InputStream in = new URL("http://commons.apache.org").openStream();
		System.out.println(IOUtils.toString(in));
		List<String> contents = IOUtils.readLines(in);
		System.out.println(contents);
		IOUtils.closeQuietly(in);
	}

	public static void FileUtilsDemo() throws IOException {
		System.out.println("---------------FileUtilsDemo------------------");
		File file = new File("/commons/io/project.properties");
		List<String> contents = FileUtils.readLines(file, "UTF-8");
		System.out.println(contents);
	}

	/**
	 * The class aims to be consistent between Unix and Windows, to aid
	 * transitions between these environments (such as moving from development
	 * to production).
	 */
	public static void FilenameUtilsDemo() {
		System.out.println("---------------FileUtilsDemo------------------");
		String filename = "C:/commons/io/../lang/project.xml";
		String normalized = FilenameUtils.normalize(filename);
		// result is "C:/commons/lang/project.xml"
		System.out.println(normalized);
	}

	/**
	 * LineIterator better for big file that not suitable to load entirely
	 * 
	 * @throws IOException
	 */
	public static void LineiteratorDemo() throws IOException {
		System.out.println("---------------LineiteratorDemo------------------");
		LineIterator it = FileUtils.lineIterator(new File("C:/test.xml"),
				"UTF-8");
		try {
			while (it.hasNext()) {
				String line = it.nextLine();
				// / do something with line
			}
		} finally {
			LineIterator.closeQuietly(it);
		}
	}

	public static void copyFile() throws Exception {
		System.out.println("---------------copyFile------------------");
		File src = new File("src.txt");
		File dest = new File("dest.txt");
		FileUtils.copyFile(src, dest);

		/**
		 * download to local file system
		 */
		InputStream in = new URL("http://www.baidu.com/img/baidu_logo.gif").openStream();
		byte[] gif = IOUtils.toByteArray(in);
		// IOUtils.write(gif,new FileOutputStream(new File("c:/test.gif")));
		FileUtils.writeByteArrayToFile(new File("c:/test.gif"), gif);
		IOUtils.closeQuietly(in);
		
		/**
		 * input file stream copy to output file stream
		 */
		Writer write = new FileWriter("c:\\kk.dat");  	  
        InputStream ins = new FileInputStream(new File("c:\\text.txt"));  
        IOUtils.copy(ins, write);  
        write.close();  
        ins.close();  
	}
	
	
	public static void wirteDemo() throws Exception {
		System.out.println("---------------wirteDemo------------------");
		String name = "my name is panxiuyan";     
        File file =  new File("c:\\name.txt");         
        FileUtils.writeStringToFile(file, name);  
        String[] content = new String[] { "foo", "bar"}; 
        List<String> contentList = Arrays.asList(content);
        FileUtils.writeLines(file, contentList);
	}
	
	public static void directoryHandle() throws Exception {
		File dir = new File("c:\\test");  		  
        FileUtils.cleanDirectory(dir); 	//delete everything under directory 
        FileUtils.deleteDirectory(dir); // delete everything include directory itself 
        long size = FileUtils.sizeOfDirectory(dir);  
        FileUtils.touch( dir ); 
	}

	public static void main(String[] args) throws Exception {
		IOUtilsDemo();
		FileUtilsDemo();
		FilenameUtilsDemo();
		copyFile();
		wirteDemo();
		directoryHandle();
	}
}
