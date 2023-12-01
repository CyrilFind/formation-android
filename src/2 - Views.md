---
marp: true
---

<!-- headingDivider: 2 -->

# Views Framework

![bg right:65% 100%](../assets/jetpack.svg)

## Activity

![bg left:25% 85%](../assets/bottomnav.png)

- Contrôle une "page" qui prends généralement tout l’écran
- Son rôle est de créer, afficher, manipuler les `View` pour permettre à l'utilisateur d'interagir
- Obéit à un "Lifecycle"
- Peut contenir des `Fragment` (ex: youtube mini player fragment)
- Souvent une "Single Activity" dans laquelle on navigue en intervertissant des `Fragment`
- ⚠️ Éviter la tendance à mettre trop de logique dans l'Activity

## Context

Objet très présent sur Android:

- Fourni par le système
- Interface aux infos globales sur l'environnement de l'application
- Accède aux resources et aux classes spécifiques à l'application
- Permet de lancer des `Activity`
- Diffuse et reçoit des `Intents`
- `Activity` hérite de `Context` donc peut faire tout ça également

## Layouts

Fichier XML décrivant un écran (ou une partie)

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
  xmlns:android="http://schemas.android.com/apk/res/android"
  xmlns:app="http://schemas.android.com/apk/res-auto" >
    <androidx.cardview.widget.CardView >
        <TextView ... />
        <ImageView ... />
        <EditText ... />
        <Button ... />
    </androidx.cardview.widget.CardView>
</androidx.constraintlayout.widget.ConstraintLayout>
```

## Views

Élément graphique de l’interface: Text, Image, Button, ...

```xml
<TextView
  android:id="@+id/textView_login" // reference to the view
  android:layout_width="match_parent" // use all available width in parent
  android:layout_height="wrap_content" // use only needed height
/>

<ImageView
  android:id="@+id/imageView_login"
  android:src="@drawable/ic_login"
  android:layout_width="0dp" // match width to constraints
  android:layout_height="200dp" // specify explicit height
  app:layout_constraintEnd_toEndOf="@id/textView_login" // constraint start
  app:layout_constraintStart_toStartOf="parent" // contraint end
  android:visibility="invisible" // visible, invisible or gone
/>
```

## ViewGroups

View contenant d’autres Views, avec diverses règles d’affichage:

![w:900](../assets/layouts.png)

## Inflating Layout in Activity

```kotlin
class MainActivity : AppCompatActivity() {
   override fun onCreate(savedInstanceState: Bundle?) {
       super.onCreate(savedInstanceState)
       setContentView(R.layout.activity_main) // inflate
//    access resources^ ^layouts   ^layout file name
}

class MainFragment : Fragment() {
  override fun onCreateView(...): View {
    return inflater.inflate(R.layout.fragment_main, container, false)
  }
}

```

## References to views

```kotlin
val loginTextView: TextView = findViewById(R.id.textView_login)
val loginImageView = findViewById<ImageView>(R.id.imageView_login)
```

Problèmes:

- Pas type safe
- Pas null-safe
- Tous les ids de tous les layouts sont disponibles
- Verbeux

## ViewBinding

Dans `app/build.gradle`:

```gradle
android {
    buildFeatures {
        viewBinding true
    }
}
```

Usage:

```kotlin
// Dans `onCreate` ou `onCreateView`:
val binding = ActivityMainBinding.inflate(layoutInflater)
val rootView = binding.root

// toutes les vues avec des ids sont accessibles
binding.textView.text = "hello world!"
binding.imageView.setOnCLickListener { ... }
```

[Documentation](https://developer.android.com/topic/libraries/view-binding#fragments)

## Declare main activity in manifest

```xml
// MainActivity needs to include intent-filter to start from launcher
<activity
      android:name=".MainActivity"
      android:label="@string/app_name"
      android:theme="@style/AppTheme.NoActionBar">
  <intent-filter>
      <action android:name="android.intent.action.MAIN"/>
      <category android:name="android.intent.category.LAUNCHER"/>
  </intent-filter>
</activity>
```

# Lifecycle

![bg right:70% 100%](../assets/jetpack.svg)

## Activity lifecycle

![bg right](../assets/activity_lifecycle.png)

## Fragment lifecycle

![bg right](../assets/fragment_lifecycle.png)

## Configuration Changes

![bg right:40% 80%](../assets/rotation.png)

- Rotation
- Changement de langage
- Mode multi-fenêtre

Android garde seulement :

- L’intent éventuellement utilisé
- L’état des vues ayant un ID (ex: RecyclerView scroll position)

## InstanceState

```kotlin
override fun onSaveInstanceState(outState: Bundle) {
   super.onSaveInstanceState(outState)
   outState.putString("key", count_text_view.text.toString())
}

override fun onCreate(savedInstanceState: Bundle?) {
   super.onCreate(savedInstanceState)
   setContentView(R.layout.activity_main)
   savedInstanceState?.getString("key").let { count ->
       count_text_view.setText(count)
   }
}
```

- Préserve les données de l’Activity
- Configuré manuellement
- Perdu si on quitte l’Activity
- Plus persistent: DB, Web, SharedPreference, DataStore

# iOS

![bg right:30% 80%](../assets/xcode.png)

- UIViewController (Équivalent de Activity)
- Storyboards (Layout XML manipulé visuellement)
- Xibs (Vue XML)

```swift
class LoginViewController: UIViewController {
    @IBOutlet weak var label: UILabel!
    @IBAction func setDefaultLabelText(_ sender: UIButton) {
        let defaultText = "Default Text"
        label.text = defaultText
    }
}
```

## UIViewController

![bg right:40% 90%](../assets/ios_lifecycle.png)

- Layout:
  - StoryBoard
  - Nib (`init(nibName:bundle:)`)
  - `loadView`, `viewDidLoad`, ...
- rotation: `viewWillTransition`
- state restauration: `restorationIdentifiers` on VC and Views
