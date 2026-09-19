# Day 9 – Main Points (JS)

aaj ka topic khtm hua? js me  

Screenshot 2026-05-26 085826.png me Day 9 ke jo 5 main points the:
1. Closures — function inside function ➡ ✅ Done (Dukaan aur Chotu wala concept)  
2. Closure practical use — counter, private var ➡ ✅ Done (Object wala Private Counter)  
3. Lexical scoping ➡ ✅ Done (Dada-Baap-Beta aur Scope Chain)  
4. IIFE ➡ ✅ Done (Hath-o-hath chalne wala patakha)  
5. Closure interview questions ➡ ✅ Done (var vs let loop panga aur value retention)  

Quant: Ratio + proportion x5.

### Scope — Local vs. Global  
Scope determines where your variables can be seen and used in your code.

**Global Scope**  
Variables declared outside of any function or block are global. They can be accessed from absolutely anywhere in your script.  
```js
const globalName = "John"; // Global
function test() {
  console.log(globalName); // Works! Accessible inside the function
}
```

**Local (Function) Scope**  
Variables declared inside a function are local to that function. They are locked inside, and the outside world cannot see them.  
```js
function secretRoom() {
  const secret = "Super Secret Key"; // Local
  console.log(secret); // Works inside
}
// console.log(secret); // Error! 'secret' is not defined out here
```