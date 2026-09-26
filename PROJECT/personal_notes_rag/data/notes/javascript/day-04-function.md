# General

## Notes

Here is a clear, simple, and in-depth breakdown of all the JavaScript function concepts on your checklist today. Let's knock these out one by one!

1. Function Declaration vs. Function Expression

The main difference here is how they are written and hoisting (whether you can use them before they are defined).

Function Declaration

You declare a function directly using the function keyword.

Key Feature: They are hoisted, meaning JavaScript moves them to the top of the code before running it. You can call them before they appear in your code.

```javascript
// Calling it before it's written works!
greet();
function greet() {
 console.log("Hello there!");
}
```

Function Expression

You create a function and assign it to a variable.

Key Feature: They are not hoisted. You cannot call them before they are defined.

```javascript
// This would throw an error if called here!
// sayHi();
const sayHi = function() {
 console.log("Hi there!");
};
sayHi(); // Must call it after the expression
2. Arrow Functions () => {}
```

Arrow functions give you a shorter, cleaner way to write functions. They were introduced in ES6.

The Shortcut Rules:

1. If you only have one parameter, you don't need parentheses ().

2. If the function body has only one line of code, you can remove the curly braces {} and the return keyword. It returns automatically!

```javascript
// Regular Function Expression
const double = function(number) {
 return number * 2;
};
// Clean Arrow Function version
const doubleArrow = number => number * 2;
console.log(doubleArrow(5)); // 10
```

Note on this: Arrow functions do not have their own this context. They inherit it from the surrounding code.

3. Default + Rest Parameters

These features make your functions incredibly flexible when dealing with inputs.

Default Parameters

If someone forgets to pass an argument into your function, a default value steps in so your code doesn't crash or return undefined.

```javascript
function welcomeUser(name = "Guest") {
 console.log(`Welcome, ${name}!`);
```

18/09/2026, 23:58 day 04 -function

1/21

```javascript
}
welcomeUser("Alice"); // Welcome, Alice!
welcomeUser(); // Welcome, Guest! (Fallback kicks in)
```

Rest Parameters (...args)

The rest parameter allows a function to accept any number of arguments and bundles them all into a neat single array. You look for the three dots ....

```javascript
function sumAll(...numbers) {
 // 'numbers' is now an array: [1, 2, 3, 4]
 let total = 0;
 for (let num of numbers) {
 total += num;
 }
 return total;
}
console.log(sumAll(1, 2, 3, 4)); // 10
```

4. Return Values

A function is like a machine: you give it raw materials (parameters), it does some work, and return is the final product it hands back to you.

Once a function hits a return statement, it stops executing immediately. Any code written after that return inside the function is ignored.

If you don't explicitly use a return statement, the function automatically returns undefined by default.

```javascript
function calculateAge(birthYear) {
 return 2026 - birthYear;
 console.log("This will never print!"); // Ignored code
}
const myAge = calculateAge(2002);
console.log(myAge); // 24
```

5. Scope — Local vs. Global

Scope determines where your variables can be seen and used in your code.

Global Scope

Variables declared outside of any function or block are global. They can be accessed from absolutely anywhere in your script.

```javascript
const globalName = "John"; // Global
function test() {
 console.log(globalName); // Works! Accessible inside the function
}
```

Local (Function) Scope

Variables declared inside a function are local to that function. They are locked inside, and the outside world cannot see them.

```javascript
function secretRoom() {
 const secret = "Super Secret Key"; // Local
 console.log(secret); // Works inside
}
// console.log(secret); // Error! 'secret' is not defined out here
```

Which of these topics would you like to practice writing a few interactive code examples for first?

## Doubt: bhai isko apni langauge me smjha blk desi me

Q: bhai isko apni langauge me smjha blk desi me

Ekdum chill hoke suno, saare concepts dimaag me fit ho jayenge.

1. Function Declaration vs Expression (Kaam karne ke do tareeqe)

Bhai, function samajh le ek kaam karne wala banda hai. Isko bulane ke do tareeqe hain:

18/09/2026, 23:58 day 04 -function

2/21

Function Declaration (Dada banda - Hoisting)

Isme tum bande ko seedha naam dekar khada kar dete ho.

Fayda (Hoisting): Yeh banda itna haazir-jawaab hai ki isko kaam par lagane se pehle, tum isko upar kahin se bhi aawaaz maar sakte ho. Yeh poore code me sabse upar pehle hi register ho jata hai.

