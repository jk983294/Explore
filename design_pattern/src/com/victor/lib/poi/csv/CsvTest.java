package com.victor.lib.poi.csv;

/**
 * csv convert test
 */
public class CsvTest extends Excel2CsvConverterBase {

    private String field1;

    public CsvTest(String inputFileName, String outputFileName, String field1) {
        super(inputFileName, outputFileName);
        this.field1 = field1;
    }

    @Override
    public void initIntColumnNames() {
        intColumnNames.add("field2");
    }

    @Override
    public void initDefaultValue() {
        columnName2defaultValue.put("field1", field1);
    }

    public static void convert(String input, String output, String field1){
        new CsvTest(input, output, field1).convert();
    }

    public static void main(String[] args) {
        String field1 = "test";
        String input = "D:\\dumyData\\csv_convert_" + field1 + ".xlsx";
        String output = "D:\\dumyData\\csv_convert_" + field1 + ".csv";
        convert(input, output, field1);
    }
}
