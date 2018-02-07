/**
 * the pattern an easy way to implement inheritance
 * with a performance boost as well:
 * when defining a function in an object, they're all created by reference
 * instead of creating their own individual copies.
 */
var copyObject = (function () {

    function F() {}

    return function ( proto ) {
        F.prototype = proto;
        return new F();
    };
})();

// or
var createObject = function (o) {
    // we only want the prototype part of the `new`
    // behavior, so make an empty constructor
    function F() {}

    // set the function's `prototype` property to the
    // object that we want the new object's prototype
    // to be.
    F.prototype = o;

    // use the `new` operator. We will get a new
    // object whose prototype is o, and we will
    // invoke the empty function, which does nothing.
    return new F();
};


/**
 * Understanding “Prototypes” in JavaScript
 */
var person = Object.create(null); // this creates an empty objects
Object.defineProperty(person, 'firstName', {
    value: "Yehuda",
    writable: true,
    enumerable: true,
    configurable: true
});

//better way
var config = {
    writable: true,
    enumerable: true,
    configurable: true
};

var defineProperty = function(obj, name, value) {
    config.value = value;
    Object.defineProperty(obj, name, config);
}

var person = Object.create(null);
defineProperty(person, 'firstName', "Yehuda");
defineProperty(person, 'lastName',   "Katz");

// more better
var person = Object.create(null);
defineProperty(person, 'fullName', function() {
    return this.firstName + ' ' + this.lastName;
});

// this time, let's make man's prototype person, so all
// men share the fullName function
var man = Object.create(person);
defineProperty(man, 'sex', "male");

var yehuda = Object.create(man);
defineProperty(yehuda, 'firstName', "Yehuda");
defineProperty(yehuda, 'lastName', "Katz");

yehuda.sex        // "male"
yehuda.fullName() // "Yehuda Katz"