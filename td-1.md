# TD 1 - Introduction à Android

## Avant de commencer
Prendre en main l'IDE: vous pouvez aller dans les paramètres (<kbd>Cmd</kbd> + <kbd>, </kbd> ou  `Android Studio > Preferences`) et adapter à vos habitudes, par ex:
- La Font utilisée
- Le thème global
- La coloration syntaxique
- Les raccourcis clavier
- Les plugins

Je vous conseille en particulier de:
- Changer le raccourci pour les commentaires car sur AZERTY celui par défaut ne fonctionne pas (mettez <kbd>Cmd + :</kbd>)
- Changer la coloration syntaxique, car par défaut elle n'est pas terrible pour Kotlin: vous pouvez installer un plugin (ex: "Rainglow Color Schemes") et choisir parmis les divers proposés ou utiliser mon thème "Darculai" dispo sur ce repo (qui est juste le thème Darcula par défaut avec quelques ajouts)
- les plugins: RainbowBrackets, Codota, grep console, SonarLint, KeyPromoter (un peu relou mais permet d'apprendre les raccourcis), et plein d'autres (regardez les plus téléchargés dans l'onglet MarketPlace)

## Kotlin Koans

Suivre les exercices des [Kotlin Koans](https://try.kotlinlang.org) dans Android Studio (en ajoutant le plugin "Edutools" puis `File > Learn and Teach > Browse Courses > Kotlin Koans`) ou sur le site [try.kotl.in](https://try.kotl.in) (mais vous n'aurez pas la complétion)

## Google Codelabs
Faire les tutos de la collection
[Android Kotlin Fundamentals](https://codelabs.developers.google.com/android-kotlin-fundamentals/) (au moins de 02.1 à 02.4)

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
