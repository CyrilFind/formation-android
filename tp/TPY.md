# TP 6: SignUp/Login et Navigation

## Ajout des dépendances

Dans le fichier `app/build.gradle`, ajouter si elle n'y sont pas les dépendances suivantes:

```groovy
  implementation 'androidx.core:core-ktx:1.8.0-alpha02'
  implementation 'androidx.navigation:navigation-fragment-ktx:2.4.0-rc01'
  implementation 'androidx.navigation:navigation-ui-ktx:2.4.0-rc01'
```

## Nouveaux Fragments

Créer 3 nouveaux fragments et leurs layouts (manuellement ou avec l'IDE):

- `AuthenticationFragment`
  - 2 buttons: "Log In" et "Sign Up"
- `LoginFragment`
  - 2 `EditText`, un pour l'email, le second pour le password
  - un bouton "Log In"
  - L'attribut `android:hint` permet d'ajouter des placeholders
  - L'attribut `android:inputType` permet de gérer le type d'input (password par exemple)
- `SignupFragment`
  - Plusieurs `EditText`: `firstname, lastname, email, password, password_confirmation`
  - Un bouton "Sign Up"

## Nouvelle Activity

- Créer une nouvelle Activity : `AuthenticationActivity`
- Ajoutez la dans l'`AndroidManifest` et déclarez la comme étant le point d'entrée de votre application (ce n'est plus `MainActivity` pour l'instant)
- Remplacez le layout associé:

```xml
<?xml version="1.0" encoding="utf-8"?>
<fragment
    android:id="@+id/nav_host_fragment"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:name="androidx.navigation.fragment.NavHostFragment"
    app:defaultNavHost="true"
    app:navGraph="@navigation/nav_graph" />
```

Créer `res/navigation/nav_graph.xml` qui n'existe pas encore (manuellement ou en suivant la suggestion de l'IDE): c'est un graphe de navigation qui servira à définir les fragments à insérer dans cette balise.

## Navigation

- Ajouter les 3 fragments créés précédemment dans le graphe de navigation
- Définissez `AuthenticationFragment` comme `Start Destination` (avec l'icône maison 🏠)
- Définissez ensuite les enchaînements entre les fragments: l'`AuthenticationFragment` permet d'ouvrir les 2 autres
- Passez en mode `Text`, vous devriez remarquer 2 actions dans l'`AuthenticationFragment`: elles vont permettre la navigation dans le code grace au `NavController` avec cette syntaxe:

```kotlin
findNavController().navigate(R.id.action_authenticationFragment_to_loginFragment)
```

- Dans `AuthenticationFragment`, faites en sorte naviguer ainsi en cliquant sur chaque bouton
- À présent, vous pouvez naviguer entre les fragments 🎊

## Login

- Créer la `data class LoginForm` qui contient un email et un password de type `String`
- Créer la `data class LoginResponse` qui contient un token de type `String`
- Ajouter un nouveau call réseau dans `UserWebService`:

  ```kotlin
  @POST("users/login")
  suspend fun login(@Body user: LoginForm): Response<LoginResponse>
  ```

- Dans `LoginFragment` cliquer sur "Log in", doit:

  - Vérifier que les champs sont remplis
  - Créer une instance de `LoginForm`
  - Envoyer le formulaire au serveur via la fonction `login` de `UserService`

  - En cas d'erreur, afficher un toast d'explication:

  ```kotlin
  Toast.makeText(context, "Erreur de connexion", Toast.LENGTH_LONG).show()
  ```

  - Si le call se passe bien, ajouter le token renvoyé dans les `SharedPreference`:

  ```kotlin
  const val SHARED_PREF_TOKEN_KEY = "auth_token_key"
  // ...
  PreferenceManager.getDefaultSharedPreferences(context).edit {
      putString(SHARED_PREF_TOKEN_KEY, fetchedToken)
  }
  ```

  - puis naviguer vers la liste de tâches

## Refacto de l'API

Le but est de remplacer le `TOKEN` en dur par celui stocké et le récupéré depuis les `SharedPreference`

Une bonne pratique serait ici l'[injection de dépendance](https://en.wikipedia.org/wiki/Dependency_injection) mais pour faire simple nous allons ajouter à `Api` un `Context` initialisé au lancement de l'app (nécessaire pour utiliser `SharedPreference`):

```kotlin
object Api {
  // ...

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
  <!-- ... -->
/>
```

- Dans `Api`, utilisez `by lazy {}` pour `retrofit` et supprimez `TOKEN` pour utiliser le token stocké:

```kotlin
fun getToken() = PreferenceManager.getDefaultSharedPreferences(appContext).getString(SHARED_PREF_TOKEN_KEY, "")
```

- Tout devrait fonctionner ! 🙌

## Sign Up

Faire comme pour le login mais avec une `data class SignUpForm` qui contient: `firstname, lastname, email, password, password_confirmation` afin de permettre de créer un compte.

## Déconnexion

Ajouter un bouton pour se déconnecter qui efface le token dans les `SharedPreference` et renvoie au début de l'Authentification

## Redirection

En réalité, utiliser `AuthenticationActivity` comme point de départ n'est pas une bonne pratique car lorsque le user relance son application, il faut lui afficher directement la liste des tâches:

- remettez donc `MainActivity` comme activité principale le Manifest
- naviguez tout de suite vers l'authentification si il n'y a pas de token sauvegardé
- fermez l'authentification quand le token est sauvegardé

## Ajout et Édition

Suivez les mêmes étapes pour remplacer la navigation des TDs précédents avec des `Intent` explicites par cette nouvelle navigation:

- Remplacez le `FragmentContainerView` dans `MainActivity` par celui de `AuthenticationActivity` et supprimez `AuthenticationActivity`
- Ajoutez `TaskListFragment` au graphe de navigation
- Transformez `DetailActivity` en `FormFragment` en adaptant les `override` et ajoutez le au graphe
- Faites pareil pour `UserInfoActivity`
- Pour communiquer entre Fragments vous pouvez utiliser les `savedStateHandle` ([exemple](https://stackoverflow.com/a/62320979/3466492))
