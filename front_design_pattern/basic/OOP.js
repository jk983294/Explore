/**
 * 1. private variables are declared with the 'var' keyword inside the object,
 * and can only be accessed by private functions and privileged methods.
 * 2. private functions are declared inline inside the object's constructor
 * (or alternatively may be defined via var functionName=function(){...})
 * and may only be called by privileged methods (including the object's constructor).
 * 3. privileged methods are declared with this.methodName=function(){...}
 * and may invoked by code external to the object.
 * 4. public properties are declared with this.variableName
 * and may be read/written from outside the object.
 * 5. public methods are defined by Classname.prototype.methodName = function(){...}
 * and may be called from outside the object.
 * 6.prototype properties are defined by Classname.prototype.propertyName = someValue
 * 7. static properties are defined by Classname.propertyName = someValue
 */
function Person(n,race){
    this.constructor.population++;

    // ************************************************************************
    // PRIVATE VARIABLES AND FUNCTIONS
    // ONLY PRIVELEGED METHODS MAY VIEW/EDIT/INVOKE
    // ***********************************************************************
    var alive=true, age=1;
    var maxAge=70+Math.round(Math.random()*15)+Math.round(Math.random()*15);
    function makeOlder(){ return alive = (++age <= maxAge) }

    var myName=n?n:"John Doe";
    var weight=1;


    // ************************************************************************
    // PRIVILEGED METHODS
    // MAY BE INVOKED PUBLICLY AND MAY ACCESS PRIVATE ITEMS
    // MAY NOT BE CHANGED; MAY BE REPLACED WITH PUBLIC FLAVORS
    // ************************************************************************
    this.toString=this.getName=function(){ return myName }

    this.eat=function(){
        if (makeOlder()){
            this.dirtFactor++;
            return weight*=3;
        } else alert(myName+" can't eat, he's dead!");
    }
    this.exercise=function(){
        if (makeOlder()){
            this.dirtFactor++;
            return weight/=2;
        } else alert(myName+" can't exercise, he's dead!");
    }
    this.weigh=function(){ return weight }
    this.getRace=function(){ return race }
    this.getAge=function(){ return age }
    this.muchTimePasses=function(){ age+=50; this.dirtFactor=10; }


    // ************************************************************************
    // PUBLIC PROPERTIES -- ANYONE MAY READ/WRITE
    // ************************************************************************
    this.clothing="nothing/naked";
    this.dirtFactor=0;
}


// ************************************************************************
// PUBLIC METHODS -- ANYONE MAY READ/WRITE
// ************************************************************************
Person.prototype.beCool = function(){ this.clothing="khakis and black shirt" }
Person.prototype.shower = function(){ this.dirtFactor=2 }
Person.prototype.showLegs = function(){ alert(this+" has "+this.legs+" legs") }
Person.prototype.amputate = function(){ this.legs-- }


// ************************************************************************
// PROTOTYOPE PROERTIES -- ANYONE MAY READ/WRITE (but may be overridden)
// ************************************************************************
Person.prototype.legs=2;


// ************************************************************************
// STATIC PROPERTIES -- ANYONE MAY READ/WRITE
// ************************************************************************
Person.population = 0;



// Here is the code that uses the Person class
function RunGavinsLife(){
    var gk=new Person("Gavin","caucasian");       //New instance of the Person object created.
    var lk=new Person("Lisa","caucasian");        //New instance of the Person object created.
    alert("There are now "+Person.population+" people");

    gk.showLegs(); lk.showLegs();                 //Both share the common 'Person.prototype.legs' variable when looking at 'this.legs'

    gk.race = "hispanic";                         //Sets a public variable, but does not overwrite private 'race' variable.
    alert(gk+"'s real race is "+gk.getRace());    //Returns 'caucasian' from private 'race' variable set at create time.
    gk.eat(); gk.eat(); gk.eat();                 //weight is 3...then 9...then 27
    alert(gk+" weighs "+gk.weigh()+" pounds and has a dirt factor of "+gk.dirtFactor);

    gk.exercise();                                //weight is now 13.5
    gk.beCool();                                  //clothing has been update to current fashionable levels
    gk.clothing="Pimp Outfit";                    //clothing is a public variable that can be updated to any funky value
    gk.shower();
    alert("Existing shower technology has gotten "+gk+" to a dirt factor of "+gk.dirtFactor);

    gk.muchTimePasses();                          //50 Years Pass
    Person.prototype.shower=function(){           //Shower technology improves for everyone
        this.dirtFactor=0;
    }
    gk.beCool=function(){                         //Gavin alone gets new fashion ideas
        this.clothing="tinfoil";
    };

    gk.beCool(); gk.shower();
    alert("Fashionable "+gk+" at "
        +gk.getAge()+" years old is now wearing "
        +gk.clothing+" with dirt factor "
        +gk.dirtFactor);

    gk.amputate();                                //Uses the prototype property and makes a public property
    gk.showLegs(); lk.showLegs();                 //Lisa still has the prototype property

    gk.muchTimePasses();                          //50 Years Pass...Gavin is now over 100 years old.
    gk.eat();                                     //Complains about extreme age, death, and inability to eat.
}