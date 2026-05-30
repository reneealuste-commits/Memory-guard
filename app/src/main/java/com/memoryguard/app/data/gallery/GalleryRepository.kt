package com.memoryguard.app.data.gallery

import android.content.ContentUris
import android.content.Context
import android.net.Uri
import android.provider.MediaStore
import com.memoryguard.app.data.model.PhotoItem
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Reads recent images from the system photo gallery via MediaStore.
 */
class GalleryRepository(private val context: Context) {

    /**
     * @param limit Maximum number of recent photos to load (newest first).
     */
    suspend fun loadRecentPhotos(limit: Int = DEFAULT_SCAN_LIMIT): List<PhotoItem> =
        withContext(Dispatchers.IO) {
            val photos = mutableListOf<PhotoItem>()
            val collection = MediaStore.Images.Media.EXTERNAL_CONTENT_URI
            val projection = arrayOf(
                MediaStore.Images.Media._ID,
                MediaStore.Images.Media.DISPLAY_NAME,
                MediaStore.Images.Media.DATE_ADDED,
                MediaStore.Images.Media.SIZE
            )
            val sortOrder = "${MediaStore.Images.Media.DATE_ADDED} DESC"

            context.contentResolver.query(
                collection,
                projection,
                null,
                null,
                sortOrder
            )?.use { cursor ->
                val idColumn = cursor.getColumnIndexOrThrow(MediaStore.Images.Media._ID)
                val nameColumn = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DISPLAY_NAME)
                val dateColumn = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATE_ADDED)
                val sizeColumn = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.SIZE)

                while (cursor.moveToNext() && photos.size < limit) {
                    val id = cursor.getLong(idColumn)
                    val uri = ContentUris.withAppendedId(collection, id)
                    photos.add(
                        PhotoItem(
                            id = id,
                            uri = uri,
                            displayName = cursor.getString(nameColumn),
                            dateAddedSeconds = cursor.getLong(dateColumn),
                            sizeBytes = cursor.getLong(sizeColumn)
                        )
                    )
                }
            }
            photos
        }

    companion object {
        const val DEFAULT_SCAN_LIMIT = 48
    }
}
