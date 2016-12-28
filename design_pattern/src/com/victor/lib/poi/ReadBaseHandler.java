package com.victor.lib.poi;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.poi.xssf.model.SharedStringsTable;
import org.apache.poi.xssf.usermodel.XSSFRichTextString;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

/**
 * base handler for POI event model reader, it maintain the row, column, content  for further handling
 */
public abstract class ReadBaseHandler extends DefaultHandler {
	
	public String content;					//content for that cell
	public String columnStr;				//current column
	public String position;					//current position column+row
	public int previousRow;					//previous row
	public int row;							//current row
	public int column;						//current  column
	public boolean isNewRow;
	
	private SharedStringsTable sst;	
	private boolean nextIsString;
	public static final Pattern rowPattern = Pattern.compile("[0-9]+");
	public static final Pattern columnPattern = Pattern.compile("[A-Z]+");
	
	public ReadBaseHandler(SharedStringsTable sst) {
		this.sst = sst;
	}
	
	/**
	 * implement by detail handler to extract data from excel
	 * column and row are 1-based
	 */
	public abstract void cellValueHandle();
	
	@Override
	public void startElement(String uri, String localName, String name,
			Attributes attributes) throws SAXException {
		// c => cell
		if(name.equals("c")) {
			position = attributes.getValue("r");
			// Figure out if the value is an index in the SST
			String cellType = attributes.getValue("t");
			nextIsString = cellType != null && cellType.equals("s");
		}
		// Clear contents cache
		content = "";
	}
	@Override
	public void endElement(String uri, String localName, String name)
			throws SAXException {
		// Process the last contents as required.
		// Do now, as characters() may be called more than once
		if(nextIsString) {
			int idx = Integer.parseInt(content);
			content = new XSSFRichTextString(sst.getEntryAt(idx)).toString();
			nextIsString = false;
		}

		// v => contents of a cell
		// Output after we've seen the string contents
		if(name.equals("v")) {
			parsePosition();
			cellValueHandle();
		}
	}
	
	@Override
	public void characters(char[] ch, int start, int length)
			throws SAXException {
		content += new String(ch, start, length);
	}
	
	/**
	 * record current position
	 */
	public void parsePosition(){
		Matcher matcher = rowPattern.matcher(position);
		if(matcher.find()){
			previousRow = row;
			row = Integer.valueOf(matcher.group(0));
			isNewRow = previousRow != row;
		}
		matcher = columnPattern.matcher(position);
		if(matcher.find()){
			columnStr = matcher.group(0);
			column = getColumnNum();
		}	
	}
	
	/**
	 * convert Excel column "A" -> number 1
	 */
	private int getColumnNum(){
		columnStr = columnStr.trim();
		StringBuilder buffer = new StringBuilder(columnStr);
		char chars[] = buffer.reverse().toString().toLowerCase().toCharArray();
		int ret = 0, multiplier;
		for (int i = 0; i < chars.length; i++) {
			multiplier = (int)chars[i] - 96;
			ret += multiplier * Math.pow(26, i);
		}
		return ret;
	}
	
	
	/**
	 * convert column "A" -> number 1
	 */
	private int getColumnNum(String colName){
		columnStr = colName.trim();
		StringBuilder buffer = new StringBuilder(columnStr);
		char chars[] = buffer.reverse().toString().toLowerCase().toCharArray();
		int ret = 0, multiplier;
		for (int i = 0; i < chars.length; i++) {
			multiplier = (int)chars[i] - 96;
			ret += multiplier * Math.pow(26, i);
		}
		return ret;
	}

}
