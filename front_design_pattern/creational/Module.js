/**
 * best practice
 * uses object literals but only as the return value from a scoping function.
 * provide both private and public encapsulation for classes
 * only a public API is returned, keeping everything else within the closure private.
 */
var testModule = (function () {
    /**
     * private variable, limited to within the module's closure
     */
    var counter = 0;
    return {
        incrementCounter: function () {
            return counter++;
        },
        resetCounter: function () {
            console.log( "counter value prior to reset: " + counter );
            counter = 0;
        }
    };
})();
// Usage:
testModule.incrementCounter();      // Increment our counter
// Check the counter value and reset
// Outputs: counter value prior to reset: 1
testModule.resetCounter();

/**
 * another example myNamespace
 */
var myNamespace = (function () {
    var myPrivateVar, myPrivateMethod;
    // A private counter variable
    myPrivateVar = 0;
    // A private function which logs any arguments
    myPrivateMethod = function( foo ) {
        console.log( foo );
    };
    return {
        // A public variable
        myPublicVar: "foo",
        // A public function utilizing privates
        myPublicFunction: function( bar ) {
            // Increment our private counter
            myPrivateVar++;
            // Call our private method using bar
            myPrivateMethod( bar );
        }
    };
})();


/**
 * Import mixins, how globals (e.g jQuery, Underscore) can be passed in as arguments to our module's anonymous function.
 */
// Global module
var myModule = (function ( jQ, _ ) {

    function privateMethod1(){
        jQ(".container").html("test");
    }

    function privateMethod2(){
        console.log( _.min([10, 5, 100, 2, 1000]) );
    }

    return{
        publicMethod: function(){
            privateMethod1();
        }
    };

// Pull in jQuery and Underscore
})( jQuery, _ );
myModule.publicMethod();

/**
 * not good practice
 * object literal notation
 */
var myModule = {
    myProperty: "someValue",
    myConfig: {
        useCaching: true,
        language: "en"
    },
    saySomething: function () {
        console.log( "Where in the world is Paul Irish today?" );
    },
    reportMyConfig: function () {
        console.log( "Caching is: " + ( this.myConfig.useCaching  ? "enabled" : "disabled") );
    },
    updateMyConfig: function( newConfig ) {
        if ( typeof newConfig === "object" ) {
            this.myConfig = newConfig;
            console.log( this.myConfig.language );
        }
    }
};
//usage
myModule.saySomething();
myModule.reportMyConfig();
myModule.updateMyConfig({
    language: "fr",
    useCaching: false
});
myModule.reportMyConfig();