```javascript
// Function neeche likha hai, par aawaaz pehle hi maar di!
bulao();
function bulao() {
 console.log("Haan bhai, hazir hoon!");
}
```

Function Expression (Darpok banda - No Hoisting)

Isme tum pehle ek variable (dabba) banate ho aur function ko us dabbe me band kar dete ho.

Nuksaan: Yeh pehle se tayyar nahi rehta. Agar tumne isko iski line se pehle aawaaz maar di, to yeh ro dega (Error de dega). Isko pehle banana padega, uske baad hi use kar sakte ho.

```javascript
// Pehle variable me daalna zaroori hai
const chalBhai = function() {
 console.log("Ab mai chalne ko taiyar hoon!");
};
chalBhai(); // Yeh line ke baad hi chalega
```

2. Arrow Functions () => {} (Modern zamaane ka shortcut)

Pehle log lamba-chauda function keyword likhte the. Fir ES6 aaya aur bola—"Chhoro yaar, itna kaat-baat kyun karni, shortcut marte hain!" * function keyword ko maar diya goli.

Beech me laga diya ek teer (arrow) =>.

```javascript
// Purana boring tareeqa
const square = function(x) {
 return x * x;
};
// Naya mast tareeqa (Ek line me kaam khatam)
const squareArrow = x => x * x;
```

Dhyaan rakhna: Agar sirf ek hi line ka kaam hai, to na {} lagane ki zaroorat hai, na return likhne ki. Yeh apne aap samajh jata hai.

3. Default + Rest Parameters (Jugadu Settings)

Default Parameters (Backup plan)

Suno, tumne ek function banaya jo dosto ko party ka invitation bhejta hai. Agar kisi ne dost ka naam bhejna bhool gaya, to wahan undefined likha na aaye, isiliye hum ek backup naam set kar dete hain.

```javascript
function partyBulao(naam = "Mere Bhai") {
 console.log(`Party me aaja, ${naam}!`);
}
partyBulao("Rahul"); // Output: Party me aaja, Rahul!
partyBulao(); // Output: Party me aaja, Mere Bhai! (Backup chal gaya)
```

Rest Parameters (...sabKuch)

Yeh ek bada thaila hai. Tum function ko 2, 4 ya 10 items de do, yeh ... (teen dots) un sabko samet kar ek array (list) me daal deta hai.

```javascript
// Is thaile me jitne chaho numbers phenk ke maaro
function kharchaCalculator(...saareKharche) {
 // saareKharche ab ek array ban chuka hai: [100, 50, 200]
 console.log(saareKharche);
}
kharchaCalculator(100, 50, 200);
```

4. Return Values (Kaam ka hisaab-kitaab)

18/09/2026, 23:58 day 04 -function

3/21

Function ek dukan ki tarah hai. Tumne usko paise diye (parameters), usne andar kaam kiya, aur aakhiri me jo maal tumhare haath me thamaya, woh hai return.

Rule 1: Jaise hi function me return chala, function wahin khatam! Uske neeche tum chahe jo likh do, code chalega hi nahi.

Rule 2: Agar tumne function me kuch return nahi kiya, to JS tumko thullu (undefined) pakda dega.

```javascript
function hisaab(a, b) {
 return a + b; // Maal wapas bhej diya
 console.log("Yeh to kabhi chalega hi nahi, bhool jao");
}
let total = hisaab(10, 20); // total me 30 aa gaya
```

5. Scope — Local vs Global (Ghar ka mamla vs Mohalle ka mamla)

Global Scope (Mohalle ka nalka)

Jo variable tumne kisi function ke andar nahi, balki ekdum baahar khule me banaya hai. Woh Global hai. Use mohalle ka koi bhi function utha kar use kar sakta hai.

```javascript
let mohalleKaNalka = "Paani";
function gharOne() {
 console.log(mohalleKaNalka); // Bilkul use kar sakta hai!
}
```

Local Scope (Ghar ke andar ka personal saman)

Jo variable tumne kisi function ke {} ke andar bana diya, woh Local ho gaya. Woh us function ki personal property hai. Baahar ka koi banda usko chhoo bhi nahi sakta.

```javascript
function gharTwo() {
 let personalTijori = "10 Lakh Rupee"; // Local hai
 console.log(personalTijori); // Ghar ke andar chalega
}
// console.log(personalTijori); // ERROR! Baahar waalo ko ghanta nahi dikhega
```

