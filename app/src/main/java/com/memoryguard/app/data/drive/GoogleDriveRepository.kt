package com.memoryguard.app.data.drive

import android.content.ContentUris
import android.content.Context
import android.provider.MediaStore
import android.provider.OpenableColumns
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.api.client.googleapis.extensions.android.gms.auth.GoogleAccountCredential
import com.google.api.client.http.InputStreamContent
import com.google.api.client.http.javanet.NetHttpTransport
import com.google.api.client.json.gson.GsonFactory
import com.google.api.services.drive.Drive
import com.google.api.services.drive.DriveScopes
import com.google.api.services.drive.model.File
import com.memoryguard.app.data.model.PhotoGroup
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.BufferedInputStream
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Creates a Memory Guard folder in the user's Google Drive and uploads bundle photos.
 */
class GoogleDriveRepository(private val context: Context) {

    /**
     * Uploads all photos in [group] into:
     * `Memory Guard / {categoryName}_{date} / photo_*.jpg`
     */
    suspend fun uploadMemoryBundle(
        account: GoogleSignInAccount,
        group: PhotoGroup,
        onProgress: (uploaded: Int, total: Int) -> Unit
    ): Result<DriveUploadResult> = withContext(Dispatchers.IO) {
        runCatching {
            val credential = GoogleAccountCredential.usingOAuth2(
                context,
                listOf(DriveScopes.DRIVE_FILE)
            )
            credential.selectedAccount = account.account

            val driveService = Drive.Builder(
                NetHttpTransport(),
                GsonFactory.getDefaultInstance(),
                credential
            )
                .setApplicationName(APPLICATION_NAME)
                .build()

            val memoryGuardRootId = findOrCreateFolder(
                driveService,
                folderName = ROOT_FOLDER_NAME,
                parentId = "root"
            )

            val bundleFolderName = buildBundleFolderName(group.categoryName)
            val bundleFolderId = findOrCreateFolder(
                driveService,
                folderName = bundleFolderName,
                parentId = memoryGuardRootId
            )

            val photoIds = group.photoIds.take(MAX_PHOTOS_PER_BUNDLE)
            if (photoIds.isEmpty()) {
                throw IllegalStateException("No photos in this group to upload")
            }

            photoIds.forEachIndexed { index, photoId ->
                val uri = ContentUris.withAppendedId(
                    MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
                    photoId
                )
                uploadPhotoFromUri(driveService, uri, photoId, bundleFolderId)
                onProgress(index + 1, photoIds.size)
            }

            DriveUploadResult(
                folderId = bundleFolderId,
                folderName = bundleFolderName,
                uploadedPhotoCount = photoIds.size
            )
        }
    }

    private fun buildBundleFolderName(categoryName: String): String {
        val dateLabel = SimpleDateFormat("yyyy-MM-dd", Locale.US).format(Date())
        val safeCategory = sanitizeFolderName(categoryName)
        return "${safeCategory}_$dateLabel"
    }

    private fun sanitizeFolderName(name: String): String {
        return name
            .trim()
            .replace(Regex("""[\\/:*?"<>|]"""), "-")
            .take(60)
            .ifBlank { "Memory_Bundle" }
    }

    private fun findOrCreateFolder(
        driveService: Drive,
        folderName: String,
        parentId: String
    ): String {
        val escapedName = folderName.replace("'", "\\'")
        val query = buildString {
            append("mimeType='application/vnd.google-apps.folder'")
            append(" and trashed=false")
            append(" and name='$escapedName'")
            append(" and '$parentId' in parents")
        }

        val existing = driveService.files().list()
            .setQ(query)
            .setSpaces("drive")
            .setFields("files(id)")
            .setPageSize(1)
            .execute()
            .files
            ?.firstOrNull()
            ?.id

        if (existing != null) return existing

        val metadata = File().apply {
            name = folderName
            mimeType = "application/vnd.google-apps.folder"
            parents = listOf(parentId)
        }
        return driveService.files().create(metadata)
            .setFields("id")
            .execute()
            .id
    }

    private fun uploadPhotoFromUri(
        driveService: Drive,
        uri: android.net.Uri,
        photoId: Long,
        parentFolderId: String
    ) {
        val (displayName, mimeType) = resolveDisplayNameAndMime(uri)
        val fileName = displayName ?: "memory_guard_$photoId.jpg"
        val resolvedMime = mimeType ?: "image/jpeg"

        context.contentResolver.openInputStream(uri)?.use { rawStream ->
            val metadata = File().apply {
                name = fileName
                parents = listOf(parentFolderId)
            }
            val mediaContent = InputStreamContent(
                resolvedMime,
                BufferedInputStream(rawStream)
            )
            driveService.files()
                .create(metadata, mediaContent)
                .setFields("id")
                .execute()
        } ?: throw IllegalStateException("Could not read photo $photoId from gallery")
    }

    private fun resolveDisplayNameAndMime(uri: android.net.Uri): Pair<String?, String?> {
        var name: String? = null
        var mime: String? = context.contentResolver.getType(uri)
        context.contentResolver.query(
            uri,
            arrayOf(OpenableColumns.DISPLAY_NAME),
            null,
            null,
            null
        )?.use { cursor ->
            if (cursor.moveToFirst()) {
                val index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                if (index >= 0) name = cursor.getString(index)
            }
        }
        return name to mime
    }

    companion object {
        private const val APPLICATION_NAME = "Memory Guard"
        private const val ROOT_FOLDER_NAME = "Memory Guard"
        private const val MAX_PHOTOS_PER_BUNDLE = 40
    }
}
