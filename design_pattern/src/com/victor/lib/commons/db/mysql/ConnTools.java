package com.victor.lib.commons.db.mysql;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * connection tools
 */
public class ConnTools {

    private static String driverClassName = "com.mysql.jdbc.Driver";
    private static String url = "jdbc:mysql://192.168.104.101:3306/testdb?useUnicode=true&characterEncoding=utf8";
    private static String user = "root";
    private static String password = "123456";

    public static Connection makeConnection() {
        Connection conn = null;
        try {
            Class.forName(driverClassName);
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        try {
            conn = DriverManager.getConnection(url, user, password);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return conn;
    }
}
