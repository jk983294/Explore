package com.victor.lib.poi;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.model.SharedStringsTable;

public class CopySheetHandler extends ReadBaseHandler {

    private Sheet copySheet;
    private Row sheetRow;
    private Cell sheetCell;

    public CopySheetHandler(SharedStringsTable sst) {
        super(sst);
    }

    @Override
    public void cellValueHandle() {
        if (isNewRow) {
            sheetRow = copySheet.createRow((short) row -1);
        }
        sheetCell = sheetRow.createCell((short) column-1);
        sheetCell.setCellValue(content);
    }

    public Sheet getCopySheet() {
        return copySheet;
    }

    public void setCopySheet(Sheet copySheet) {
        this.copySheet = copySheet;
    }
}
