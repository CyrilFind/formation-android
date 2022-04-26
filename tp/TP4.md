# TP 4: Images, Permissions, Stockage

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

- Trouvez comment afficher l'image sous la forme d'un cercle avec `Coil`

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

## ActivityResult: Caméra

<aside class="positive">

Afin de demander au système d'exploitation de prendre une photo, on veut récupérer un ["Activity Result"](https://developer.android.com/training/basics/intents/result), comme précédemment pour la création/édition de tâches, mais cette fois avec un Intent [**implicite**](https://developer.android.com/guide/components/intents-filters#ExampleSend)

Pour les cas d'utilisations très courants, il existe [plusieurs "contrats" prédéfinis](https://developer.android.com/reference/androidx/activity/result/contract/ActivityResultContracts) qui simplifient et cachent l'utilisation des intents, et on peut également [définir nos propres contrats](https://developer.android.com/training/basics/intents/result#custom)

</aside>

- On va donc ici utiliser `TakePicturePreview` qui retourne un `Bitmap` (c'est à dire une image stockée dans une variable, pas dans un fichier):

```kotlin
private val getPhoto = registerForActivityResult(TakePicturePreview()) { bitmap ->
    imageView.load(bitmap) // afficher
}
```

- ajoutez un click listener au bouton correspondant pour y utiliser ce launcher: `getPhoto.launch()`

<aside class="negative">

➡️ Si vous testez, ça ne va pas fonctionner tout de suite, car on a pas demandé la **permission** d'accéder à la caméra !

</aside>

## Permissions: Caméra

<aside class="positive">

Afin d'accéder à certaines resources sensibles du téléphone, il faut [demander des permissions](https://developer.android.com/guide/topics/permissions/overview): caméra, stockage de fichiers, etc...

Pour cela, il faut ajouter [ajouter des balises dans le manifest](https://developer.android.com/training/permissions/requesting#add-to-manifest) mais aussi souvent [afficher une popup au moment où on en a besoin](https://developer.android.com/training/permissions/requesting#allow-system-manage-request-code).

</aside>

- Dans `AndroidManifest`: ajoutez donc la balise nécessaire pour accéder à la caméra (facile à trouver sur Google ou les liens ci dessus)
- créez un nouveau launcher pour demander cette permission:

```kotlin
 private val requestCamera =
    registerForActivityResult(RequestPermission()) { accepted ->
        if (accepted) // lancer l'action souhaitée
        else // afficher une explication
    }
```

- Afin d'afficher des explications à l'utilisateur on utilisera cette méthode:

```kotlin
private fun showMessage(message: String) {
    Snackbar.make(findViewById(android.R.id.content), message, Snackbar.LENGTH_LONG).show()
}
```

- Créez cette méthode

```kotlin
private fun launchCameraWithPermission() {
    val camPermission = Manifest.permission.CAMERA
    requestCamera.launch(camPermission)
}
```

- Complétez le launcher et modifiez le click listener afin d'ouvrir la caméra **en demandant la permission**

## Uploader l'image capturée

- Dans l'interface `UserWebService`, ajouter une nouvelle méthode:

```kotlin
@Multipart
@PATCH("users/update_avatar")
suspend fun updateAvatar(@Part avatar: MultipartBody.Part): Response<UserInfo>
```

- Créez une ["extension"](https://kotlinlang.org/docs/extensions.html) qui va convertir l'image en `MultipartBody.Part` afin de pouvoir l'envoyer en HTTP:

```kotlin
private fun Bitmap.toRequestBody(): MultipartBody.Part {
    val tmpFile = File.createTempFile("avatar", "jpeg")
    tmpFile.outputStream().use {
        this.compress(Bitmap.CompressFormat.JPEG, 100, it) // this est le bitmap dans ce contexte
    }
    return MultipartBody.Part.createFormData(
        name = "avatar",
        filename = "temp.jpeg",
        body = tmpFile.readBytes().toRequestBody()
    )
}
```

- Dans la cacllback de `getPhoto`, envoyez l'image au serveur avec `updateAvatar` et en convertissant `bitmap` avec `toRequestBody`
- Modifiez `UserInfo` pour ajouter un champ `val avatar: String?` afin de pouvoir recevoir l'URL à laquelle l'image sera stockée sur le serveur

<aside class="negative">

⚠️ Attention c'est un tout petit serveur qui va automatiquement supprimer les images stockées automatiquement donc ne vous inquiétez pas si l'image ne s'affiche plus après un certain temps

</aside>

- Enfin, au chargement de l'activité, afficher l'avatar renvoyé depuis le serveur:

```kotlin
lifecycleScope.launch {
    val userInfo = ...getInfos()...
    imageView.load(userInfo.avatar) {
        error(R.drawable.ic_launcher_background) // affiche une image par défaut en cas d'erreur:
    }
}
```

## Gérer le refus

<aside class="positive">

Il y a tout une gestion [assez compliquée](https://developer.android.com/training/permissions/requesting#workflow_for_requesting_permissions) notamment dans le cas où l'utilisateur *refuse* une permission

</aside>

- Modifiez votre code pour suivre les recommendations de google en vous aidant de ceci:

```kotlin
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
```

<aside class="positive">

Par ex, si l'utilisateur refuse trop de fois la permission, la popup système ne s'affiche plus avec le launcher et il doit aller dans les paramètres système pour les autoriser

</aside>

- Modifiez votre code pour permettre à l'utilisateur d'ouvrir les paramètres système liés à votre app:

```kotlin
private fun showMessage(message: String) {
    Snackbar.make(findViewById(android.R.id.content), message, Snackbar.LENGTH_LONG)
        .setAction("Open Settings") {
            val intent = Intent(
                ACTION_APPLICATION_DETAILS_SETTINGS,
                Uri.fromParts("package", packageName, null)
            )
            startActivity(intent)
        }
        .show()
}
```

## Stockage: Accéder et uploader

On va maintenant permettre à l'utilisateur d'uploader une image enregistrée sur son téléphone

<aside class="positive">

Pour cela, il faut avoir la permission d'écrire sur le stockage de l'appareil, et la gestion de ces permissions est très compliquée selon les différents versions de l'OS, etc.

</aside>

Pour simplifier la gestion du stockage on utilisera [ModernStorage](https://google.github.io/modernstorage/mediastore/):

```groovy
implementation("com.google.modernstorage:modernstorage-bom:1.0.0-alpha06")
implementation("com.google.modernstorage:modernstorage-permissions")
implementation("com.google.modernstorage:modernstorage-storage")
implementation("com.squareup.okio:okio")
```

- ajoutez `READ_EXTERNAL_STORAGE` au manifest

- Pour demander la permission:

```kotlin
// launcher pour la permission d'accès au stockage
val requestReadAccess = registerForActivityResult(RequestAccess()) { hasAccess ->
    if (hasAccess) {
        // launch gallery
    } else {
        // message
    }
}

fun openGallery() {
    requestReadAccess.launch(
        RequestAccess.Args(
            action = Action.READ,
            types = listOf(StoragePermissions.FileType.Image),
            createdBy = StoragePermissions.CreatedBy.AllApps
        )
    )
}
```

- Pour ouvrir le sélecteur de fichiers:

```kotlin
// register
private val galleryLauncher = registerForActivityResult(GetContent()) { uri ->
    // au retour de la galerie on fera quasiment pareil qu'au retour de la caméra mais avec une URI àla place du bitmap
}

// use
galleryLauncher.launch("image/*")
```

- Gérez le retour de l'uri, quasiment comme la caméra, vous aurez besoin d'une variante de l'extension précédente pour l'URI:

```kotlin
private fun Uri.toRequestBody(): MultipartBody.Part {
    val fileInputStream = contentResolver.openInputStream(this)!!
    val fileBody = fileInputStream.readBytes().toRequestBody()
    return MultipartBody.Part.createFormData(
        name = "avatar",
        filename = "temp.jpeg",
        body = fileBody
    )
}
```

## Amélioration de la caméra

<aside class="positive">

Actuellement, la qualité d'image récupérée de l'appareil photo est très faible (car passée en `Bitmap`), pour changer cela il faut utiliser le contrat `TakePicture` qui retourne directement une `Uri`

Et il faut également demander la permission d'accéder aux fichiers (en écriture !)

</aside>

- ajoutez [`WRITE_EXTERNAL_STORAGE`](https://developer.android.com/training/data-storage/shared/media#scoped_storage_enabled) au manifest

- aidez vous de la [documentation](https://google.github.io/modernstorage/storage/), de ce que vous avez fait précédemment, et de ce squelette:

```kotlin
private val fileSystem by lazy { AndroidFileSystem(this) } // pour interagir avec le stockage

private lateinit var photoUri: Uri // on stockera l'uri dans cette variable

private val getPhoto = registerForActivityResult(TakePicture()) { success ->
    // afficher et uploader l'image enregistrée dans `photoUri`
}

private val requestCamera =
    registerForActivityResult(ActivityResultContracts.RequestPermission()) { accepted ->
        // créer et stocker l'uri:
        photoUri = fileSystem.createMediaStoreUri(
            filename = "picture-${UUID.randomUUID()}.jpg",
            collection = MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
            directory = "Todo",
        )!!
        openCamera.launch(photoUri)
    }

val requestWriteAccess = registerForActivityResult(RequestAccess()) { accepted ->
    // utiliser le code précédent de `launchCameraWithPermissions`
}

fun launchCameraWithPermissions() {
    requestWriteAccess.launch(
        RequestAccess.Args(
            action = Action.READ_AND_WRITE,
            types = listOf(StoragePermissions.FileType.Image),
            createdBy = StoragePermissions.CreatedBy.Self
        )
    )
}
```

## Édition infos utilisateurs

- Comme précédemment, re-factorisez cette Activity en utilisant un `UserInfoViewModel`
- Dans `UserInfoActivity`, permettre d'éditer et d'afficher les informations (nom, prénom, email) en respectant cette architecture
- Vous aurez besoin d'ajouter ça à `UserWebService`:

```kotlin
@PATCH("users")
suspend fun update(@Body user: UserInfo): Response<UserInfo>
```
