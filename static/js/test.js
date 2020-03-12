$(document).ready(function () {
    console.log("Hello world");

    var nameFunc = myFunc("John");
    var myString = nameFunc(18);
    console.log(myString); // Your name is John and your age is 18.

});

function myFunc(name) {
    return function (age) {
        return "Your name is " + name + " and your age is " + age;
    }
}



