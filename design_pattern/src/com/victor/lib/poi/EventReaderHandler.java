package com.victor.lib.poi;

import java.util.ArrayList;

import org.apache.poi.xssf.model.SharedStringsTable;


public class EventReaderHandler extends ReadBaseHandler {

	private ArrayList<String> values;
	
	public EventReaderHandler(SharedStringsTable sst) {
		super(sst);
		values = new ArrayList<>();
	}

	@Override
	public void cellValueHandle() {
		if ( row >= 1) {
			values.add(content);
			System.out.println(row + " " + column + " " + content);
		}
	}

}