Bhai, ab batao, isme se kisi topic ka live code run karke dikhaun ya Quant ke P&L (Profit & Loss) wale 5 questions par chalein?

## Doubt: bhai isko theory ke sath sath code krke hai. phle number 1 krte hai

Q: bhai isko theory ke sath sath code krke hai. phle number 1 krte hai

Bhai, ekdum sahi tareeqa hai. Jab tak khud code karke haath gande nahi karoge, tab tak feel nahi aayegi.

Chalo sabse pehle Topic 1: Function Declaration vs Expression ko code ke sath poora cheer-phaad karte hain.

Apne VS Code ya browser ka console khol lo aur mere sath dekho.

Part 1: Function Declaration (Seedha aur Saral)

Yeh bilkul waise hi hai jaise hum school me seekhte hain. function keyword lagaya, ek achha sa naam diya, aur baaki ka kaam brackets ke andar.

Code Example:

```javascript
// 1. Pehle humne function ko call kiya (Awaaz maari)
sayHello();
// 2. Function banaya neeche hai
function sayHello() {
 console.log("Hey bhai! Kaise ho?");
}
```

Isme chal kya raha hai? (The Theory)

Yahan dimaag me ek sawaal aana chahiye: "Bhai, code to upar se neeche chalta hai, to line number 2 par jab humne call kiya, tab tak toh JavaScript ko pata hi nahi tha ki sayHello kya hai! Fir error kyun nahi aaya?"

Iska jawab hai Hoisting (Upar khichna).

JavaScript jab tumhara code chalata hai, to woh sabse pehle poore page me ghoomkar saare Function Declarations ko dhoondhta hai aur unhe dimaag me sabse upar (top pe) bitha deta hai. Isiliye tum isko poore file me kahin se bhi call karo, yeh hamesha chalega.

18/09/2026, 23:58 day 04 -function

4/21

Part 2: Function Expression (Variable me band banda)

Yahan hum thoda alag khelte hain. Hum function ko aazaad nahi chhodte, balki ek variable banate hain (jaise let ya const) aur function ko uske andar daal dete hain.

Code Example:

```javascript
// Agar tum isko yahan call karoge: sayBye();
// TO ERROR AAYEGA: "Cannot access 'sayBye' before initialization"
// Humne variable me function daal diya
const sayBye = function() {
 console.log("Chalo bhai, milte hain baad me!");
};
// Ab variable ke naam ke aage () lagakar call karo
sayBye(); // Yeh ekdum makkhan chalega!
```

Isme chal kya raha hai? (The Theory)

Function Expression me Hoisting nahi hoti. JavaScript isko ek normal variable ki tarah treat karta hai. Jab tak code line-by-line chalkar const sayBye wali line par nahi pahunchega, tab tak JavaScript ko ghanta nahi pata ki sayBye kya cheez hai.

Isiliye, isko tum pehle nahi chala sakte, hamesha banane ke baad hi chalana padega.

Quick Revision Table (Bolo Zuban Kesari)

Feature Function Declaration Function Expression

```javascript
Syntax function naam() { ... } const naam = function() { ... }
```

Hoisting Haan bhai! (Upar khinch jata hai) Na bhai na! (Wahin rehta hai)

Kab call karein? Banane se pehle ya baad me, kahin bhi. Sirf banane ke baad me.

Ab tumhari baari (Chota sa task)

Apne console me ek baar ek Function Declaration banao jo do numbers ko multiply kare, aur ek Function Expression banao jo tumhara naam print kare.

Jab yeh dono chal jayein, to mujhe batao, fir Number 2 (Arrow Functions) par toot padenge!

## Doubt: iske short note de do bro for revision easy eng me

Q: iske short note de do bro for revision easy eng me

Bhai, ekdum crisp aur short notes, tumhare revision ke liye. Isko save karke rakh lo, exam se pehle bas 2 minute dekhoge to sab yaad aa jayega!

📝 Revision Notes: Topic 1 (Declaration vs Expression)

1. Function Declaration

What is it? Creating a function directly with the function keyword and a name.

Hoisting: YES. JavaScript moves it to the top of the file automatically.

Call Timing: You can call it before or after you write it in the code.

```javascript
// You can call it here (Before)
greet();
function greet() {
 console.log("Hello!");
}
```

