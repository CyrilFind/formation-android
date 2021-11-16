---
marp: true
---
<!-- headingDivider: 2 -->
<!-- TODO: Deeplinks ? -->

# Intents

## Définition

![height:350px](../assets/intents.png)

Un objet contenant les infos nécessaires à démarrer une `Activity` (en général) ➡️ Conceptuellement proche d'un lien HTML

Sert aussi (plus rarement) à démarrer un `Service` ou à envoyer un `Broadcast`

Un intent peut être "lancé" par une application ou par le système

## Explicit / Implicit

![bg right 95%](../assets/intents_explicit_implicit.png)

```kotlin
val explicitIntent = Intent(context, MyActivity::class.java)

// implicit intents:
val urlIntent = Intent("http://www.google.com")
val callButtonIntent = Intent(ACTION_CALL_BUTTON)
val phoneIntent = Intent(ACTION_DIAL, "tel:8005551234")
val searchIntent = Intent(Intent.ACTION_WEB_SEARCH)
searchIntent.putExtra(SearchManager.QUERY, "cute cat pictures")

val createPdfIntent = Intent(ACTION_CREATE_DOCUMENT)
createPdfIntent.type = "application/pdf" // set MIME type
createPdfIntent.addCategory(CATEGORY_OPENABLE)

// use:
startActivity(intent)

// To use later (ex: in Notifications)
val pendingIntent = PendingIntent.getActivity(
    context, 
    REQUEST_CODE, 
    intent, 
    FLAG_UPDATE_CURRENT) // Parcelable
pendingIntent.send()
```

## Send / Receive data

```kotlin
// Preparing intent in FirstActivity
val intent = Intent(this, SecondActivity::class.java)

intent.data = Uri.parse("https://www.google.com") // Web URL
intent.data = Uri.fromFile(File("/file_path/file.jpg")) // File URI

intent.putExtra("level_key", 42)
intent.putExtra("food_key", arrayOf("Rice", "Beans", "Fruit"))

val bundle = Bundle() // Use bundle to prepare a lot of data
bundle.putFloat("percent_key", 55f)
intent.putExtras(bundle)

startActivity(intent)

// Receiving data in SecondActivity
val uri = intent.data
val level = intent.getIntExtra("level_key", 0) // default to 0
val food = intent.getStringArrayExtra("food_key")
val bundle = intent.extras
val percent = bundle.getFloat("percent_key")
```

## Intent Filters

```xml
<activity android:name="ShareActivity">
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <action android:name="android.intent.action.SEND_MULTIPLE"/>
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
        <data android:mimeType="image/*" />
        <data android:mimeType="video/*" />
    </intent-filter>
</activity>
<activity android:name="BrowserActivity">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="https" />
        <data android:host="developer.android.com" />
    </intent-filter>
    <intent-filter>
        <intent-filter> 
            <action android:name="android.intent.action.MAIN" />

            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
    </intent-filter>
</activity>
```

## Requesting

```kotlin
class FirstActivity : Activity() { // requesting Activity
    companion object {
        const val UNIQUE_REQUEST_CODE = 666 // ID of the request
    }

    override fun onCreate() {
        // ...
        val intent = Intent(this, SecondActivity::class.java) // explicit intent
        startActivityForResult(intent, UNIQUE_REQUEST_CODE) // launch request
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, intent: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == UNIQUE_REQUEST_CODE && resultCode == Activity.RESULT_OK) {
                val reply = intent!!.getStringExtra(SecondActivity.EXTRA_REPLY)
                // … do something with the data
            }
        }
    }
}

class SecondActivity : Activity() { // requested Activity
    companion object {
        const val EXTRA_REPLY = "reply_key" // use a key to put/get result data
    }

    override fun onCreate() {
        // ...
        intent.putExtra(EXTRA_REPLY, "Done !") // add result data to intent
        setResult(RESULT_OK, intent) // specify all went well and return the data
        finish() // close this activity
    }
}
```

## New API

```kotlin
// Asking for an image
val getContent = registerForActivityResult(GetContent()) { uri: Uri? -> // Handle the returned Uri }
// ...
getContent.launch("image/*")

// Asking for a result
val startForResult = registerForActivityResult(StartActivityForResult()) { result: ActivityResult ->
    if (result.resultCode == Activity.RESULT_OK) {
        val intent = result.data
        // Handle the Intent
    }
}
// ...
startForResult.launch(Intent(this, ResultProducingActivity::class.java))
```

Also:

- [Default ActivityResultContracts](https://developer.android.com/reference/androidx/activity/result/contract/ActivityResultContracts)
- [Creating a custom contract](https://developer.android.com/training/basics/intents/result#custom)

## Resolving intents

```kotlin
// Check if that intent can be handled !
if (intent.resolveActivity(packageManager) != null) {
   startActivity(intent) // if no result needed, otherwise: ↴
   startActivityForResult(intent, ACTIVITY_REQUEST_CREATE_FILE)
}
```

![height:300px](../assets/disambiguation.png)

## Using Chooser Intent / Sharesheet

![height:300px](../assets/app_chooser.png)

```kotlin
// using Chooser Intent / Sharesheet
val intent = Intent(Intent.ACTION_SEND)
val chooserIntent = Intent.createChooser(intent, "Chooser Title")
   startActivity(chooserIntent)
```

# Permissions

## Demander la permission

- Demandées “à la volée” depuis Android M
- Les permissions “dangereuses” doivent être demandées à chaque fois
- On recommande d’expliquer la raison avant (et après un refus)
- Ajouter dans le manifest:
    `<uses-permission android:name="android.permission.CAMERA" />`
- Vérifier si la permission a été donnée
- La demander sinon (éventuellement demander à devenir app par défaut)
- Éxecuter l’action ou expliquer pourquoi elle est impossible en cas de refus

## Example

```kotlin
// Register the permissions callback
val requestPermissionLauncher =
        registerForActivityResult(RequestPermission()) { isGranted ->
            if (isGranted) // Permission is granted
            else // Explain required permission the user denied
    }

// Checking for a permission, and requesting a permission from the user when necessary
when {
    ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) 
        == PackageManager.PERMISSION_GRANTED -> {
        // You can use the API that requires the permission.
    }
    shouldShowRequestPermissionRationale(...) -> {
        // Explain to the user why your app requires this permission
    }
    else -> {
        // ask for the permission
        requestPermissionLauncher.launch(Manifest.permission.CAMERA)
    }
}
```

# iOS

## segues

![height:400px](../assets/segue.png)

```swift
self.performSegue(withIdentifier: "SECOND_SCREEN_SEGUE", for sender: self)
```

[Documentation](https://developer.apple.com/library/archive/featuredarticles/ViewControllerPGforiPhoneOS/UsingSegues.html)

## Handmade delegates for results

```swift
protocol ImageDelegate{
  func onImageReceived(_ picker: ImagePickerController, didReceiveValue value: UIImage)
  func onCancel(_ picker: ImagePickerController)
}

class TakePictureController : UIViewController, ImageDelegate{ ... }
```

## Share Extensions

Separate module with custom ViewController

Capabilities configured with a plist file:

![height:250px](../assets/ios_share_extensions.png)
