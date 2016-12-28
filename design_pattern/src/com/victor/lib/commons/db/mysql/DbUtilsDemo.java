package com.victor.lib.commons.db.mysql;

import com.victor.lib.commons.db.mysql.model.User;
import org.apache.commons.dbutils.handlers.*;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import junit.framework.TestCase;
import org.apache.commons.dbutils.DbUtils;
import org.apache.commons.dbutils.QueryRunner;


public class DbUtilsDemo extends TestCase {

    public static void main(String[] args) throws SQLException {
        test_insert();
        test_find();
    }

    public static void test_insert() throws SQLException {
        System.out.println("-------------test_insert()-------------");
        //创建连接
        Connection conn = ConnTools.makeConnection();
        //创建SQL执行工具
        QueryRunner qRunner = new QueryRunner();
        //执行SQL插入
        int n = qRunner.update(conn, "insert into user(name, pswd) values('iii','iii')");
        System.out.println("成功插入" + n + "条数据！");
        //关闭数据库连接
        DbUtils.closeQuietly(conn);
    }

    public static void test_find() throws SQLException {
        System.out.println("-------------test_find()-------------");
        //创建连接
        Connection conn = ConnTools.makeConnection();
        //创建SQL执行工具
        QueryRunner qRunner = new QueryRunner();
        //执行SQL查询，并获取结果
        List<User> list = (List<User>) qRunner.query(conn, "select id, name, pswd from user", new BeanListHandler(User.class));
        //输出查询结果
        for (User user : list) {
            System.out.println(user);
        }
        //关闭数据库连接
        DbUtils.closeQuietly(conn);
    }
}