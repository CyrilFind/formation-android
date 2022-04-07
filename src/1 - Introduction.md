---
marp: true
---
<!-- headingDivider: 2 -->

# Introduction au Dévelopment Mobile

## Kotlin

![bg left:30% 50%](../assets/kotlin.png)

- Moderne
- Concis
- Java Interop
- Développé par JetBrains
- Kotlin everywhere: JVM, Backend, JS, KTS, iOS...

## Typage statique inféré

```kotlin
val myInt: Int = 1
val myInt = 1

val myString: String = "coucou"
val myString = "coucou"

val myUser: User = User()
val myUser = User()
```

## Mutabilité

```kotlin
// valeur donnée à la compilation qui ne peut pas changer:
const val MY_CONSTANT = 42 

// valeur donnée à l'execution qui ne peut pas changer ensuite:
val myImmutableVariable = MY_CONSTANT + 8

// valeur qui peut changer:
var myMutableVariable = 0 
myMutableVariable = 1
```

## Nullabilité

```kotlin
val user: User? = getCurrentUser()

// soft unwrap: exécute ou retourne null si l'instance est null
user?.name // soft unwrap
    
// force unwrap: exécute OU crash si l'instance est nulle:
user!!.toString()

// elvis operator: éxécute la partie à droite si la partie à gauche est null:
user?.name ?: "no user" // coalesce operator
```

⚠️ Pour l'interopérabilité avec Java il faut une annotation `@Nullable`

## Smart casts

```kotlin
var user: User?

user?.connect()

if (nullable != null) { nullable.connect() }
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

## Functions

```kotlin
fun functionName(
  firstArgumentName: FirstArgumentType, 
  secondArgumentName: SecondArgumentType
) : ReturnType {
  val result: ReturnType
  // ...
  return result
}

// short syntax: le 
fun add(first: Int, second: Int) = first + second
```

## Classes

```kotlin
// classes are final by default
class Student( // declaration and constructor 
  name: String, // constructor argument
  public val subjects: List<Subject>, // public property
) : User(name) { // parent constructor
    private val secret = "something hidden" // private property

    init { ... }
} 

// open makes them non-final
open class User(val name: String) {} 
```

## Object

Permet de créer facilement un Singleton

``` kotlin
object Analytics { 
  fun trackLoginEvent() { ... }
}

// à utiliser comme une classe `static` Java:
Analytics.trackLoginEvent() 
```

## Companion object

Permet d'avoir l'équivalent des membres `static` en Java:

``` kotlin
class Math {

  companion object {
    const val PI = 3.14159265359
  }
}

Math.PI // interop java: MyClass.Companion.MY_CONSTANT
```

## Data class

`equals(), toString(), hashCode(), copy()` et destructuration sans rien coder !

``` kotlin
data class Point(val x: Float, val y: Float)

val pointA = Point(1.0f, 2.0f)

val (x, y) = pointA

val pointB = pointA.copy(y = 1.0f)

pointB.toString() // Point(x=1.0f, y=1.0f)

val pointC = Point(1.0f, 2.0f)
pointA == pointC // ➡️ true
```

## Sealed class

Classes ayant un nombre de sous classes défini et limité

``` kotlin
sealed class Result {
  
  class Success(val value: Any) : Result()
  
  class Failure(val error: Error) : Result()
}
```

➡️ Permet d'être smart-casté

## Extension functions

``` kotlin
fun String.capitalize(): String { 
  this.chars().mapIndexed { char, index -> 
    if (index == 0) char.toUpperCase() else char 
  } 
}

"blabla".capitalize() // ➡️ "Blabla"
```

## Delegates

``` kotlin
class DraggableButton(
  clickListener: ClickListener, 
  dragListener: DragListener
) : ClickListener by clickListener, DragListener by dragListener

val lazyUser: User by lazy { getCurrentUser() }
```

## Lambdas

Blocs d'execution qui se manipulent en tant que variables:

```kotlin
val add: (Int, Int) -> Int = { a, b -> a + b }

val three = add(1, 2)

fun operation(number: Int, operation: (Int, Int) -> Int) {
    operation(number, number)
 }

operation(4, add) // 8
operation(3) { a, b -> a - b } // 0

// Lambda for SAM
button.setOnClickListener { view -> ... }
```

## Kotlin Koans

Petits exercices pour prendre en main le langage:

- Soit en ligne: [try.kotl.in/koans](http://try.kotl.in/koans)

- Soit dans l'IDE (pour avoir l'autocompletion), :
  - installer le plugin Edutools: `Plugins > Marketplace > Edutools > Install`
  - accepter de redémarrer
  - Démarrer le cours: `My Courses > Start New Course > Marketplace > Kotlin Koans > Start`

# Android

![bg right:70% 100%](../assets/jetpack.svg)

## Intro

![bg left:30% 50%](../assets/android.png)

- Nombreux utilisateurs
- Devices très différents
- Versions d’OS anciennes
- Puissance limitée
- Phone, Tablet, TV, Watch, Auto, Chrome OS, Fuschia OS
- Dev natif en Kotlin et Java

## Android Studio

![bg left:30% 100%](../assets/android_studio.svg)

- IDE dédié développé par Jetbrains (IntelliJ)
- Navigation projet
- Terminal
- Logcat
- Émulateurs
- SDK Manager
- Refactoring
- RAM 🔥

## Éléments d'une app Android

![bg left:30% 50%](../assets/android.png)

- Scripts Gradle
- AndroidManifest.xml
- App
- Activity
- Fragment
- Layouts XML

## App Components

![bg left:30% 160%](../assets/app_components.png)

- Activity / Fragments ➡ Screen Controller
- Service ➡ Headless Controller
- Broadcast Receiver ➡ Event Listener
- ContentProvider ➡ Shared Data API

# iOS

![bg left:30% 80%](../assets/xcode.png)

- Beaucoup d'utilisateurs aux US
- Plus de 💰 dépensés
- Moins de devices différents
- OS mis à jour plus rapidement
- Swift (interop Objective-C)
- XCode 💩

# Cross-Platform et Composants

![bg left:30% 80%](../assets/compose.svg)

- Permet de coder une seule fois
- Souvent à base de "Components" (à la React)
- Désavantage: performances, UX, possibilités spécifiques ou récentes des OS
- Xamarin, ReactNative, NativeScript, Ionic, ...
- Dart: Flutter (iOS, Android, Desktop, Web) par Google
- Swift: SwiftUI (iOS only) par Apple
- Kotlin: Jetpack Compose sur Android, Desktop, Web et même iOS (non-officiel) par JetBrains et Google