2. Function Expression

What is it? Creating a function and storing it inside a variable (const or let).

Hoisting: NO. It behaves like a normal variable.

18/09/2026, 23:58 day 04 -function

5/21

Call Timing: You can ONLY call it after the line where it is defined. Calling it before will throw an error.

```javascript
// Calling it here will crash the code! ❌
const sayHi = function() {
 console.log("Hi!");
};
sayHi(); // Call it here (After)
```

⚡ Quick Comparison Table

Feature Function Declaration Function Expression

```javascript
Syntax function myFunc() {} const myFunc = function() {}
```

## Hoisted? Yes  No

When to call? Anywhere in the file Only after defining it

Bhai, yeh ready hai!

## Doubt: next part

Q: next part

Bhai, ab aate hain Topic 2: Arrow Functions () => {} par. Yeh JavaScript ka sabse stylish aur modern tareeqa hai function likhne ka.

Chalo pehle iska poora mamla samajhte hain, fir code karenge, aur aakhiri me iske mast short notes milenge.

Part 1: Arrow Function Kya Hai? (The Theory)

ES6 (2015) me JavaScript waalo ne socha ki yaar, baar-baar function aur return likh kar haath dard ho jata hai. Kuch aisa banate hain jo dekhne me chota ho aur likhne me makkhan.

To unhone Arrow Function nikaala. Isme se function keyword ko delete kar diya aur parameters ke aage ek teer (=>) laga diya.

The Magic Rules (Shortcuts):

1. No function keyword: Iski zaroorat hi nahi hai.

2. One Parameter Rule: Agar function me sirf ek hi input (parameter) ja raha hai, to tum brackets () ko bhi hata sakte ho.

3. One Line Rule: Agar function ke andar sirf ek hi line ka code hai, to curly braces {} aur return keyword dono ko hata do. JavaScript apne aap samajh jayega ki is line ko return karna hai! (Isko Implicit Return bolte hain).

Part 2: Code Karke Dekhte Hain

Chalo ek normal function expression ko step-by-step Arrow Function me badalte hain.

1. Normal Tareeqa (Purana)

```javascript
const double = function(number) {
 return number * 2;
};
console.log(double(5)); // Output: 10
```

2. Arrow Function (Pehle step me badla)

Humne function hataya aur => lagaya:

```javascript
const doubleArrow = (number) => {
 return number * 2;
};
```

3. Ekdum Pro Tareeqa (Shortcut lagakar)

Kyunki sirf ek parameter hai (number) aur ek hi line ka kaam hai (number * 2), sab f ◌ालतू cheezein uda do:

```javascript
const doublePro = number => number * 2;
console.log(doublePro(5)); // Output: 10 (Ekdum clean!)
```

18/09/2026, 23:58 day 04 -function

6/21

📝 Revision Notes: Topic 2 (Arrow Functions)

What is it? A shorter and modern way to write functions using =>.

```javascript
Syntax: const myFunc = (param) => { code }
```

Shortcut 1: No brackets () needed if there is only 1 parameter.

Shortcut 2: No {} and no return needed if it's a 1-line code.

Limitation: Arrow functions do not have their own this keyword (yeh jab tum Objects padhoge tab bohot kaam aayega).

Quick Code Snippets for Revision:

```javascript
// 0 Parameters
const sayHi = () => "Hello Bhai!";
// 1 Parameter (No parenthesis needed)
const square = x => x * x;
// Multiple Parameters (Parenthesis required)
const add = (a, b) => a + b;
```

Bhai, Arrow Function dimaag me fit hua? Agar haan, to batao fir Topic 3: Default + Rest Parameters par chalein?

## Notes

Bhai, ab aate hain Topic 3: Default + Rest Parameters par. Yeh dono features tumhare functions ko ekdum flexible aur jugadu bana dete hain taaki alag-alag inputs par tumhara code kabhie phate na (crash na ho).

Chalo pehle dono ko alag-alag samajhte hain, fir code karenge aur aakhiri me short notes!

Part 1: Default Parameters (The Backup Plan)

The Theory

Socho tumne ek function banaya jo user ko "Good Morning" wish karta hai. Ab agar koi user apna naam dena bhool gaya, to JavaScript output me Good Morning undefined dikha dega, jo dekhne me bohot ganda lagta hai.

Default Parameters hume yeh azaadi dete hain ki agar koi bahar se value na bhejkar bhool jaye, to function apne aap ek backup value utha le.

