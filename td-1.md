# TD 1 - Introduction à Android

## Kotlin Koans

Faire au moins la première série d'exercices des [Kotlin Koans](https://try.kotlinlang.org): [try.kotl.in](https://try.kotl.in) ou dans Android Studio (en ajoutant le plugin "Edutools" puis `File > Learn and Teach > Browse Courses > Kotlin Koans`)

## Google Codelabs
Faire les tutos de la collection (en particulier de 02.1 à 02.4):
[Android Kotlin Fundamentals](https://codelabs.developers.google.com/android-kotlin-fundamentals/) 

## En cas de problèmes de réseau
Ajouter les dépendances suivantes dans le `app/build.gradle` d'un projet (n'importe lequel) et compiler (pour les télécharger en avance)

```groovy
dependencies {
   // ...
   implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.3.2'
   implementation 'com.squareup.retrofit2:retrofit:2.6.1'
   implementation 'com.squareup.moshi:moshi:1.9.1'
   implementation 'androidx.recyclerview:recyclerview:1.0.0'
   implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.3.2'
    // ...
}
```
