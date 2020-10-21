# TD 1 - Introduction à Android

## Avant de commencer

Prendre en main l'IDE: vous pouvez aller dans les paramètres (`Cmd + ,` ou  `Android Studio > Preferences`) et les adapter à vos habitudes (Font, thème, coloration syntaxique, raccourcis clavier,plugins)
Je vous conseille en particulier de:

- Changer le raccourci pour les commentaires car sur AZERTY celui par défaut ne fonctionne pas (mettez `Cmd + :`)
- Changer la coloration syntaxique qui n'est par défaut pas terrible pour Kotlin: vous pouvez installer un plugin (ex: "Rainglow Color Schemes") et choisir parmi les divers proposés ou importer mon thème [Darculai](./Darculai_cyrilfind.icls)
- Ajouter des plugins comme RainbowBrackets, Codota, grep console, SonarLint (et regardez les plus téléchargés dans l'onglet MarketPlace)
- Activer les imports automatiques: `Editor > General > Auto Import > Kotlin > cocher "Add unambiguous import on the fly" et "Optimize imports on the fly..."`
- Ne pas prendre la toute dernière version d'Android pour l'émulateur (ça évitera des erreurs et pèsera moins sur votre disque dur)
- Activer les "type hints" afin de voir les types des variables que Kotlin "devine"

## Kotlin Koans

Suivre les exercices des [Kotlin Koans](https://try.kotlinlang.org) dans Android Studio (en ajoutant le plugin "Edutools" puis `File > Learn and Teach > Browse Courses > Kotlin Koans`) ou sur le site [try.kotl.in](https://try.kotl.in) (mais vous n'aurez pas l'auto-complétion)

## Google Codelabs

Faire les tutos de la collection
[Android Kotlin Fundamentals](https://codelabs.developers.google.com/android-kotlin-fundamentals/) à partir de 02.1 (vous pouvez survoler rapidement ceux d'avant) et

⚠️ Attention:

- Ne restez pas bloqués sur les pages "Introduction", "Overview", ce sont juste des résumés de ce que vous allez faire.
- Parfois l'IDE bug en mode `Visuel` et n'affiche pas certains attributs dans le layout editor (typiquement textAlignment, fontFamily,...) dans ce cas, rien de grave, passez juste en mode `Text`
- Parfois les attributs avec start/end ne s'affiche pas: idem rien de grave vous pouvez utiliser left/right (ex: marginLeft au lieu de marginRight)
