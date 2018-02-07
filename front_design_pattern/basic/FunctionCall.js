/**
 * The Core Primitive
 */
function hello(thing) {
    // The first parameter is this
    console.log(this + " says hello " + thing);
}
hello.call("Yehuda", "world") //=> Yehuda says hello world


/**
 * Simple Function Invocation
 */
function hello(thing) {
    console.log("Hello " + thing);
}

hello("world")
// desugars to:
hello.call(window, "world");


/**
 * Member Functions
 */
var person = {
    name: "Brendan Eich",
    hello: function(thing) {
        console.log(this + " says hello " + thing);
    }
}

person.hello("world")
// desugars to this:
person.hello.call(person, "world");


// hello could attach to object dynamic
// It is always set at call time based upon the way it was invoked by its caller.
function hello(thing) {
    console.log(this + " says hello " + thing);
}

person = { name: "Brendan Eich" }
person.hello = hello;

person.hello("world") // still desugars to person.hello.call(person, "world")

hello("world") // "[object DOMWindow]world"

/**
 * Function.prototype.bind, fix this value, could not allow change this value
 */
var boundHello = person.hello.bind(person);
boundHello("world") // "Brendan Eich says hello world"

//trick in jquery when callback
var person = {
    name: "Alex Russell",
    hello: function() { console.log(this.name + " says hello world"); }
}
// also pass person as this, that trick used in callback to maintain the scope this
$("#some-div").click(person.hello.bind(person));

//another trick to deal with callback
function  a(){
    this.x = 0;
    var that = this;
    function y(){
        that.x = 3;
        console.log(that.x);
    }
    y();
    return this.x;
}
console.log(a());

// callback
var stateManager = {
    fly: function () {
        var self = this;
        $( "#container" )
            .unbind()
            .on( "click" , "div.toggle", function ( e ) {
                self.handleClick( e.target );
            });
    },

    handleClick: function ( elem ) {
        elem.find( "span" ).toggle( "slow" );
    }
};