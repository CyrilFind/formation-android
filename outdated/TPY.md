# TP 6: Connection et persistance

## AuthenticationActivity

Créer une nouvelle Activity : `AuthenticationActivity` avec pour UI:

- Un titre, ex: "Connection"
- Un bouton "Connect with Todoist"

## OAuth

- Lire la [documentation de l'Authorization](https://developer.todoist.com/guides/#authorization): elle ne rentre pas beaucoup dans les détails car elle repose sur `OAuth`, un protocole assez répandu
- Vous aurez aussi besoin [d'enregistrer votre app à ce lien](https://developer.todoist.com/appconsole.html) afin de récupérer un `client ID`, un `client secret` et une redirect URL
- Dans notre cas il s'agit d'ouvrir une page web de connection à Todoist, d'intercepter l'url de redirection pour récupérer un code et de faire une requête avec pour enfin recevoir un token
- Vous pouvez gérer tout cela avec [AppAuth](https://github.com/openid/AppAuth-Android), une lib qui simplifie beaucoup la procédure.
<!-- https://github.com/okta/okta-mobile-kotlin ? -->
<!-- https://joebirch.co/android/oauth-on-android-with-custom-tabs/ ? -->
- En cas d'erreur, afficher un toast d'explication:

  ```kotlin
  Toast.makeText(context, "explication", Toast.LENGTH_LONG).show()
  ```

- Si tout se passe bien, ajouter le token renvoyé dans un [`Preference Datastore`](https://developer.android.com/topic/libraries/architecture/datastore#preferences-datastore)
- et enfin quittez cette activity

## API

Le but est de remplacer le `TOKEN` en dur par celui stocké et le récupéré depuis le Datastore

Une bonne pratique serait ici l'[injection de dépendance](https://en.wikipedia.org/wiki/Dependency_injection) avec [Koin](https://insert-koin.io/docs/setup/koin#android) ou [Hilt](https://developer.android.com/training/dependency-injection/hilt-android) mais pour faire simple nous allons ajouter à `Api` un `Context` initialisé au lancement de l'app (nécessaire pour utiliser Datastore):

```kotlin
object Api {
  lateinit var appContext: Context
  fun setUpContext(context: Context) {
      appContext = context
  }

}
```

- Créer une classe `App`:

```kotlin
class App: Application() {
    override fun onCreate() {
        super.onCreate()
        Api.setUpContext(this)
    }
}
```

- Dans `AndroidManifest`, on spécifie la classe à utiliser dorénavant:

```xml
<application
  android:name=".App"
/>
```

- Dans `Api`:

```kotlin
fun getToken() = runBlocking { appContext.dataStore.... }
```

<aside class="negative">

Ici on ne peut pas utiliser de coroutine donc on force l'attente du résultat avec `runBlocking`

</aside>

- Tout devrait fonctionner ! 🙌

## Déconnexion

Ajouter un bouton pour se déconnecter qui efface le token de la mémoire et ouvre vers la page de connexion

## Navigation

- Transformez vos activity en `Fragment`, sauf `MainActivity` qui leur servira d'hôte
- Utilisez le [navigation component](https://developer.android.com/guide/navigation/navigation-getting-started) pour passer d'un écran à l'autre
- Pour communiquer entre Fragments vous pouvez utiliser les `savedStateHandle` ([exemple](https://stackoverflow.com/a/62320979/3466492)) ou les [Safe Args](https://developer.android.com/guide/navigation/navigation-getting-started#ensure_type-safety_by_using_safe_args)
