package com.victor.design.aop;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class AOPHandle implements InvocationHandler {

    private AOPMethod method;
    private Object o;
    public AOPHandle(Object o, AOPMethod method) {
        this.o=o;
        this.method=method;
    }
    /**
     * 这个方法会自动调用,Java动态代理机制
     * @param proxy	代理对象的接口,不同于对象
     * @param method	被调用方法
     * @param args	方法参数
     * 不能使用invoke时使用proxy作为反射参数时,因为代理对象的接口,不同于对象这种代理机制是面向接口，而不是面向类的
     **/
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        Object ret=null;
        //修改的地方在这里哦
        this.method.before(proxy, method, args);
        ret=method.invoke(o, args);
        //修改的地方在这里哦
        this.method.after(proxy, method, args);
        return ret;
    }
}
