# Sujets Exploratoires

## But

Sujets à implémenter de façon autonome:

- Lisez bien la documentation avant de commencer et/ou suivez les codelabs en adaptant à votre projet car il n'y a pas d'étapes pour vous guider.
- En revanche n'hésitez pas à poser des questions !
- Faites cette partie sur une branche à part de votre rendu principal
- Le but est d'aller le plus loin possible mais c'est normal si vous ne terminez pas certains sujets

**But:** Expliquer à vos camarades comment implémenter votre sujet et les avantages/inconvénients, les difficultés/les raccourcis que vous avez trouvés

**Barème** approximatif sur 10: 3pts sur l'avancée + 7pts sur la présentation

**Forme:** démo très rapide et présentation sous forme de "retour d'expérience" avec du code et des slides

**Temps:** en ~10 min

## 1 - Clean Archi et Injection de dépendance

Utilisez `Koin` pour faire de la "Dependency Injection" afin de s'approcher d'une "Clean Archi":

- Commencer par exposer les éléments de la classe `Api`
- Injectez les `WebService` dans les `Repository`
- Injectez les `Repository` dans les `ViewModels`
- Présentez les `Repository` à travers des `interface`
- refactorisez pour placer des `UseCase` ou `Interactor` entre les `ViewModel` et les `Repository`

**Documentation:**

