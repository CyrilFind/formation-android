# TD 8: Améliorations

Voici des sujets d'amélioration, vous pouvez les faire dans l'ordre de votre choix.

Lisez bien la documentation avant de commencer chacun car il n'y a pas d'étapes pour vous guider.


## Deep linking

Ajouter la possibilité d'ouvrir l'application à partir de certaines URI:

- Ouvrir l'activité par défaut avec "https://android-tasks-api.herokuapp.com/"
- Ouvrir l'activité d'édition de la tache avec https://android-tasks-api.herokuapp.com/tasks/ID_DE_LA_TACHE

#### Documentation
- [Deep Link](https://developer.android.com/training/app-links/deep-linking)
- [Deep link Navigation](https://developer.android.com/guide/navigation/navigation-deep-link)


## PreferenceScreen

Ajouter un menu et une page "Settings" en utilisant un `PreferenceScreen`:

- Ajout un OptionsMenu menu pour y acceder
- Permettre de changer l'aspect de l'app:
    - la couleur de la police 
    - La couleur de l'`AppBar`
    - le titre dans l'`AppBar`
    - ...

#### Documentation
- [Menus](https://developer.android.com/guide/topics/ui/menus)
- [Settings](https://developer.android.com/guide/topics/ui/settings.html)


## Data-Binding

Utiliser le data-binding pour afficher et éditer les données de l'application directement dans les layouts:

- Commencer par les infos user affichées dans le fragment principal
- Faire de même dans `TaskViewHolder`
- Permettre d'éditer directement dans `TaskActivity`
    
#### Documentation 
- [Data Binding](https://developer.android.com/topic/libraries/data-binding) (affichage)
- [Two Way Data Binding](https://developer.android.com/topic/libraries/data-binding/two-way) (édition)


## Pagination

Utiliser une PagedList pour afficher une liste infinie de tâche de façon efficace à la place de la RecyclerView actuelle qui n'affiche que la première page retournée par le serveur.

Pour rappel, il y a 2 parametres dans l'API permettant de récuperer les tâches: `per_page` et `page`

#### Documentation 
- [Paging Library](https://developer.android.com/topic/libraries/architecture/paging)
- [Tasks API](https://android-tasks-api.herokuapp.com/api-docs/)


## Notifications et AlarmManager

Ajouter une fonctionnalité "Rappel" à vos tâches à l'aide de la date `due_date` stockée sur le serveur: 

- ajouter un `DatePicker` et un `TimePicker` ou bien un `DatePickerDialog` et `TimePickerDialog` pour éditer cette date
- Utiliser `AlarmManager` pour envoyer une notification 5 minutes avant la `due_date`
- Ajouter un `PendingIntent` qui ouvre `TaskActivity` avec le détail de la tâche
- Ajouter une action supplémentaire `Mark as Done` dans la notification qui supprime la `Task` directement

#### Documentation
- [Alarms](https://developer.android.com/training/scheduling/alarms)
- [Pickers](https://developer.android.com/guide/topics/ui/controls/pickers)
- [PickerDialog](https://www.journaldev.com/9976/android-date-time-picker-dialog)
- [Notifications](https://developer.android.com/guide/topics/ui/notifiers/notifications)
- [Notifications Codelab](https://codelabs.developers.google.com/codelabs/advanced-android-kotlin-training-notifications/index.html?index=..%2F..advanced-android-kotlin-training#0)


## Work Manager

Implémenter des `Worker` pour executer des tâches de fond sur les images et utiliser `WorkManager` pour les exécuter de façon efficace et avec les contraintes nécessaires (ex: réseau disponible):

- Commencer par la compression et l'upload de l'image 
- Ajouter un Worker appliquant un filtre sépia
- Afficher dans l'app ou dans une notification l'état de progrès du travail
  
#### Documentation
- [WorkManager: Getting Started](https://developer.android.com/topic/libraries/architecture/workmanager/basics.html)
- [CoroutineWorker](https://developer.android.com/topic/libraries/architecture/workmanager/advanced/coroutineworker)
- [Tuto RayWanderlitch](https://www.raywenderlich.com/6040-workmanager-tutorial-for-android-getting-started)
- [Article ProAndroidDev](https://proandroiddev.com/exploring-the-stable-android-jetpack-workmanager-82819d5d7c34)


## Room

Implémenter un cache des données serveur avec `Room`:

- Gestion offline des informations de l'utilisateur
- Gestion offline des tâches: liste, ajout, edition, supression

#### Documentation
- [Codelab "Room with a view"](https://codelabs.developers.google.com/codelabs/android-room-with-a-view-kotlin) (sur Room de façon générale)
- [Codelab "Repository"](https://codelabs.developers.google.com/codelabs/kotlin-android-training-repository) (sur la mise en place d'un Cache avec Room)


## Testing and dependency Injection

- Créer des tests unitaires 
- Créer des tests UI avec Espresso sur les différentes features de l'applications:
  - Affichage de la liste des tâches
  - Résultat des actions sur les boutons: ajout, suppression, ...
  - Mocker les appels réseaux

#### Documentation
- [Testing Codelab](https://codelabs.developers.google.com/codelabs/advanced-android-kotlin-training-testing-basics/) (5.1 à 5.3)
- [Mockito](https://site.mockito.org/)
- [Espresso](https://developer.android.com/training/testing/ui-testing/espresso-testing)


