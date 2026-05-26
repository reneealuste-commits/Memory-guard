package com.memoryguard.app.data.model

import android.net.Uri

/**
 * A single image from the device gallery (MediaStore).
 */
data class PhotoItem(
    val id: Long,
    val uri: Uri,
    val displayName: String?,
    val dateAddedSeconds: Long,
    val sizeBytes: Long
)