Code Example:

```javascript
// Humne naam ke aage hi "=" lagakar backup value "Bhai" set kar di
function sayGharKaNaam(naam = "Bhai") {
 console.log(`Aur batao, kaise ho ${naam}?`);
}
sayGharKaNaam("Rahul"); // Output: Aur batao, kaise ho Rahul?
sayGharKaNaam(); // Output: Aur batao, kaise ho Bhai? (Backup chal gaya!)
```

Part 2: Rest Parameters (...sabKuch)

The Theory

"Rest" ka matlab hota hai "baaki ka bacha kucha". Jab tumhe nahi pata ki samne wala bande function me kitne arguments bhejne wala hai (2 bhejega, 5 bhejega, ya 50 bhejega), tab tum Rest Parameter ka use karte ho.

Iski pehchan hoti hai teen dots .... Yeh saare bache-kuche inputs ko samet kar ek Array (List) me pack kar deta hai.

Code Example:

```javascript
// ...items saare numbers ko ek list me daal dega
function addCartItems(...items) {
 // 'items' ab ek array ban gaya hai: [100, 250, 400, 50]
 let total = 0;

 for(let price of items) {
 total += price;
 }
 return total;
```

18/09/2026, 23:58 day 04 -function

7/21

```javascript
}
// Tum chahe jitne items pass karo, yeh sabko sambhal lega
console.log(addCartItems(100, 250, 400, 50)); // Output: 800
```

Bade Bhai Ka Gyaan ⚠ : Rest parameter hamesha function ke parameters me sabse aakhiri me hona chahiye. Tum function khana(a, b, ...baakiKa) likh sakte ho, par function khana(...baakiKa, a) nahi likh sakte. JavaScript confuse ho jayega!

📝 Revision Notes: Topic 3 (Default & Rest)

1. Default Parameters

Purpose: Sets a backup value if an argument is missing or undefined.

```javascript
Syntax: function myFunc(param = "Default Value") {}
```

2. Rest Parameters (...)

Purpose: Collects multiple single arguments into a single Array.

```javascript
Syntax: function myFunc(...allArgs) {}
```

Rule: Must always be the last parameter in the function list.

```javascript
// Cheat Sheet Example
function test(a, b = 10, ...c) {
 console.log(a, b, c);
}
test(5); // Output: 5, 10, []
test(5, 20, 1, 2); // Output: 5, 20, [1, 2]
```

Bhai, dono parameters clear hain dimaag me? Ab chala jaye Topic 4: Return Values par?

## Doubt: topic 4

Q: topic 4

Bhai, ab toot padte hain Topic 4: Return Values par. Yeh topic bohot seedha hai, par isme do aise rules hain jahan aksar log galti kar baithte hain.

Chalo iska poora post-mortem karte hain!

Part 1: Return Value Kya Hai? (The Theory)

Function ko tum ek ATM Machine ki tarah samajho. Tumne apna card dala aur PIN daala (Inputs/Parameters), machine ne andar processing ki, aur aakhiri me tumhe cash nikaal kar de diya. Woh cash hi tumhara return value hai.

Agar function kuch return nahi kar raha, to woh bas andar hi andar kaam karke shaant ho jata hai, tum uske result ko baahar kisi variable me save nahi kar sakte.

Do Sabse Zaroori Rules:

1. The Full Stop Rule: Jaise hi JavaScript function ke andar return keyword ko dekhta hai, woh function ko wahin ke wahin khatam kar deta hai. Uske neeche tum chahe jo likh do, woh line kabhi execute nahi hogi.

2. The Undefined Rule: Agar tumne function se kuch bhi return nahi karwaya, to JavaScript gusse me tumko default value undefined pakda dega.

Part 2: Code Karke Dekhte Hain

1. Sahi Tareeqa (Returning a Value)

```javascript
function calculateDiscount(price, discount) {
 let finalPrice = price - discount;
 return finalPrice; // Maal baahar bhej diya
}
// Ab hum is return value ko ek variable me save kar sakte hain
const myBill = calculateDiscount(500, 50);
console.log(myBill); // Output: 450
```

2. Return ke baad ka dhoka (Full Stop Rule)

18/09/2026, 23:58 day 04 -function

8/21

