---
marp: true
---
<!-- headingDivider: 2 -->
<!-- class: invert -->

# Lifecycle

## Context

- provided by the Android system
- Interface to global information about an application environment
- access to application-specific resources and classes
- launching activities
- broadcasting and receiving intents

## Activity

![bg left:30% 50%](assets/bottomnav.png)

- Représente en gros une "page"
- Généralement prends tout l’écran
- Gère l’interaction entre la vue et l’utilisateur
- Peut démarrer d’autres Activity dans la même app ou d’autres
- Obéit à un "Lifecycle"
- Les Activity peuvent être hiérarchisée dans le manifest (pour la navigation)
- Une Activity "inflate" un layout XML dans `onCreate`

## Inflating Layout in Activity

```kotlin
class MainActivity : AppCompatActivity() {
   override fun onCreate(savedInstanceState: Bundle?) {
       super.onCreate(savedInstanceState)
       setContentView(R.layout.activity_main)
//    access resources^ ^layouts   ^layout file name
}
```

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

# Lifecycle Components

## Activity lifecycle

![bg right](assets/activity_lifecycle.png)

## Fragment lifecycle

![bg right](assets/fragment_lifecycle.png)

## Configuration Changes

![bg right:40% 80%](assets/rotation.png)

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

## UIViewController

![bg right:40% 95%](assets/ios_lifecycle.png)

- Layout:
  - StoryBoard
  - Nib (`init(nibName:bundle:)`)
  - `loadView`, `viewDidLoad`, ...
- rotation: `viewWillTransition`
- state restauration:  `restorationIdentifiers` on VC and Views
