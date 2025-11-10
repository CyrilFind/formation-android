---
marp: true
---

<!-- headingDivider: 2 -->

# Kotlin

![bg right:30% 80%](../assets/kotlin.png)

## Intro

![bg right:30% 80%](../assets/kotlin.png)

- Moderne, Concis
- Orienté Objet / Fonctionnel
- Java Interop
- Développé par JetBrains
- Kotlin everywhere: JVM, Backend, JS, KTS, iOS...
- Pour Android on est sur la JVM: garbage collector, etc

## Typage statique inféré

```kotlin
// explicit
val myInt: Int = 1

// implicit
val myInt = 1
val myString = "coucou"
val myUser = User()

val myList = listOf(0f, 0.5f, 1f) // List<Float>
val emptyList = emptyList<Double>() // List<Double>
```

## Mutabilité

```kotlin
// valeur primitive fixée à la compilation qui ne peut pas changer
const val APP_ID = 42424242

// valeur donnée à l'execution qui ne peut pas changer ensuite
val user = 0
user = 1 // ❌ ne compile pas

// valeur qui peut changer
var myMutableVariable = 0
myMutableVariable = 1

// structure de données mutables ou immutables, ex: listes
val immutableList = listOf(1, 2, 3)
immutableList.add(4) // ❌ la méthode n'existe pas

val mutableList = mutableListOf(1, 2, 3)
mutableList.add(4) // ✅
```

## Nullabilité

```kotlin
var user: User? = null
user = getUser()

// soft unwrap: exécute ou retourne null si l'instance est null
val name: String? = user?.name

// force unwrap: exécute OU crash si l'instance est nulle
val name: String = user!!.toString()

// elvis operator: exécute la partie à droite si la partie à gauche est null
val name: String = user?.name ?: "none"

// let: extension qui permet de manipuler une instance dans une lambda
// souvent utilisé avec des instances nullables
val name: String = user?.let { it.name } ?: "none"
```

⚠️ `@Nullable` pour l'interopérabilité avec Java

## Smart casts

```kotlin
var user: User?

user?.connect()

if (user != null) user.connect()
```

## When statements

Un `switch-case` en plus puissant:

```kotlin
val primeNumbers = listOf(1, 3, 5, 7, 11, 13, 17)

val x: Any? = 13

val result = when(x) {
    null -> "x is null" // ❌ -> smart casté comme Any
    !is Int -> "x is not an int" // ❌ -> smart casté comme Int
    in 1..10 -> "x is between 1 and 10" // ❌
    !in 10..20 -> "x is not between 10 and 20" // ❌
    in primeNumbers -> "x is a prime" // ✅
    else -> "none of the above" // ignoré
}

print(result)
```

## Loops

```kotlin
val list = listOf(1, 2, 3, 4, 5)

for (i in 0..4) {
  print(list[i])
}

for (element in list) {
  print(element)
}

list.forEach { element ->
  print(element)
}

// while, do while, etc
```

## Functions

```kotlin
fun add(
  first: Int,
  second: Int,
) : Int {
  var result: Int
  result = first + second
  return result
}

// short syntax
fun add(first: Int, second: Int) = first + second
```

## Classes

```kotlin
open class User(login: String) {// final by default: `open` for inheritage
  open fun connect() {}
}

class Student(// declaration and primary constructor
  login: String, // constructor argument
  public val subjects: List<Subject> = emptyList(), // public property (default)
) : User(login) { // parent constructor
    private val email: String // private property

    // secondary constructor
    constructor(firstname: String, lastname: String) : this("$firstname_$lastname")

    init { // additional constructor logic
      email = "$login@school.com"
    }

    override fun connect() { // override parent method
      super.connect() // call parent method
      // additional logic
    }
}
```

## Object

Permet de créer facilement un Singleton (~`static class` en Java)

```kotlin
object Analytics {
  fun trackLoginEvent() { ... }
}

Analytics.trackLoginEvent()
```

## Companion object

Permet d'avoir l'équivalent des membres `static` en Java:

```kotlin
class Math {

  companion object {
    const val PI = 3.14159265359
  }
}

Math.PI // interop java: MyClass.Companion.MY_CONSTANT
```

## Data class

`equals(), toString(), hashCode(), copy()` et destructuration sans rien coder !

```kotlin
data class Point(val x: Float, val y: Float)

val pointA = Point(1.0f, 2.0f)

val (x, y) = pointA

val pointB = pointA.copy(y = 1.0f)

pointB.toString() // Point(x=1.0f, y=1.0f)

val pointC = Point(1.0f, 2.0f)
pointA == pointC // ➡️ true
```

## Enum class

```kotlin
enum class Color {
  RED, GREEN, BLUE
}

enum class Color(val rgb: Int) {
  RED(0xFF0000),
  GREEN(0x00FF00),
  BLUE(0x0000FF),
}
```

## Sealed class

Classes ayant un nombre de sous classes défini et limité

```kotlin
sealed class Result {
  class Success(val value: Any) : Result()
  class Failure(val error: Error) : Result()
  object Loading : Result()
}

// utile avec les smart cast
when (result) {
  is Result.Success -> display(result.value)
  is Result.Failure -> log(result.error)
  is Result.Loading -> displayLoader()
}
```

## Extensions

```kotlin
fun capitalize(string: String): String { // function
  return string
}

fun String.capitalize(): String { // function
  return ...
}

val String.titlecased // property
  get() = this.capitalize()

"hello".capitalize() // ➡️ "Hello"
```

## Lambdas

Blocs d'execution qui se manipulent en tant que variables:

```kotlin
val add: (Int, Int) -> Int = { a, b -> a + b }
add(1, 2) // ➡️ 3

fun applyToSelf(number: Int, operation: (Int, Int) -> Int) {
    operation(number, number)
 }

applyToSelf(4, add) // 8
applyToSelf(3) { a, b -> a * b } // 9

// for Single Abstract Method (SAM) interface
button.setOnClickListener { view -> ... }
```

## Delegates

```kotlin
class DraggableButton(
  clickListener: ClickListener,
  dragListener: DragListener
) : ClickListener by clickListener, DragListener by dragListener

val lazyUser: User by lazy { getCurrentUser() }
```

## Démo

![bg right:30% 80%](../assets/kotlin.png)

[Kotlin Playground](https://play.kotlinlang.org)

## Swift

![bg right:30% 80%](../assets/swift.png)

Très similaire:

- Typage statique inféré
- Optionals
- Closure
- Extensions
- <https://nilhcem.com/swift-is-like-kotlin/>

Pas de smart cast:

```swift
let user: User? = getCurrentUser()
if let user = user {
  // user is not null
}
```

Nuances: Structs, Automatic Reference Counting, `weak`...
