/**
 * 1. You cause a class to inherit using ChildClassName.prototype = new ParentClass();.
 * 2. You need to remember to reset the constructor property for the class
 * using ChildClassName.prototype.constructor=ChildClassName.
 * 3. You can call ancestor class methods which your child class has overridden using the Function.call() method.
 * 4. Javascript does not support protected methods.
 */
function Mammal(name){
    this.name=name;
    this.offspring=[];
}
Mammal.prototype.haveABaby=function(){
    var newBaby=new Mammal("Baby "+this.name);
    this.offspring.push(newBaby);
    return newBaby;
}
Mammal.prototype.toString=function(){
    return '[Mammal "'+this.name+'"]';
}


Cat.prototype = new Mammal();        // Here's where the inheritance occurs
Cat.prototype.constructor=Cat;       // Otherwise instances of Cat would have a constructor of Mammal
function Cat(name){
    this.name=name;
}
Cat.prototype.toString=function(){
    return '[Cat "'+this.name+'"]';
}





Function.prototype.inheritsFrom = function( parentClassOrObject ){
    if ( parentClassOrObject.constructor == Function )
    {
        //Normal Inheritance
        this.prototype = new parentClassOrObject;
        this.prototype.constructor = this;
        this.prototype.parent = parentClassOrObject.prototype;
    }
    else
    {
        //Pure Virtual Inheritance
        this.prototype = parentClassOrObject;
        this.prototype.constructor = this;
        this.prototype.parent = parentClassOrObject;
    }
    return this;
}
//
//
LivingThing = {
    beBorn : function(){
        this.alive = true;
    }
}
//
//
function Mammal(name){
    this.name=name;
    this.offspring=[];
}
Mammal.inheritsFrom( LivingThing );
Mammal.prototype.haveABaby=function(){
    this.parent.beBorn.call(this);
    var newBaby = new this.constructor( "Baby " + this.name );
    this.offspring.push(newBaby);
    return newBaby;
}
//
//
function Cat( name ){
    this.name=name;
}
Cat.inheritsFrom( Mammal );
Cat.prototype.haveABaby=function(){
    var theKitten = this.parent.haveABaby.call(this);
    alert("mew!");
    return theKitten;
}
Cat.prototype.toString=function(){
    return '[Cat "'+this.name+'"]';
}
//
//
var felix = new Cat( "Felix" );
var kitten = felix.haveABaby( ); // mew!
alert( kitten );                 // [Cat "Baby Felix"]

var someAnimal = new Mammal('Mr. Biggles');
var myPet = new Cat('Felix');
alert('someAnimal is '+someAnimal);   // results in 'someAnimal is [Mammal "Mr. Biggles"]'
alert('myPet is '+myPet);             // results in 'myPet is [Cat "Felix"]'

myPet.haveABaby();                    // calls a method inherited from Mammal
alert(myPet.offspring.length);        // shows that the cat has one baby now
alert(myPet.offspring[0]);            // results in '[Mammal "Baby Felix"]'