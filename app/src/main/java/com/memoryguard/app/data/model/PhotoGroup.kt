package com.memoryguard.app.data.model

import android.net.Uri

/**
 * A meaningful category of photos produced by AI (or fallback) grouping.
 */
data class PhotoGroup(
    val id: String,
    val categoryName: String,
    val photoCount: Int,
    val thumbnailUri: Uri?,
    val description: String,
    val photoIds: List<Long>,
    val isMarkedSafeToDelete: Boolean = false
)