```javascript
function testReturn() {
 console.log("Yeh line chalegi.");
 return "Kaam Khatam!";

 // Yeh line kabhi nahi chalegi kyunki upar return ho chuka hai
 console.log("Mujhe to bhool hi gaye bhai!");
}
console.log(testReturn());
```

3. Jab return lagana bhool jao (Undefined Rule)

```javascript
function noReturnFunc(a, b) {
 let sum = a + b; // Kaam toh kiya, par baahar nahi bheja
}
const result = noReturnFunc(10, 20);
console.log(result); // Output: undefined (Kyunki return gayab hai!)
```

📝 Revision Notes: Topic 4 (Return Values)

What is it? The output that a function sends back to the place where it was called.

The Exit Gate: return stops the function immediately. No code runs after it inside that function.

Missing Return: If a function has no return statement, it automatically returns undefined.

```javascript
// Quick Check Cheat Sheet
const multiplication = (a, b) => {
 return a * b; // Exits here
 console.log("No"); // Dead code
};
```

Bhai, return ka mamla ekdum saaf? Ab chalte hain aaj ke aakhiri aur sabse mazaedaar JS topic par—Topic 5: Scope (Local vs Global). Shuru karein?

## Notes

Bhai, ab aate hain aaj ke aakhiri JS topic par—Topic 5: Scope (Local vs Global).

Isko samajhne ke liye bas ek line dimaag me bitha lo: "Ghar ka mamla vs Mohalle ka mamla". Scope hume batata hai ki kaun sa variable code me kahan se dikh raha hai aur kahan se nahi.

Part 1: Scope Kya Hai? (The Theory)

JavaScript me teen tarah ke scope hote hain jo tumhare variables ki boundary taiyaar karte hain:

1. Global Scope (Mohalle ka nalka)

Jo variable tumne kisi bhi function ya curly braces {} ke baahar khule me banaya hai, woh Global hai.

Isko poore code me koi bhi function, arrow function ya loop utha kar use kar sakta hai.

2. Local / Function Scope (Ghar ke andar ka personal saman)

Jab tum kisi variable ka janm ek function ke andar {} ke beech me karte ho, to woh sirf usi function ke andar zinda rehta hai.

Function ke baahar nikalte hi woh mar jata hai. Baahar waale use access nahi kar sakte.

3. Block Scope (Tijori ke andar ka maal)

Yeh let aur const ke aane ke baad aaya. Agar tumne let ya const ko kisi normal curly braces {} ke andar banaya—jaise koi if condition ya for loop—to woh sirf un braces ke andar hi kaam karega. (Dhyaan rakhna, purana var block scope ko nahi maanta, par hume var use nahi karna hai!).

Part 2: Code Karke Dekhte Hain

1. Global vs Local Code

```javascript
let mohalleKaNalka = "Paani"; // Global Variable
function ghar() {
```

18/09/2026, 23:58 day 04 -function

9/21

```javascript
 let personalTijori = "Ghehna"; // Local Variable

 console.log(mohalleKaNalka); // 1. Chalega! (Ghar ke andar mohalle ka paani aa sakta hai)
 console.log(personalTijori); // 2. Chalega! (Ghar ke andar apna saman dikhega)
}
ghar();
console.log(mohalleKaNalka); // 3. Chalega! (Baahar khule me nalka dikh raha hai)
// console.log(personalTijori); // 4. ERROR! Baahar ke logo ko ghar ki tijori nahi dikhegi
```

2. Block Scope Code (if ya for ke andar)

```javascript
if (true) {
 let blockVariable = "Mai sirf is IF ke andar chalunga";
 console.log(blockVariable); // Ekdum mast chalega
}
// console.log(blockVariable); // ERROR! Braces ke baahar aate hi khatam
```

📝 Revision Notes: Topic 5 (Scope)

Global Scope: Variables defined outside any function/block. Accessible everywhere.

Local Scope: Variables defined inside a function. Accessible only inside that function.

Block Scope: Variables defined with let/const inside {} (like if or for). Accessible only inside those brackets.

```javascript
// Quick Scope Visualizer
const globalVar = " 🌍 ";
function testScope() {
 const localVar = " 🏠 ";
 if (true) {
 const blockVar = " 📦 ";
 // Here you can see: 🌍 , 🏠 , 📦
 }
 // Here you can see: 🌍 , 🏠 ( 📦 is dead)
}
// Here you can see: 🌍 ( 🏠 and 📦 are dead)
```