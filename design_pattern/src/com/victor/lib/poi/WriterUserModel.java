package com.victor.lib.poi;


import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Date;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class WriterUserModel {
	
	private final static String filepath = "D:/dumyData/";
	
	public static void main(String[]args) throws Exception {
		WriterUserModel wum = new WriterUserModel();
		wum.method1();
//		wum.method2();
		System.out.println("write over...");
	}
	
	public void method1() throws IOException {
		Workbook wb = new XSSFWorkbook();
        Sheet sheet = wb.createSheet("Sheet 1");
        final int NUM_OF_ROWS = 30000;
        final int NUM_OF_COLUMNS = 20;

        // Create a row and put some cells in it. Rows are 0 based.
        Row row;
        Cell cell;
        for (int rowIndex = 0; rowIndex < NUM_OF_ROWS; rowIndex++) {
            row = sheet.createRow((short) rowIndex);
            for (int colIndex = 0; colIndex < NUM_OF_COLUMNS; colIndex++) {
                cell = row.createCell((short) colIndex);
                cell.setCellValue(colIndex * (rowIndex + 1));
            }
        }
        // Write the output to a file
        FileOutputStream fileOut = new FileOutputStream(filepath + "ooxml-scatter-chart.xlsx");
        wb.write(fileOut);
        fileOut.close();
		
	}
	
	public void method2() throws IOException {
		Workbook wb = new XSSFWorkbook(); //or new HSSFWorkbook();
        CreationHelper creationHelper = wb.getCreationHelper();
        Sheet sheet = wb.createSheet("new sheet");

        // Create a row and put some cells in it. Rows are 0 based.
        Row row = sheet.createRow((short)0);
        // Create a cell and put a value in it.
        Cell cell = row.createCell((short)0);
        cell.setCellValue(1);

        //numeric value
        row.createCell(1).setCellValue(1.2);

        //plain string value
        row.createCell(2).setCellValue("This is a string cell");

        //rich text string
        RichTextString str = creationHelper.createRichTextString("Apache");
        Font font = wb.createFont();
        font.setItalic(true);
        font.setUnderline(Font.U_SINGLE);
        str.applyFont(font);
        row.createCell(3).setCellValue(str);

        //boolean value
        row.createCell(4).setCellValue(true);

        //formula
        row.createCell(5).setCellFormula("SUM(A1:B1)");

        //date
        CellStyle style = wb.createCellStyle();
        style.setDataFormat(creationHelper.createDataFormat().getFormat("m/d/yy h:mm"));
        cell = row.createCell(6);
        cell.setCellValue(new Date());
        cell.setCellStyle(style);

        //hyperlink
        row.createCell(7).setCellFormula("SUM(A1:B1)");
        cell.setCellFormula("HYPERLINK(\"http://google.com\",\"Google\")");


        // Write the output to a file
        FileOutputStream fileOut = new FileOutputStream(filepath + "ooxml-cell.xlsx");
        wb.write(fileOut);
        fileOut.close();
	}

}
