package com.victor.lib.poi;

import java.io.FileOutputStream;
import java.io.InputStream;
import java.lang.reflect.Constructor;
import java.util.Iterator;

import org.apache.poi.openxml4j.opc.OPCPackage;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.eventusermodel.XSSFReader;
import org.apache.poi.xssf.model.SharedStringsTable;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.xml.sax.ContentHandler;
import org.xml.sax.InputSource;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.XMLReaderFactory;

public class Data2Process {
	/**
	 * read one sheet
	 * @throws Exception
	 */
	public static void processOneSheet(String filename, String sheetName, String handlerName, Class<?> ctorParams[], Object arglist[]) throws Exception {
		OPCPackage pkg = OPCPackage.open(filename);
		XSSFReader r = new XSSFReader( pkg );
		SharedStringsTable sst = r.getSharedStringsTable();

		Class<?> classtype = Class.forName (handlerName);
		Object handler;
		if (ctorParams == null) {
			Constructor<?> constructor = classtype.getConstructor(SharedStringsTable.class);
			handler = constructor.newInstance(sst);
		}else {
			ctorParams[0] = SharedStringsTable.class;
			arglist[0] = sst;
			Constructor<?> constructor = classtype.getConstructor(ctorParams);
			handler = constructor.newInstance(arglist);
		}
		
		XMLReader parser = XMLReaderFactory.createXMLReader("com.sun.org.apache.xerces.internal.parsers.SAXParser");
		parser.setContentHandler((ContentHandler)handler);

		// rId2 found by processing the Workbook
		// Seems to either be rId# or rSheet#
		InputStream sheet2 = r.getSheet(sheetName);
		InputSource sheetSource = new InputSource(sheet2);
		parser.parse(sheetSource);
		sheet2.close();
	}

	/**
	 * read all sheets
	 * @throws Exception
	 */
	public static void processAllSheets(String filename, String handlerName, Class<?> ctorParams[], Object arglist[]) throws Exception {
		OPCPackage pkg = OPCPackage.open(filename);
		XSSFReader r = new XSSFReader( pkg );
		SharedStringsTable sst = r.getSharedStringsTable();
		
		Class<?> classtype = Class.forName (handlerName);
		Object handler;
		if (ctorParams == null) {
			Constructor<?> constructor = classtype.getConstructor(SharedStringsTable.class);
			handler = constructor.newInstance(sst);
		}else {
			ctorParams[0] = SharedStringsTable.class;
			arglist[0] = sst;
			Constructor<?> constructor = classtype.getConstructor(ctorParams);
			handler = constructor.newInstance(arglist);
		}
		
		XMLReader parser = XMLReaderFactory.createXMLReader("com.sun.org.apache.xerces.internal.parsers.SAXParser");
		parser.setContentHandler((ContentHandler)handler);

		Iterator<InputStream> sheets = r.getSheetsData();
		while(sheets.hasNext()) {
			InputStream sheet = sheets.next();
			InputSource sheetSource = new InputSource(sheet);
			parser.parse(sheetSource);
			sheet.close();
		}
		//you can return this handler to get stored useful data
	}
	
	
	public static void copyAllSheets(String sourceFileName, String copyFileName) throws Exception {
		OPCPackage pkg = OPCPackage.open(sourceFileName);
		XSSFReader r = new XSSFReader( pkg );
		SharedStringsTable sst = r.getSharedStringsTable();
		
		Workbook copy = new XSSFWorkbook();		
        
        
		CopySheetHandler handler = new CopySheetHandler(sst);
		
		XMLReader parser = XMLReaderFactory.createXMLReader("com.sun.org.apache.xerces.internal.parsers.SAXParser");
		parser.setContentHandler(handler);

		Iterator<InputStream> sheets = r.getSheetsData();
		int i = 1;
		while(sheets.hasNext()) {
			InputStream sheet = sheets.next();
			InputSource sheetSource = new InputSource(sheet);
			handler.setCopySheet(copy.createSheet("Sheet" + i));
			parser.parse(sheetSource);
			sheet.close();
			++i;
		}
		// Write the output to a file
        FileOutputStream fileOut = new FileOutputStream(copyFileName);
        copy.write(fileOut);
        fileOut.close();
	}
	
	public static void main(String[] args) throws Exception {
		String filepath = "D:/dumyData/ooxml-cell.xlsx";
		processOneSheet(filepath,"rId1","com.victor.finFriday.excelpoi.EventReaderHandler",null,null);
		System.out.println("\n\n");
		processAllSheets(filepath, "com.victor.finFriday.excelpoi.EventReaderHandler", null, null);
		
		System.out.println("\n\n");
		copyAllSheets("D:/dumyData/ooxml-scatter-chart.xlsx", "D:/dumyData/copy.xlsx");
		System.out.println("copy over ...");
	}
}
