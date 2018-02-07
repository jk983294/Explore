/**
 * promote code re-use
 * offered the ability to add behaviour to existing classes in a system dynamically
 */


/**
 * method 1
 */
function Vehicle( vehicleType ){
    this.vehicleType = vehicleType || "car";
    this.model = "default";
    this.license = "00000-000";
}
// Lets create a new instance of vehicle, to be decorated
var truck = new Vehicle( "truck" );

// New functionality we're decorating vehicle with
truck.setModel = function( modelName ){
    this.model = modelName;
};
truck.setColor = function( color ){
    this.color = color;
};

// Test the value setters and value assignment works correctly
truck.setModel( "CAT" );
truck.setColor( "blue" );
console.log( truck );

// Demonstrate "vehicle" is still unaltered, because it doesn't use prototype to add new function
var secondInstance = new Vehicle( "car" );
console.log( secondInstance );

/**
 * method 2
 */
function MacBook() {
    this.cost = function () { return 997; };
    this.screenSize = function () { return 11.6; };
}
// Decorators
function memory( macbook ) {
    var v = macbook.cost();
    macbook.cost = function() { return v + 75; };
}
function engraving( macbook ){
    var v = macbook.cost();
    macbook.cost = function(){ return  v + 200; };
}
function insurance( macbook ){
    var v = macbook.cost();
    macbook.cost = function(){ return  v + 250; };
}

var mb = new MacBook();
// New functionality we're decorating vehicle with
memory( mb );
engraving( mb );
insurance( mb );

console.log( mb.cost() );
console.log( mb.screenSize() );

/**
 * jquery way
 */
var decoratorApp = decoratorApp || {};

// define the objects we're going to use
decoratorApp = {
    defaults: {
        validate: false,
        limit: 5,
        name: "foo",
        welcome: function () {
            console.log( "welcome!" );
        }
    },
    options: {
        validate: true,
        name: "bar",
        helloWorld: function () {
            console.log( "hello world" );
        }
    },
    settings: {},
    printObj: function ( obj ) {
        var arr = [],
            next;
        $.each( obj, function ( key, val ) {
            next = key + ": ";
            next += $.isPlainObject(val) ? printObj( val ) : val;
            arr.push( next );
        } );
        return "{ " + arr.join(", ") + " }";
    }

};

// merge defaults and options, without modifying defaults explicitly
decoratorApp.settings = $.extend({}, decoratorApp.defaults, decoratorApp.options);

// what we have done here is decorated defaults in a way that provides
// access to the properties and functionality it has to offer (as well as
// that of the decorator "options"). defaults itself is left unchanged

$("#log").append( decoratorApp.printObj(decoratorApp.settings) +
        + decoratorApp.printObj(decoratorApp.options) +
        + decoratorApp.printObj(decoratorApp.defaults));

// settings -- { validate: true, limit: 5, name: bar, welcome: function (){ console.log( "welcome!" ); },
// helloWorld: function (){ console.log("hello!"); } }
// options -- { validate: true, name: bar, helloWorld: function (){ console.log("hello!"); } }
// defaults -- { validate: false, limit: 5, name: foo, welcome: function (){ console.log("welcome!"); } }



