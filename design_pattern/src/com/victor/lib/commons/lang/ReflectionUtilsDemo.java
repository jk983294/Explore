package com.victor.lib.commons.lang;


import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.List;

import org.apache.commons.beanutils.ConvertUtils;
import org.apache.commons.beanutils.PropertyUtils;
import org.apache.commons.beanutils.converters.DateConverter;
import org.apache.commons.lang3.StringUtils;

public class ReflectionUtilsDemo {

    /**
     * convert To Unchecked Exception
     */
    public static IllegalArgumentException convertToUncheckedException(Exception ex){
        if(ex instanceof IllegalAccessException || ex instanceof IllegalArgumentException
                || ex instanceof NoSuchMethodException){
            throw new IllegalArgumentException("exception", ex);
        }else{
            throw new IllegalArgumentException(ex);
        }
    }

    /**
     * convert value to toType object
     * @param value:  string
     * @param toType: class
     * @return
     */
    public static Object convertValue(Object value, Class<?> toType){
        try {
            DateConverter dc = new DateConverter();

            dc.setUseLocaleFormat(true);
            dc.setPatterns(new String[]{"yyyy-MM-dd", "yyyy-MM-dd HH:mm:ss"});

            ConvertUtils.register(dc, Date.class);

            return ConvertUtils.convert(value, toType);
        } catch (Exception e) {
            e.printStackTrace();
            throw convertToUncheckedException(e);
        }
    }

    /**
     * collect list element's property into array list
     */
    @SuppressWarnings("unchecked")
    public static List collectPropertyToList(Collection collection, String propertyName){
        List list = new ArrayList();

        try {
            for(Object obj: collection){
                list.add(PropertyUtils.getProperty(obj, propertyName));
            }
        } catch (Exception e) {
            e.printStackTrace();
            convertToUncheckedException(e);
        }

        return list;
    }

    /**
     * collect list element's property into string, join by separator
     */
    @SuppressWarnings("unchecked")
    public static String collectPropertyToString(Collection collection, String propertyName,
                                                 String separator){
        List list = collectPropertyToList(collection, propertyName);
        return StringUtils.join(list, separator);
    }

    /**
     * getSuperClassGenericType
     * like: public EmployeeDao extends BaseDao<Employee, String>
     */
    @SuppressWarnings("unchecked")
    public static Class getSuperClassGenericType(Class clazz, int index){
        Type genType = clazz.getGenericSuperclass();

        if(!(genType instanceof ParameterizedType)){
            return Object.class;
        }

        Type [] params = ((ParameterizedType)genType).getActualTypeArguments();

        if(index >= params.length || index < 0){
            return Object.class;
        }

        if(!(params[index] instanceof Class)){
            return Object.class;
        }

        return (Class) params[index];
    }

    /**
     * getSuperClassGenericType
     * like: public EmployeeDao extends BaseDao<Employee, String>
     */
    @SuppressWarnings("unchecked")
    public static<T> Class<T> getSuperGenericType(Class clazz){
        return getSuperClassGenericType(clazz, 0);
    }

    /**
     * recursively get object DeclaredMethod
     */
    public static Method getDeclaredMethod(Object object, String methodName, Class<?>[] parameterTypes){

        for(Class<?> superClass = object.getClass(); superClass != Object.class; superClass = superClass.getSuperclass()){
            try {
                return superClass.getDeclaredMethod(methodName, parameterTypes);
            } catch (NoSuchMethodException e) {
                //Method is not defined in current class layer, then go up
            }
        }

        return null;
    }

    /**
     * make filed Accessible
     */
    public static void makeAccessible(Field field){
        if(!Modifier.isPublic(field.getModifiers())){
            field.setAccessible(true);
        }
    }

    /**
     * recursively get object DeclaredField
     */
    public static Field getDeclaredField(Object object, String filedName){

        for(Class<?> superClass = object.getClass(); superClass != Object.class; superClass = superClass.getSuperclass()){
            try {
                return superClass.getDeclaredField(filedName);
            } catch (NoSuchFieldException e) {
                //Field is not defined in current class layer, then go up
            }
        }
        return null;
    }

    /**
     * invokeMethod directly and ignore the modifier (private, protected)
     * @throws InvocationTargetException
     * @throws IllegalArgumentException
     */
    public static Object invokeMethod(Object object, String methodName, Class<?> [] parameterTypes,
                                      Object [] parameters) throws InvocationTargetException{

        Method method = getDeclaredMethod(object, methodName, parameterTypes);

        if(method == null){
            throw new IllegalArgumentException("Could not find method [" + methodName + "] on target [" + object + "]");
        }

        method.setAccessible(true);

        try {
            return method.invoke(object, parameters);
        } catch(IllegalAccessException e) {

        }

        return null;
    }

    /**
     * set field value directly and ignore the modifier (private, protected), and also it doesn't call setter
     */
    public static void setFieldValue(Object object, String fieldName, Object value){
        Field field = getDeclaredField(object, fieldName);

        if (field == null)
            throw new IllegalArgumentException("Could not find field [" + fieldName + "] on target [" + object + "]");

        makeAccessible(field);

        try {
            field.set(object, value);
        } catch (IllegalAccessException e) {

        }
    }

    /**
     * get field value directly and ignore the modifier (private, protected), and also it doesn't call getter
     */
    public static Object getFieldValue(Object object, String fieldName){
        Field field = getDeclaredField(object, fieldName);

        if (field == null)
            throw new IllegalArgumentException("Could not find field [" + fieldName + "] on target [" + object + "]");

        makeAccessible(field);

        Object result = null;

        try {
            result = field.get(object);
        } catch (IllegalAccessException e) {

        }

        return result;
    }
}
