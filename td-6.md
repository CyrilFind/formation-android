
# TD 6: Images
## Afficher une image distante avec Glide

### Ajout des dépendances

Dans le fichier `app/build.gradle`, ajouter :

```groovy
    implementation 'com.github.bumptech.glide:glide:4.10.0'
    annotationProcessor 'com.github.bumptech.glide:compiler:4.10.0'
```

- Ajouter une `ImageView` à coté de votre `header_text_view` qui affichera l'avatar de l'utilisateur
- Dans `onResume`, utiliser Glide pour afficher une image de test:

```kotlin
Glide.with(this).load("https://goo.gl/gEgYUd").into(image_view)
```

- À partir de la [documentation de Glide](https://github.com/bumptech/glide), afficher l'image sous la forme d'un cercle

### Nouvelle activité
- Créer une nouvelle activité `UserInfoActivity` et ajoutez la dans le manifest
- Remplir son layout:

```xml
<LinearLayout ...>
    <ImageView
        android:id="@+id/image_view"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />
        
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
- Lancer cette appli quand on clique sur l'`ImageView` que vous venez de remplir avec `Glide`

## Demander la Permission

- `AndroidManifest`: ajouter la permission `android.permission.CAMERA`
- `UserInfoActivity` : Dans `onCreate()`, ajouter un `onClickListener` à `take_picture_button`qui appele la méthode `askCameraPermissionAndOpenCamera()`


```kotlin

private fun askCameraPermissionAndOpenCamera() {
  if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
    if (ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.CAMERA)) {
        // l'OS dit d'expliquer pourquoi on a besoin de cette permission:
        showDialogBeforeRequest()    
    } else {
        // l'OS ne demande pas d'explication, on demande directement:
        requestCameraPermission()
    }
  } else {
    openCamera()
  }
}

private fun showDialogBeforeRequest() {
    // Affiche une popup (Dialog) d'explications: 
    AlertDialog.Builder(this).apply {
        setMessage("On a besoin de la caméra sivouplé ! 🥺")
        setPositiveButton(android.R.string.ok) { _, _ -> requestCameraPermission() }
        setCancelable(true)
        show()
    }
}

private fun requestCameraPermission() {
    // CAMERA_PERMISSION_CODE est défini par nous et sera récupéré dans onRequestPermissionsResult
    ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), CAMERA_PERMISSION_CODE )
}

private fun openCamera() {
    // On va utiliser un Intent implicite
}

companion object {
    const val CAMERA_PERMISSION_CODE = 42
}
```

- Prenez le temps de lire et comprendre ce pavé 🤔
- Overrider la méthode `onRequestPermissionsResult`:
Si l'utilisateur à donné accès à la camera, utilisez `openCamera()`:

```kotlin 
if (requestCode == CAMERA_PERMISSION_CODE && grantResults.firstOrNull() == PackageManager.PERMISSION_GRANTED)
```
Sinon, affichez un Toast:

```kotlin
Toast.makeText(this, "Si vous refusez, on peux pas prendre de photo ! 😢", Toast.LENGTH_LONG).show()
```


## Ouvrir l'appareil photo

- Il est possible d'ouvrir des `Intent` et de récuperer des informations grâce à la fonction `startActivityForResult` qui est jumelée à la fonction `onActivityResult`

```kotlin
private fun openCamera() {
  val cameraIntent = Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE)
  startActivityForResult(cameraIntent, CAMERA_REQUEST_CODE)
}
```

- Déclarer la constante `CAMERA_REQUEST_CODE`

```kotlin
const val CAMERA_REQUEST_CODE = 2001
```

- Implémenter la fonction `onActivityResult` qui appelera la fonction `handlePhotoTaken(data: Intent?)`:


```kotlin
private fun handlePhotoTaken(data: Intent?) {
  val image = data?.extras?.get("data") as? Bitmap
  // Afficher l'image ici
  
  val imageBody = imageToBody(image)
  // Plus tard, on l'enverra au serveur
}

// Celle ci n'est pas très intéressante à lire
// En gros, elle lit le fichier et le prépare pour l'envoi HTTP
private fun imageToBody(image: Bitmap?): MultipartBody.Part {
  val f = File(cacheDir, "tmpfile.jpg")
  f.createNewFile()
  try {
      val fos = FileOutputStream(f)
      image?.compress(Bitmap.CompressFormat.PNG, 100, fos)
      fos.flush()
      fos.close()
  } catch (e: FileNotFoundException) {
      e.printStackTrace()
  } catch (e: IOException) {
      e.printStackTrace()
  }
  val body = RequestBody.create(MediaType.parse("image/png"), f)
  return MultipartBody.Part.createFormData("avatar", f.path, body)
}
```

- Dans la fonction `handlePhotoTaken`, afficher la photo à l'aide de Glide

## Uploader l'image capturée

- Dans l'interface `UserService`, ajouter une nouvelle fonction

```kotlin
@Multipart
@PATCH("users/update_avatar")
suspend fun updateAvatar(@Part avatar: MultipartBody.Part): Response<UserInfo>
```

- Dans `handlePhotoTaken`, appelez cette fonction pour mettre à jour le serveur avec le nouvel avatar
- Modifier la `data class UserInfo` pour ajouter un champ `avatar: String` qui est une URL renvoyée depuis le serveur
- Enfin au chargement de l'activité, afficher l'avatar renvoyé depuis le serveur:

```kotlin
    val glide = Glide.with(this)
    lifecycleScope.launch {
        val userInfo = ...getInfos()
        glide.load(userInfo.avatar)...into(...)
    }
```

## Uploader une image stockée
- Ajouter dans le manifest la permission `android.permission.READ_EXTERNAL_STORAGE`
- Permettez à l'utilisateur d'uploader une image qu'il avait déjà sur son téléphone

```kotlin
// Pour ouvrir la gallerie:
val galleryIntent = Intent(Intent.ACTION_PICK)
galleryIntent.type = "image/*"
startActivityForResult(galleryIntent, GALLERY_REQUEST_CODE)

// Pour récupérer le bitmap dans onActivityResult
val bitmap = MediaStore.Images.Media.getBitmap(contentResolver, data?.data)
```

## Édition infos utilisateurs
- Comme pour tasks, refactorisez en utilisant un `UserInfoViewModel` et un `UserInfoRepository`
- Dans `UserInfoActivity`, permettre d'éditer et d'afficher les informations (nom, prénom, email) en respectant cette architecture
- Vous aurez besoin d'ajouter ça à `UserService`:

```kotlin
@PATCH("users")
suspend fun update(@Body user: UserInfo): Response<UserInfo>
```
