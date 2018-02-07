/**
 * define all of our functions and variables in the private scope
 * and return an anonymous object with pointers to the private functionality
 * we wished to reveal as public.
 */
var myRevealingModule = (function () {
    var privateVar = "Ben Cherry",
        publicVar  = "Hey there!";

    function privateFunction() {
        console.log( "Name:" + privateVar );
    }
    function publicSetName( strName ) {
        privateVar = strName;
    }
    function publicGetName() {
        privateFunction();
    }

    // Reveal public pointers to
    // private functions and properties
    return {
        setName: publicSetName,
        greeting: publicVar,
        getName: publicGetName
    };

})();

myRevealingModule.setName( "Paul Kinlan" );