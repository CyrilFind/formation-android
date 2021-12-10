# TP 5: Images

## Coil

<aside class="positive">

La lib `Coil` permet d'afficher des images depuis une URL de façon efficace en gérant la taille, le cache, etc... `Picasso` et `Glide` sont les alternatives les plus utilisées.
</aside>

- Rendez vous sur le [repository de Coil](https://coil-kt.github.io/coil/) et lisez le `ReadMe`
- Ajouter les dépendances nécessaires à `app/build.gradle`
- Ajouter une `ImageView` qui affichera l'avatar de l'utilisateur dans le layout de la liste (à coté de votre `TextView` par ex)
- Dans `onResume`, récupérez une référence à cette vue puis utilisez Coil pour afficher une image en passant une URL de votre choix, par exemple:

```kotlin
avatarImageView.load("https://goo.gl/gEgYUd")
```

- Trouvez comment l'image sous la forme d'un cercle avec `Coil`

## Nouvelle activité

- Créer un nouveau package `user`
- Créez y une nouvelle activité `UserInfoActivity` et ajoutez la dans le manifest
- Remplir son layout:

```xml
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:orientation="vertical"
    android:layout_width="match_parent"
    android:layout_height="match_parent" >
    <ImageView
        android:id="@+id/image_view"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        tools:srcCompat="@tools:sample/avatars" />

    <Button
        android:id="@+id/upload_image_button"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Choisir une Image" />

    <Button
        android:id="@+id/take_picture_button"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Prendre une photo" />
</LinearLayout>
```

- Lancer cette `Activity` quand on clique sur l'`ImageView` que vous venez de remplir avec `Coil`

## Demander la Permission

- `AndroidManifest`: ajouter la permission `android.permission.CAMERA`
- `UserInfoActivity` : Dans `onCreate()`, ajouter un `onClickListener` à `take_picture_button` qui appele la méthode `askCameraPermissionAndOpenCamera()`

- Prenez le temps de lire et comprendre ce pavé 🤔 :

```kotlin
private val requestPermissionLauncher =
    registerForActivityResult(RequestPermission()) { accepted ->
        if (accepted) openCamera()
        else showExplanationDialog()
    }

private fun askCameraPermissionAndOpenCamera() {
    val camPermission = Manifest.permission.CAMERA
    val permissionStatus = checkSelfPermission(this, camPermission)
    val isAlreadyAccepted = permissionStatus == PackageManager.PERMISSION_GRANTED
    when {
        isAlreadyAccepted -> openCamera()
        shouldShowRequestPermissionRationale(camPermission) -> showExplanationDialog()
        else -> requestPermissionLauncher.launch(camPermission)
    }
}

private fun showExplanationDialog() {
    AlertDialog.Builder(this)
        .setMessage("On a besoin de la caméra sivouplé ! 🥺")
        .setPositiveButton("Bon, ok") { dialog, _ -> dialog.dismiss() }
        .show()
}

private fun openCamera() {
}
```

➡️ C'est normal que le code ne marche pas tout de suite, il manque des choses

## Ouvrir l'appareil photo

Pour l'ouverture de la caméra, on va créer un launcher, comme précédemment, mais avec autre "contrat":

```kotlin
// register
private val takePicture = registerForActivityResult(TakePicturePreview()) { bitmap ->
        val tmpFile = File.createTempFile("avatar", "jpeg")
        tmpFile.outputStream().use {
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, it)
        }
        handleImage(tmpFile.toUri())
    }

// use
private fun openCamera() = takePicture.launch()
```

<aside class="positive">

Ici le système sous jacent va utiliser un `Intent` implicite demandant au système d'ouvrir une app permettant de prendre une photo (en général l'app photo par défaut)
</aside>

➡️ Il manque encore une brique !

## Uploader l'image capturée

- Dans l'interface `UserWebService`, ajouter une nouvelle fonction

```kotlin
@Multipart
@PATCH("users/update_avatar")
suspend fun updateAvatar(@Part avatar: MultipartBody.Part): Response<UserInfo>
```

- Ajouter une fonction pour convertir l'image en `MultipartBody.Part` afin de pouvoir l'envoyer en HTTP:

```kotlin
// convert
private fun convert(uri: Uri) =
    MultipartBody.Part.createFormData(
        name = "avatar",
        filename = "temp.jpeg",
        body = contentResolver.openInputStream(uri)!!.readBytes().toRequestBody()
    )
```

- Ajoutez une méthode `handleImage` qui utilise `updateAvatar` avec `convert`
- Modifier la `data class UserInfo` pour ajouter un champ `avatar: String` (avec une valeur par défaut): c'est une URL qui sera renvoyée depuis le serveur
- Enfin au chargement de l'activité, afficher l'avatar renvoyé depuis le serveur:

```kotlin
    lifecycleScope.launch {
        val userInfo = ...getInfos()
        imageView.load(userInfo.avatar) {
            // affiche une image en cas d'erreur:
            error(R.drawable.ic_launcher_background) 
        }
    }
```

## Accéder aux fichiers locaux

Actuellement, la qualité d'image récupérée de l'appareil photo est faible (car passée dans le code en bitmap)

Améliorer cette qualité en changeant le fonctionnement pour enregistrer directement l'image dans un fichier...mais c'est un peu compliqué:

Vous devrez pour ça ajouter un `FileProvider` dans `AndroidManifest.xml`:

```xml
<provider
    android:name="androidx.core.content.FileProvider"
    android:authorities="${applicationId}.fileprovider"
    android:exported="false"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>
```

Créez `app/src/main/res/xml/file_paths.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<paths >
    <external-path name="external_files" path="."/>
</paths>
```

- Vous pourrez ensuite utiliser:

```kotlin
// create a temp file and get a uri for it
private val photoUri by lazy {
    FileProvider.getUriForFile(
        this,
        BuildConfig.APPLICATION_ID +".fileprovider",
        File.createTempFile("avatar", ".jpeg", externalCacheDir)

    )
}

// register
private val takePicture = registerForActivityResult(TakePicture()) { success ->
    if (success) handleImage(photoUri)
    else Toast.makeText(this, "Erreur ! 😢", Toast.LENGTH_LONG).show()
}

// use
private fun openCamera() = takePicture.launch(photoUri)
```

- Ajouter dans le manifest la permission `android.permission.READ_EXTERNAL_STORAGE`

## Uploader une image stockée

Permettez à l'utilisateur d'uploader une image enregistrée sur son téléphone

```kotlin
// register
private val pickInGallery =
    registerForActivityResult(GetContent()) { ... }

// use
pickInGallery.launch("image/*")
```

## Édition infos utilisateurs

- Comme précedemment, refactorisez en utilisant un `UserInfoViewModel` et un `UserInfoRepository`
- Dans `UserInfoActivity`, permettre d'éditer et d'afficher les informations (nom, prénom, email) en respectant cette architecture
- Vous aurez besoin d'ajouter ça à `UserWebService`:

```kotlin
@PATCH("users")
suspend fun update(@Body user: UserInfo): Response<UserInfo>
```
