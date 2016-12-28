package com.victor.lib.db.mybatis;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.IOException;
import java.io.Reader;

public class MybatisDemo {

    public static void main(String args[]) throws IOException{
        MybatisDemo demo = new MybatisDemo();
        //demo.xmlBased();
        demo.annotationBased();
    }

    public void xmlBased() throws IOException {
        Reader reader = Resources.getResourceAsReader("SqlMapConfig.xml");
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(reader);
        SqlSession session = sqlSessionFactory.openSession();

//        {
//            //select a particular student using id
//            Student student = session.selectOne("Student.getById", 1);
//            System.out.println("Current details of the student are" );
//            System.out.println(student.toString());
//
//            //Set new values to the mail and phone number of the student
//            student.setEmail("mohamad123@yahoo.com");
//            student.setPhone(90000000);
//
//            //Update the student record
//            session.update("Student.update",student);
//            System.out.println("Record updated successfully");
//            session.commit();
//
//            //verifying the record
//            Student std = (Student) session.selectOne("Student.getById", 1);
//            System.out.println("Details of the student after update operation" );
//            System.out.println(std.toString());
//            session.commit();
//            session.close();
//        }

//        {
//            //select contact all contacts
//            List<Student> student = session.selectList("Student.getAll");
//            for(Student st : student ){
//                System.out.println(st.getId());
//                System.out.println(st.getName());
//                System.out.println(st.getBranch());
//                System.out.println(st.getPercentage());
//                System.out.println(st.getEmail());
//                System.out.println(st.getPhone());
//            }
//            System.out.println("Records Read Successfully ");
//            session.commit();
//            session.close();
//        }

//        {
//            //Create a new student object
//            Student student = new Student("Mohammad", "It", 80, 984803322, "Mohammad@gmail.com");
//
//            //Insert student data
//            session.insert("Student.insert", student);
//            System.out.println("record inserted successfully");
//            session.commit();
//            session.close();
//        }

        {
            //Delete operation
            session.delete("Student.deleteById", 1);
            session.commit();
            session.close();
            System.out.println("Record deleted successfully");
        }
    }

    public void annotationBased() throws IOException {
        Reader reader = Resources.getResourceAsReader("SqlMapConfig.xml");
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(reader);
        SqlSession session = sqlSessionFactory.openSession();
        session.getConfiguration().addMapper(StudentMapper.class);

        StudentMapper mapper = session.getMapper(StudentMapper.class);

        {
            //Create a new student object
            Student student = new Student();

            //Set the values
            student.setName("zara");
            student.setBranch("EEE");
            student.setEmail("zara@gmail.com");
            student.setPercentage(90);
            student.setPhone(123412341);

            //Insert student data
            mapper.insert(student);
            System.out.println("record inserted successfully");
            session.commit();
            session.close();
        }

        {
            //select a particular student using id
            Student student = mapper.getById(2);
            System.out.println("Current details of the student are "+student.toString());

            //Set new values to the mail and phone number of the student
            student.setEmail("Shyam123@yahoo.com");
            student.setPhone(984802233);

            //Update the student record
            mapper.update(student);
            System.out.println("Record updated successfully");
            session.commit();
            session.close();
        }

        {
            //Get the student details
            Student student = mapper.getById(2);
            System.out.println(student.getBranch());
            System.out.println(student.getEmail());
            System.out.println(student.getId());
            System.out.println(student.getName());
            System.out.println(student.getPercentage());
            System.out.println(student.getPhone());
            session.commit();
            session.close();
        }

        {
            mapper.delete(2);
            System.out.println("record deleted successfully");
            session.commit();
            session.close();
        }

    }



}
