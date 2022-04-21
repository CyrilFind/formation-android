# TP 5: Images, Permissions, Stockage

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
- Lisez, utilisez et complétez ce pavé de code:

```kotlin
 private val cameraPermissionLauncher =
        registerForActivityResult(RequestPermission()) { accepted ->
            if (accepted) // lancer l'action souhaitée
            else // afficher une explication
        }

private fun launchCameraWithPermission() {
    val camPermission = Manifest.permission.CAMERA
    val permissionStatus = checkSelfPermission(camPermission)
    val isAlreadyAccepted = permissionStatus == PackageManager.PERMISSION_GRANTED
    val isExplanationNeeded = shouldShowRequestPermissionRationale(camPermission)
    when {
        isAlreadyAccepted -> // lancer l'action souhaitée
        isExplanationNeeded -> // afficher une explication
        else -> // lancer la demande de permission
    }
}

private fun showExplanation() {
    // ici on construit une pop-up système (Dialog) pour expliquer la nécessité de la demande de permission
    AlertDialog.Builder(this)
        .setMessage("🥺 On a besoin de la caméra, vraiment! 👉👈")
        .setPositiveButton("Bon, ok") { _, _ -> /* ouvrir les paramètres de l'app */ }
        .setNegativeButton("Nope") { dialog, _ -> dialog.dismiss() }
        .show()
}

private fun launchAppSettings() {
    // Cet intent permet d'ouvrir les paramètres de l'app (pour modifier les permissions déjà refusées par ex)
    val intent = Intent(
        Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
        Uri.fromParts("package", packageName, null)
    )
    // ici pas besoin de vérifier avant car on vise un écran système:
    startActivity(intent)
}

private fun handleImage(imageUri: Uri) {
    // afficher l'image dans l'ImageView
}

private fun launchCamera() {
    // à compléter à l'étape suivante
}
```

Dans `onCreate()`, faire en sorte que le bouton correspondant ouvre la caméra (en demandant la permission)

## Ouvrir l'appareil photo

Pour l'ouverture de la caméra, on va créer un launcher, comme précédemment, mais avec autre "contrat":

```kotlin
// register
private val cameraLauncher = registerForActivityResult(TakePicturePreview()) { bitmap ->
        val tmpFile = File.createTempFile("avatar", "jpeg")
        tmpFile.outputStream().use {
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, it)
        }
        handleImage(tmpFile.toUri())
    }

// use
private fun launchCamera() {
    cameraLauncher.launch()
}
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
private fun convert(uri: Uri): MultipartBody.Part {
    return MultipartBody.Part.createFormData(
        name = "avatar",
        filename = "temp.jpeg",
        body = contentResolver.openInputStream(uri)!!.readBytes().toRequestBody()
    )
}
```

- Dans `handleImage`, envoyez l'image au serveur avec `updateAvatar` et `convert`
- Modifiez `UserInfo` pour ajouter un champ `val avatar: String?`: c'est une URL qui sera renvoyée depuis le serveur
- Enfin, au chargement de l'activité, afficher l'avatar renvoyé depuis le serveur:

```kotlin
lifecycleScope.launch {
    val userInfo = ...getInfos()...
    imageView.load(userInfo.avatar) {
        // affiche une image par défaut en cas d'erreur:
        error(R.drawable.ic_launcher_background)
    }
}
```

## Accéder aux fichiers locaux

Actuellement, la qualité d'image récupérée de l'appareil photo est faible (car passée dans le code en bitmap)

Améliorer cette qualité en changeant le fonctionnement pour enregistrer directement l'image dans un fichier... mais c'est un peu compliqué alors on va utiliser [MediaStore](https://google.github.io/modernstorage/mediastore/) de la lib `modernstorage` (faite par Google)

```groovy
implementation "com.google.modernstorage:modernstorage-mediastore:1.0.0-alpha06"
```

Dans votre nouvelle Activity:

```kotlin
val mediaStore by lazy { MediaStoreRepository(this) }
```

- Vous pourrez ensuite utiliser:

```kotlin
// créer un launcher pour la caméra
private val cameraLauncher =
    registerForActivityResult(TakePicture()) { accepted ->
        val view = // n'importe quelle vue (ex: un bouton, binding.root, window.decorView, ...)
        if (accepted) handleImage()
        else Snackbar.make(view, "Échec!", Snackbar.LENGTH_LONG).show()
    }


// utiliser
private lateinit var photoUri: Uri
private fun launchCamera() {
    lifecycleScope.launch {
        photoUri = mediaStore.createMediaUri(
            filename = "picture-${UUID.randomUUID()}.jpg",
            type = FileType.IMAGE,
            location = SharedPrimary
        ).getOrThrow()
        cameraLauncher.launch(photoUri)
    }
}
```

Afin de gérer Android 9 et antérieurs, il faut également avoir la permission `android.permission.WRITE_EXTERNAL_STORAGE`: ajouter la dans `AndroidManifest.xml` et adaptez le launcher avec `RequestMultiplePermissions`:

```kotlin
 private val permissionAndCameraLauncher = registerForActivityResult(RequestMultiplePermissions()) { results ->
     // pour simplifier on ne fait rien ici, il faudra que le user re-clique sur le bouton
 }

 private fun launchCameraWithPermission() {
        // ...
        val storagePermission = Manifest.permission.WRITE_EXTERNAL_STORAGE
        when {
            mediaStore.canWriteSharedEntries() && isAlreadyAccepted ->  ...
            // ... 
            else -> permissionAndCameraLauncher.launch(arrayOf(camPermission, storagePermission))
        }
    }

```

## Uploader une image stockée

Permettez à l'utilisateur d'uploader une image enregistrée sur son téléphone

```kotlin
// register
private val galleryLauncher = registerForActivityResult(GetContent()) {...}

// use
galleryLauncher.launch("image/*")
```

## Édition infos utilisateurs

- Comme précédemment, re-factorisez en utilisant un `UserInfoViewModel` et un `UserInfoRepository`
- Dans `UserInfoActivity`, permettre d'éditer et d'afficher les informations (nom, prénom, email) en respectant cette architecture
- Vous aurez besoin d'ajouter ça à `UserWebService`:

```kotlin
@PATCH("users")
suspend fun update(@Body user: UserInfo): Response<UserInfo>
```
