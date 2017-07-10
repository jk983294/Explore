#ifndef LUASCRIPT_H
#define LUASCRIPT_H

#include <iostream>
#include <string>
#include <vector>

// Lua is written in C, so compiler needs to know how to link its libraries
extern "C" {
#include "lauxlib.h"
#include "lua.h"
#include "lualib.h"
}

using namespace std;

class LuaScript {
public:
    LuaScript(const std::string& filename) {
        L = luaL_newstate();
        if (luaL_loadfile(L, filename.c_str()) || lua_pcall(L, 0, 0, 0)) {
            std::cout << "Error: script not loaded (" << filename << ")" << std::endl;
            L = 0;
        }
    }

    ~LuaScript() {
        if (L) lua_close(L);
    }

    void printError(const std::string& variableName, const std::string& reason) {
        std::cout << "Error: can't get [" << variableName << "]. " << reason << std::endl;
    }

    std::vector<int> getIntVector(const std::string& name);
    std::vector<std::string> getTableKeys(const std::string& name);

    inline void clean() {
        int n = lua_gettop(L);
        lua_pop(L, n);
    }

    template <typename T>
    T get(const std::string& variableName) {
        if (!L) {
            printError(variableName, "Script is not loaded");
            return lua_getdefault<T>();
        }

        T result;
        if (lua_gettostack(variableName)) {  // variable succesfully on top of stack
            result = lua_get<T>(variableName);
        } else {
            result = lua_getdefault<T>();
        }

        lua_pop(L, level + 1);  // pop all existing elements from stack
        return result;
    }
    bool lua_gettostack(const std::string& variableName) {
        level = 0;
        std::string var = "";
        for (unsigned int i = 0; i < variableName.size(); i++) {
            if (variableName.at(i) == '.') {
                if (level == 0) {
                    lua_getglobal(L, var.c_str());
                } else {
                    lua_getfield(L, -1, var.c_str());
                }

                if (lua_isnil(L, -1)) {
                    printError(variableName, var + " is not defined");
                    return false;
                } else {
                    var = "";
                    level++;
                }
            } else {
                var += variableName.at(i);
            }
        }
        if (level == 0) {
            lua_getglobal(L, var.c_str());
        } else {
            lua_getfield(L, -1, var.c_str());
        }
        if (lua_isnil(L, -1)) {
            printError(variableName, var + " is not defined");
            return false;
        }
        return true;
    }

    // Generic get
    template <typename T>
    T lua_get(const std::string& variableName) {
        return 0;
    }

    // Generic default get
    template <typename T>
    T lua_getdefault() {
        return 0;
    }

private:
    lua_State* L;
    std::string filename;
    int level;
};

template <>
inline bool LuaScript::lua_get(const std::string& variableName) {
    return (bool)lua_toboolean(L, -1);
}

template <>
inline float LuaScript::lua_get(const std::string& variableName) {
    if (!lua_isnumber(L, -1)) {
        printError(variableName, "Not a number");
    }
    return (float)lua_tonumber(L, -1);
}

template <>
inline int LuaScript::lua_get(const std::string& variableName) {
    if (!lua_isnumber(L, -1)) {
        printError(variableName, "Not a number");
    }
    return (int)lua_tonumber(L, -1);
}

template <>
inline std::string LuaScript::lua_get(const std::string& variableName) {
    std::string s = "null";
    if (lua_isstring(L, -1)) {
        s = std::string(lua_tostring(L, -1));
    } else {
        printError(variableName, "Not a string");
    }
    return s;
}

std::vector<int> LuaScript::getIntVector(const std::string& name) {
    std::vector<int> v;
    lua_gettostack(name.c_str());
    if (lua_isnil(L, -1)) {  // array is not found
        return std::vector<int>();
    }
    lua_pushnil(L);
    while (lua_next(L, -2)) {
        v.push_back((int)lua_tonumber(L, -1));
        lua_pop(L, 1);
    }
    clean();
    return v;
}

std::vector<std::string> LuaScript::getTableKeys(const std::string& name) {
    std::string code =
        "function getKeys(name) "
        "s = \"\""
        "for k, v in pairs(_G[name]) do "
        "    s = s..k..\",\" "
        "    end "
        "return s "
        "end";

    // function for getting table keys
    luaL_loadstring(L, code.c_str());  // execute code
    lua_pcall(L, 0, 0, 0);
    lua_getglobal(L, "getKeys");  // get function
    lua_pushstring(L, name.c_str());
    lua_pcall(L, 1, 1, 0);  // execute function
    std::string test = lua_tostring(L, -1);
    std::vector<std::string> strings;
    std::string temp = "";
    std::cout << "TEMP:" << test << std::endl;
    for (unsigned int i = 0; i < test.size(); i++) {
        if (test.at(i) != ',') {
            temp += test.at(i);
        } else {
            strings.push_back(temp);
            temp = "";
        }
    }
    clean();
    return strings;
}

#endif
