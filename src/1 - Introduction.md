---
marp: true
---

<!-- headingDivider: 2 -->

# Introduction au Développement Mobile

# Présentation

Cyril Findeling 👋

## Développement mobile

- technos moderne
- performances limitées
- livraisons itératives
- domaine compétitif

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
// valeur primitive donnée à la compilation qui ne peut pas changer
const val APP_ID = 42424242

// valeur donnée à l'execution qui ne peut pas changer ensuite
val user = User("alice")
user = User("bob") // ❌ ne compile pas

// valeur qui peut changer
var myMutableVariable = 0
myMutableVariable = 1
```

## Nullabilité

```kotlin
val user: User? = getCurrentUser()

// soft unwrap: exécute ou retourne null si l'instance est null
user?.name

// force unwrap: exécute OU crash si l'instance est nulle
user!!.toString()

// elvis operator: exécute la partie à droite si la partie à gauche est null
user?.name ?: "no user"
```

⚠️ `@Nullable` pour l'interopérabilité avec Java

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
// declaration and primary constructor
class Student(
  login: String, // constructor argument
  public val subjects: List<Subject> = emptyList(), // public property
) : User(login) { // parent constructor

    private val email: String // private property

    constructor(firstname: String, lastname: String) : this("$firstname_$lastname") // secondary constructor

    init { // additional constructor logic
      email = "$login@school.com"
    }
}

// classes are final by default: `open` allows inheritage
open class User(val login: String) {}
```

## Object

Permet de créer facilement un Singleton

```kotlin
object Analytics {
  fun trackLoginEvent() { ... }
}

// remplace le `static class` Java:
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

## Sealed class

Classes ayant un nombre de sous classes défini et limité

```kotlin
sealed class Result {

  class Success(val value: Any) : Result()

  class Failure(val error: Error) : Result()
}

// utile avec les smart cast
when (result) {
  is Result.Success -> display(result.value)
  is Result.Failure -> log(result.error)
}
```

## Extension functions

```kotlin
fun String.capitalize(): String {
  this.chars().mapIndexed { char, index ->
    if (index == 0) char.toUpperCase() else char
  }
}

"hello".capitalize() // ➡️ "Hello"
```

## Delegates

```kotlin
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
add(1, 2) // ➡️ 3

fun applyToSelf(number: Int, operation: (Int, Int) -> Int) {
    operation(number, number)
 }

applyToSelf(4, add) // 8
applyToSelf(3) { a, b -> a - b } // 0

// for Single Abstract Method (SAM) interface
button.setOnClickListener { view -> ... }
```

# Android

![bg right:70% 100%](../assets/jetpack.svg)

## Intro

![bg left:30% 50%](../assets/android.png)

- Nombreux utilisateurs
- Devices très différents
- Versions d’OS anciennes
- Play Store
- Puissance limitée
- Phone, Tablet, TV, Watch, Auto, Chrome, Windows, ...
- Dev natif en Kotlin et Java

## Android Studio

![bg left:30% 100%](../assets/android_studio.svg)

- IDE dédié développé par Jetbrains (IntelliJ)
- Navigation projet
- Terminal
- Logcat
- Émulateurs
- SDK Manager
- strings.xml
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
- App Store
- Swift (interop Objective-C)
- XCode 💩
- Simulator

# Cross-Platform

![bg left:30% 90%](../assets/react.png)
![bg left:30% 70%](../assets/flutter.svg)

- Permet de coder une seule fois
- Souvent à base de "Components" (à la React)
- Désavantage: performances, UX, possibilités spécifiques ou récentes des OS
- Xamarin, ReactNative, NativeScript, Ionic, ...
- Dart: Flutter (iOS, Android, Desktop, Web) par Google

# Composants

![bg left:30% 90%](../assets/compose.png)
![bg left:30% 75%](../assets/swiftui.png)

- Swift: SwiftUI par Apple
- Kotlin: Jetpack Compose sur Android, Desktop, Web et même iOS par JetBrains et Google
