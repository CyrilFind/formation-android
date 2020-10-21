# TD 7: SignUp/Login et Navigation

## Ajout des dépendances

Dans le fichier `app/build.gradle`, ajouter :

```groovy
implementation "androidx.core:core-ktx:1.1.0"
implementation "androidx.navigation:navigation-fragment-ktx:2.1.0"
implementation "androidx.navigation:navigation-ui-ktx:2.1.0"
```

## Nouvelle Activity

- Créer une nouvelle Activity : `AuthenticationActivity`
- Ajoutez la dans l'`AndroidManifest` et déclarez la comme étant le point d'entrée de votre application (ce n'est plus MainActivity)
- Remplacez le layout associé par un `<fragment...>` de type `NavHostFragment`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<fragment
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/nav_host_fragment"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:name="androidx.navigation.fragment.NavHostFragment"
    app:defaultNavHost="true"
    app:navGraph="@navigation/nav_graph" />
```

À partir du graphe de navigation (`app:navGraph="@navigation/nav_graph"`), le `NavHostFragment` va gérer la navigation en remplaçant le fragment à chaque changement d'écran.

Vous pouvez utiliser `Alt + Enter` pour créer ce fichier de navigation, nous y reviendrons plus tard.

## Nouveaux Fragments

Créer 3 nouveaux fragments et leur layout:

- `AuthenticationFragment`
  - contient 2 buttons "Log in" et "Sign Up"
- `LoginFragment`
  - Contient 2 `EditText`, un pour l'email, le second pour le password et un bouton "Login"
  - L'attribut `android:hint` permet d'ajouter des placeholders
  - L'attribut `android:inputType` permet de gerer le type d'input (password par exemple)
- `SignupFragment`
  - Plusieurs `EditText`: `firstname, lastname, email, password, password_confirmation`
  - Un bouton "Sign Up"

## Navigation

- Si le fichier `navigation/nav_graph.xml` n'existe pas créez le dans le dossier `res`
- Ajouter les 3 fragments précédents
- Définissez `AuthenticationFragment` comme `Start Destination` (avec l'icône maison 🏠)
- Définissez ensuite les enchainements entre les fragments: l'`AuthenticationFragment` permet d'ouvrir les 2 autres
- Passez en mode `Text`, vous devriez remarquer 2 actions dans l'`AuthenticationFragment`: elles vont permettre la navigation dans le code  grace au `NavController` avec cette syntaxe:

```kotlin
findNavController().navigate(R.id.action_authenticationFragment_to_loginFragment)
```

- Dans `AuthenticationFragment`, ajoutez des clickListener sur les 2 boutons "Log in" et "Sign Up" qui vont executer ces navigations
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
  - Si le call se passe bien, ajouter le token renvoyé dans les `SharedPreference` (cf plus bas) et affichez les taches de l'utilisateur
  - Sinon, afficher un toast pour expliquer l'erreur:

```kotlin
Toast.makeText(context, "text", Toast.LENGTH_LONG).show()
```

### SharedPreference

- Créer un fichier `Constants.kt` qui va contenir les constantes utilisés par les `SharedPreference`:

```kotlin
const val SHARED_PREF_TOKEN_KEY = "auth_token_key"
```

- Pour stocker le token, la syntaxe est simplifiée gràce à `core-ktx`:
(Normalement il faudrait commencer par un `.edit()` et finir par un `.apply()`)

```kotlin
PreferenceManager.getDefaultSharedPreferences(context).edit {
    putString(SHARED_PREF_TOKEN_KEY, fetchedToken)
}
```

## Refacto de l'API

Le but est de remplacer le `TOKEN` en dur par celui stocké et le récupéré depuis les `SharedPreference`

Une bonne pratique serait ici l'injection de dépendance (avec Dagger2) mais pour faire simple nous allons transformer `Api` en singleton et l'initialiser au lancement de l'app en lui passant le `Context` nécessaire pour utiliser les `SharedPreference`:

```kotlin
class Api(private val context: Context) {
    companion object {
        private const val BASE_URL = "https://android-tasks-api.herokuapp.com/api/"
        private const val TOKEN = "votre token"
        lateinit var INSTANCE: Api
    }
    // le reste ne change pas
}
```

- Créer une classe `App`

```kotlin
class App: Application() {
    override fun onCreate() {
        super.onCreate()
        Api.INSTANCE = Api(this)
    }
}
```

- Dans l'`AndroidManifest`, ajoutez l'attribut name avec votre classe `App`:

```xml
    <application
        android:name=".path.to.App"
        .../>
```

- Partout ailleurs remplacer `Api` par `Api.INSTANCE`
- Dans l'api, remplacer la `const TOKEN` par une fonction qui récupere celui qui est stocké:

```kotlin
PreferenceManager.getDefaultSharedPreferences(context).getString(SHARED_PREF_TOKEN_KEY, "")
```

- Utilisez cette fonction dans l'`interceptor` de votre `okHttpClient`

```kotlin
"Authorization", "Bearer ${getToken()}"
```

- Tout devrait fonctionner ! 🙌

## SignUp

Faire comme pour le login mais avec une `data class SignUpForm` qui contient: `firstname, lastname, email, password, password_confirmation`

## Un petit coup de polish

### Redirection

Lorsque le user relance son application, il faut lui afficher directement la liste des tâches: vérifier dans l'`AuthenticationFragment` si un token existe

- [Documentation](https://developer.android.com/guide/navigation/navigation-conditional)

### Déconnexion

Ajouter un bouton pour se déconnecter qui efface le token dans les `SharedPreference` et renvoie au début de l'Authentification

### Ajout et Édition

Suivez les mêmes étapes pour remplacer la navigation des TDs précédents avec des `Intent` explicites par cette nouvelle navigation:

- Changez le name du `<fragment>` dans `MainActivity` par un `NavHostFragment`
- Assignez lui un nouveau graphe de navigation (qui sera très simple): `main_nav_graph` (vous pouvez renommer l'ancien en `authentication_nav_graph`)
- Transformez `TaskActivity` en `TaskFragment` en adaptant les `override`
- Utilisez [SafeArgs](https://developer.android.com/guide/navigation/navigation-pass-data#Safe-args) pour passer les données d'une activité à l'autre
- Faites pareil pour `UserInfoActivity`
- Vous pouvez simplifier pas mal de choses en utilisant `by activityViewModels()` au lieu de `by viewModels()` afin de partager une l'instance de viewmodel au sein des Fragments d'une même Activity