- [Koin](https://github.com/InsertKoinIO/koin)
- [Clean Archi (Uncle bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Archi on Android](https://fernandocejas.com/2018/05/07/architecting-android-reloaded)
- [Projet boilerplate d'exemple](https://github.com/bufferapp/clean-architecture-koin-boilerplate)

## 2 - Navigation

### Safe Args

- Utilisez `SafeArgs` pour passer les données d'une activité à l'autre (au lieu de `startActivityForResult`

### Deeplinks

Ajouter la possibilité d'ouvrir l'application à partir de certaines URI:

- Ouvrir l'activité par défaut avec "<https://android-tasks-api.herokuapp.com/">
- Ouvrir l'édition de tâche avec "<https://android-tasks-api.herokuapp.com/tasks/ID_DE_LA_TACHE">

**Documentation:**

- [SafeArgs](https://developer.android.com/guide/navigation/navigation-pass-data#Safe-args)
- [Deep Link](https://developer.android.com/training/app-links/deep-linking)
- [Deep link Navigation](https://developer.android.com/guide/navigation/navigation-deep-link)

## 3 - Preferences

### PreferenceScreen

Ajouter un menu et une page "Settings" en utilisant un `PreferenceScreen`:

- Ajout un OptionsMenu menu pour y acceder
- Permettre de changer l'aspect de l'app:
  - la couleur de la police ???
  - La couleur de l'`AppBar`
  - le titre dans l'`AppBar`

### Preference Data Store

Remplacez l'utilisation des `SharedPreferences` par la nouvelle lib officielle: "Preference Datastore"

**Documentation:**

- [Menus](https://developer.android.com/guide/topics/ui/menus)
- [Settings](https://developer.android.com/guide/topics/ui/settings.html)
- [Datastore documentation](https://developer.android.com/topic/libraries/architecture/datastore#preferences-datastore)
- [Datastore codelab](https://developer.android.com/codelabs/android-preferences-datastore#0)

## 4 - DataBinding

Utiliser le data-binding pour afficher et éditer les données de l'application directement dans les layouts XML:

- Commencer par les infos user affichées dans le fragment principal
- Faire de même dans `TaskViewHolder`
- Faire de même dans les autres écrans
- Dans les écrans comme ajout/édition, userinfo, login/signup, utilisez le "two-way databinding" afin de remonter les modifications de données effectuées par l'utilisateur
- utilisez un "custom binding adapter" pour passer la liste de tâches directement

**Documentation:**

- [DataBinding](https://developer.android.com/topic/libraries/data-binding) (affichage)
- [Two-Way DataBinding](https://developer.android.com/topic/libraries/data-binding/two-way) (édition)
- [DataBinding Adapter](https://developer.android.com/topic/libraries/data-binding/binding-adapters)

## 5 - Pagination

Utiliser la lib "Paging 3" pour afficher une liste infinie de tâche de façon efficace dans votre RecyclerView qui n'affiche pour l'instant que la première page retournée par le serveur.

Pour rappel, il y a 2 parametres dans l'API permettant de récuperer les tâches: `per_page` et `page`

comment refresh ??

**Documentation:**

- [Paging 3 Library](https://developer.android.com/topic/libraries/architecture/paging/v3-overview)
- [Tasks API](https://android-tasks-api.herokuapp.com/api-docs/)

## 6 - Notifications et AlarmManager

Ajouter une fonctionnalité "Rappel" à vos tâches à l'aide du champ date `due_date` stockée sur le serveur:

- ajouter un `DatePicker` et un `TimePicker` ou bien un `DatePickerDialog` et `TimePickerDialog` pour éditer cette date
- Utiliser `AlarmManager` pour envoyer une notification 5 minutes avant la `due_date`
- Ajouter un `PendingIntent` qui ouvre l'édition de la tâche concernée
- Ajouter une action supplémentaire `Mark as Done` dans la notification qui supprime la `Task` directement

**Aide:** Pour récupérer une date du serveur vous aurez besoin d'utiliser l'annotation `@Serializable(with = DateSerializer::class)` qui indique d'utiliser un serializer custom comme celui ci:

```kotlin
@Serializer(forClass = Date::class)
object DateSerializer : KSerializer<Date> {
    private val formatter = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS", Locale.US)

    override fun serialize(encoder: Encoder, value: Date) =
        encoder.encodeString(formatter.format(value))

    override fun deserialize(decoder: Decoder): Date =
        formatter.parse(decoder.decodeString())
}
```

**Documentation:**

- [Alarms](https://developer.android.com/training/scheduling/alarms)
- [Pickers](https://developer.android.com/guide/topics/ui/controls/pickers)
- [PickerDialog](https://www.journaldev.com/9976/android-date-time-picker-dialog)
- [Notifications](https://developer.android.com/guide/topics/ui/notifiers/notifications)
- [Notifications Codelab](https://codelabs.developers.google.com/codelabs/advanced-android-kotlin-training-notifications/index.html?index=..%2F..advanced-android-kotlin-training#0)

## 7 - Work Manager

Implémenter des `CoroutineWorker` pour executer des tâches de fond sur les images et utiliser `WorkManager` pour les exécuter de façon efficace et avec les contraintes nécessaires (ex: réseau disponible):

- Créer un Worker appliquant un filtre sépia (local)
- Créer un Worker pour compresser le fichier (local)
- Créer un Worker pour uploader l'image (réseau)
- Implémenter une "chaîne" de Worker pour compresser puis uploader
- Afficher dans l'app et/ou dans une notification l'état de progrès du travail
- Faire en sorte que l'upload reprenne quand le réseau est coupé / reconnecté

**Documentation:**

- [WorkManager: Getting Started](https://developer.android.com/topic/libraries/architecture/workmanager/basics.html)
- [CoroutineWorker](https://developer.android.com/topic/libraries/architecture/workmanager/advanced/coroutineworker)
- [Chaining](https://developer.android.com/topic/libraries/architecture/workmanager/how-to/chain-work)
- [Tuto RayWanderlitch](https://www.raywenderlich.com/6040-workmanager-tutorial-for-android-getting-started)
- [Article ProAndroidDev](https://proandroiddev.com/exploring-the-stable-android-jetpack-workmanager-82819d5d7c34)

## 8 - Room

Implémenter un cache des données serveur avec `Room`:

- Gestion offline des informations de l'utilisateur
- Gestion offline des tâches: liste, ajout, edition, suppression

**Documentation:**

- [Codelab "Room with a view"](https://codelabs.developers.google.com/codelabs/android-room-with-a-view-kotlin) (sur Room de façon générale)
- [Codelab "Repository"](https://codelabs.developers.google.com/codelabs/kotlin-android-training-repository) (sur la mise en place d'un Cache avec Room)

## 9 - Tests

- Créer des tests unitaires
- vérifiez votre "code coverage"
- Créer des tests UI avec Espresso sur les différentes features de l'applications:
  - Affichage de la liste des tâches
  - Résultat des actions sur les boutons: ajout, suppression, ...
  - Mocker les appels réseaux

<!--
style
sqdelight

-->

**Documentation:**

- [Testing Codelab](https://codelabs.developers.google.com/codelabs/advanced-android-kotlin-training-testing-basics/) (5.1 à 5.3)
- [Mockito](https://site.mockito.org/)
- [Espresso](https://developer.android.com/training/testing/ui-testing/espresso-testing)

## 10 - Jetpack Compose

Remplacer vos vues XML par du Kotlin:

- [Documentation](https://developer.android.com/jetpack/compose/documentation)
- [Listes](https://developer.android.com/jetpack/compose/lists)
- [Navigation](https://developer.android.com/jetpack/compose/navigation)
