package com.victor.lib.poi;

import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.apache.poi.hssf.usermodel.HSSFDateUtil;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;

import java.io.FileInputStream;
import java.io.IOException;

public class ReaderUserModel {

	private final static String filepath = "D:/dumyData/ooxml-cell.xlsx";
	private final static String filepath1 = "D:/dumyData/ooxml-scatter-chart.xlsx";
	
	public void method1() throws IOException  {
		Workbook wb = new XSSFWorkbook(new FileInputStream(filepath));
        for (int i = 0; i < wb.getNumberOfSheets(); i++) {
            Sheet sheet = wb.getSheetAt(i);
            System.out.println(wb.getSheetName(i));
            for (Row row : sheet) {
                System.out.println("rowNum: " + row.getRowNum());
                for (Cell cell : row) {
                    System.out.println(cell.toString());
                }
            }
        }
	}
	
	public void method2() throws IOException  {
		XSSFWorkbook  wb = new XSSFWorkbook(new FileInputStream(filepath1));
		for (int k = 0; k < wb.getNumberOfSheets(); k++) {
			XSSFSheet sheet = wb.getSheetAt(k); 
			int rows = sheet.getPhysicalNumberOfRows(); 
			for (int r = 0; r < rows; r++) {
				// 定义 row
				XSSFRow row = sheet.getRow(r);
				if (row != null) {
					int cells = row.getPhysicalNumberOfCells();
					for (short c = 0; c < cells; c++) {
						XSSFCell cell = row.getCell(c);
						if (cell != null) {
							String value = null;
							switch (cell.getCellType()) {
								case XSSFCell.CELL_TYPE_FORMULA:
									value = "FORMULA ";
									break;
								case XSSFCell.CELL_TYPE_NUMERIC:
									if(HSSFDateUtil.isCellDateFormatted(cell)){
										value = "DATE value="
											+ cell.getDateCellValue();
									}else{
										value = "NUMERIC value="
												+ cell.getNumericCellValue();
									}								
									break;
								case XSSFCell.CELL_TYPE_STRING:
									value = "STRING value="
											+ cell.getStringCellValue();
									break;								
								case XSSFCell.CELL_TYPE_BOOLEAN:
									value = "BOOLEAN value="
											+ cell.getBooleanCellValue();																
									cell.getDateCellValue();								
									break;
								default:
							}							
							System.out.println(value);
						}
					}
				}
			}
		}
	}
	
	public static void main(String[] args) throws Exception {
		ReaderUserModel rum = new ReaderUserModel();
		
		rum.method1();
		rum.method2();
    }
}
