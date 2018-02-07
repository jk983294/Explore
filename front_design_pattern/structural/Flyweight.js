/**
 * optimizing code that is repetitive, slow and inefficiently shares data.
 * It aims to minimize the use of memory in an application by sharing
 * as much data as possible with related objects
 */

/**
 * Flyweights and sharing data
 */
// Simulate pure virtual inheritance/"implement" keyword for JS
Function.prototype.implementsFor = function( parentClassOrObject ){
    if ( parentClassOrObject.constructor === Function )
    {
        // Normal Inheritance
        this.prototype = new parentClassOrObject();
        this.prototype.constructor = this;
        this.prototype.parent = parentClassOrObject.prototype;
    }
    else
    {
        // Pure Virtual Inheritance
        this.prototype = parentClassOrObject;
        this.prototype.constructor = this;
        this.prototype.parent = parentClassOrObject;
    }
    return this;
};
// Flyweight object
var CoffeeOrder = {
    // Interfaces
    serveCoffee:function(context){},
    getFlavor:function(){}
};

// ConcreteFlyweight object that creates ConcreteFlyweight Implements CoffeeOrder
function CoffeeFlavor( newFlavor ){
    var flavor = newFlavor;
    // If an interface has been defined for a feature
    // implement the feature
    if( typeof this.getFlavor === "function" ){
        this.getFlavor = function() {
            return flavor;
        };
    }
    if( typeof this.serveCoffee === "function" ){
        this.serveCoffee = function( context ) {
            console.log("Serving Coffee flavor " + flavor + " to table number " + context.getTable());
        };
    }

}

// Implement interface for CoffeeOrder
CoffeeFlavor.implementsFor( CoffeeOrder );

// Handle table numbers for a coffee order
function CoffeeOrderContext( tableNumber ) {
    return{
        getTable: function() {
            return tableNumber;
        }
    };
}


function CoffeeFlavorFactory() {
    var flavors = {},
        length = 0;

    return {
        getCoffeeFlavor: function (flavorName) {

            var flavor = flavors[flavorName];
            if (typeof flavor === "undefined") {
                flavor = new CoffeeFlavor(flavorName);
                flavors[flavorName] = flavor;
                length++;
            }
            return flavor;
        },

        getTotalCoffeeFlavorsMade: function () {
            return length;
        }
    };
}

// Sample usage:
// testFlyweight()

function testFlyweight(){
    // The flavors ordered.
    var flavors = new CoffeeFlavor(),
    // The tables for the orders.
        tables = new CoffeeOrderContext(),
    // Number of orders made
        ordersMade = 0,
    // The CoffeeFlavorFactory instance
        flavorFactory;

    function takeOrders( flavorIn, table) {
        flavors[ordersMade] = flavorFactory.getCoffeeFlavor( flavorIn );
        tables[ordersMade++] = new CoffeeOrderContext( table );
    }

    flavorFactory = new CoffeeFlavorFactory();

    takeOrders("Cappuccino", 2);
    takeOrders("Cappuccino", 2);
    takeOrders("Frappe", 1);
    takeOrders("Frappe", 1);
    takeOrders("Xpresso", 1);
    takeOrders("Frappe", 897);
    takeOrders("Cappuccino", 97);
    takeOrders("Cappuccino", 97);
    takeOrders("Frappe", 3);
    takeOrders("Xpresso", 3);
    takeOrders("Cappuccino", 3);
    takeOrders("Xpresso", 96);
    takeOrders("Frappe", 552);
    takeOrders("Cappuccino", 121);
    takeOrders("Xpresso", 121);

    for (var i = 0; i < ordersMade; ++i) {
        flavors[i].serveCoffee(tables[i]);
    }
    console.log(" ");
    console.log("total CoffeeFlavor objects made: " +  flavorFactory.getTotalCoffeeFlavorsMade());
}

/**
 * DOM-layer where the Flyweight can be used as a central event-manager to
 * avoid attaching event handlers to every child element in a parent container
 * we wish to have some similar behavior.
 * two approaches that allow objects to detect events - either top down (event capture) or bottom up (event bubbling).
 *
 * Centralized event handling
 */