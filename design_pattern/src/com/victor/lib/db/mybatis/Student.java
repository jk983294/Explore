package com.victor.lib.db.mybatis;

/**
 DROP TABLE IF EXISTS test.student;
 CREATE TABLE  test.student(
     ID int(10) NOT NULL AUTO_INCREMENT,
     NAME varchar(100) NOT NULL,
     BRANCH varchar(255) NOT NULL,
     PERCENTAGE int(3) NOT NULL,
     PHONE int(10) NOT NULL,
     EMAIL varchar(255) NOT NULL,
     PRIMARY KEY ( ID )
 );
 */
public class Student {
    private int id;
    private String name;
    private String branch;
    private int percentage;
    private int phone;
    private String email;

    public Student(int id, String name, String branch, int percentage, int phone, String email) {
        super();
        this.id = id;
        this.name = name;
        this.branch = branch;
        this.percentage = percentage;
        this.phone = phone;
        this.email = email;
    }

    public Student(String name, String branch, int percentage, int phone, String email) {
        super();
        this.name = name;
        this.branch = branch;
        this.percentage = percentage;
        this.phone = phone;
        this.email = email;
    }

    public Student() {}

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getPhone() {
        return phone;
    }

    public String getEmail() {
        return email;
    }

    public String getBranch() {
        return branch;
    }

    public int getPercentage() {
        return percentage;
    }

    @Override
    public String toString() {
        return "Student{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", branch='" + branch + '\'' +
                ", percentage=" + percentage +
                ", phone=" + phone +
                ", email='" + email + '\'' +
                '}';
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setBranch(String branch) {
        this.branch = branch;
    }

    public void setPercentage(int percentage) {
        this.percentage = percentage;
    }

    public void setPhone(int phone) {
        this.phone = phone;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
