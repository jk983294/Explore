package com.victor.lib.poi.csv;

import org.apache.commons.lang3.StringUtils;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.*;

/**
 * base class for excel to csv conversion
 */
public abstract class Excel2CsvConverterBase {

    private final static String delimiter = "\t";

    protected Map<String, Integer> columnName2columnIndex;

    protected Set<String> intColumnNames;

    protected Set<Integer> intColumnIndex, defaultValueIndex;

    protected Map<String, String> columnName2defaultValue;
    /** default value must be string with proper format */
    protected Map<Integer, String> columnIndex2defaultValue;

    protected List<ArrayList<String>> sheetData;

    protected List<String> rowData;
    /**csv file content*/
    protected StringBuilder content;

    protected int columnSize;

    protected String inputFileName, outputFileName;

    public Excel2CsvConverterBase(String inputFileName, String outputFileName) {
        this.inputFileName = inputFileName;
        this.outputFileName = outputFileName;
        intColumnNames = new HashSet<>();
        columnName2columnIndex = new HashMap<>();
        defaultValueIndex = new HashSet<>();
        intColumnIndex = new HashSet<>();
        columnName2defaultValue = new HashMap<>();
        columnIndex2defaultValue = new HashMap<>();
        content = new StringBuilder();
    }

    /**
     * init int column name to intColumnNames container
     */
    public abstract void initIntColumnNames();

    /**
     * init default value, if this column have default, it will override that value
     * for those non-nullable column to set default value
     */
    public abstract void initDefaultValue();

    public void convert(){
        initIntColumnNames();
        initDefaultValue();

        try {
            FileOutputStream fos = new FileOutputStream(outputFileName);

            extractAllDataFromSourceSheet();

            writeCsvHeader();

            writeBody();

            fos.write(content.toString().getBytes());
            fos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * write other line except first column description header line
     */
    private void writeBody(){
        for (int i = 1; i < sheetData.size(); i++) {
            rowData = sheetData.get(i);
            for (int j = 0; j < columnSize; j++) {
                appendData(convertInvalidValue(rowData.get(j)), j);
            }
        }
    }

    private String convertInvalidValue(String content){
        return (content == null || content.contains("NULL")) ? "" : content;
    }

    private void appendData(String value, int index){
        if(defaultValueIndex.contains(index)){
            content.append(columnIndex2defaultValue.get(index)).append(index == columnSize - 1 ? "\n" : delimiter);
        } else if(intColumnIndex.contains(index) && !StringUtils.isEmpty(value)){
            content.append(Double.valueOf(value).intValue()).append(index == columnSize - 1 ? "\n" : delimiter);
        } else {
            content.append(value).append(index == columnSize - 1 ? "\n" : delimiter);
        }
    }

    /**
     * write first description line, every column name
     */
    private void writeCsvHeader(){
        if(columnSize <= 0) return;
        rowData = sheetData.get(0);
        for (int i = 0; i < columnSize - 1; i++) {
            content.append(rowData.get(i)).append(delimiter);
            columnName2columnIndex.put(rowData.get(i), i);
        }
        content.append(rowData.get(columnSize - 1)).append("\n");
        columnName2columnIndex.put(rowData.get(columnSize - 1), columnSize - 1);

        // prepare other index
        for(String columnName : intColumnNames){
            intColumnIndex.add(columnName2columnIndex.get(columnName));
        }
        for(String columnName : columnName2defaultValue.keySet()){
            defaultValueIndex.add(columnName2columnIndex.get(columnName));
            columnIndex2defaultValue.put(columnName2columnIndex.get(columnName), columnName2defaultValue.get(columnName));
        }
    }


    private List<ArrayList<String>> extractAllDataFromSourceSheet() throws IOException {
        sheetData = new ArrayList<>();
        XSSFWorkbook workbook = new XSSFWorkbook(new FileInputStream(inputFileName));
        XSSFSheet sheet = workbook.getSheetAt(0);
        Row row;
        Cell cell;
        int prevIndex, index;
        Iterator<Row> rowIterator = sheet.iterator();
        while (rowIterator.hasNext()){
            row = rowIterator.next();
            ArrayList<String> rowData = new ArrayList<>();
            Iterator<Cell> cellIterator = row.cellIterator();
            prevIndex = -1;
            while (cellIterator.hasNext()){
                cell = cellIterator.next();
                index = cell.getColumnIndex();
                for(; prevIndex < index - 1; ++prevIndex){
                    rowData.add("");
                }
                switch (cell.getCellType()){
                    case Cell.CELL_TYPE_BOOLEAN: rowData.add(Boolean.valueOf(cell.getBooleanCellValue()).toString()); break;
                    case Cell.CELL_TYPE_NUMERIC: rowData.add(Double.valueOf(String.format("%.6f", cell.getNumericCellValue())).toString()); break;
                    case Cell.CELL_TYPE_STRING: rowData.add(cell.toString()); break;
                    case Cell.CELL_TYPE_BLANK: rowData.add(""); break;
                    default: rowData.add(cell.toString());
                }
                prevIndex = index;
            }
            // update columnSize when first row loaded, it is header row
            if(columnSize <= 0 && rowData.size() > 0){
                columnSize = rowData.size();
            }
            // complete empty value, add blank as ""
            for (; prevIndex < columnSize - 1; ++prevIndex){
                rowData.add("");
            }
            sheetData.add(rowData);
        }
        return sheetData;
    }
}
