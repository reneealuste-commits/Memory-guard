package com.memoryguard.app.data.ai

import com.memoryguard.app.data.model.PhotoGroup
import com.memoryguard.app.data.model.PhotoItem
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

/**
 * Offline fallback when no vision API key is configured.
 * Groups photos by month so the UI remains usable during development.
 */
class LocalFallbackGrouper : PhotoGrouper {

    override suspend fun groupPhotos(
        photos: List<PhotoItem>,
        thumbnailsByPhotoId: Map<Long, ByteArray>
    ): List<PhotoGroup> {
        if (photos.isEmpty()) return emptyList()

        val formatter = SimpleDateFormat("MMMM yyyy", Locale.getDefault())
        return photos
            .groupBy { photo ->
                formatter.format(Date(photo.dateAddedSeconds * 1000L))
            }
            .map { (monthLabel, items) ->
                PhotoGroup(
                    id = UUID.randomUUID().toString(),
                    categoryName = monthLabel,
                    photoCount = items.size,
                    thumbnailUri = items.first().uri,
                    description = "Photos from $monthLabel (local grouping — add an API key for AI categories).",
                    photoIds = items.map { it.id }
                )
            }
            .sortedByDescending { it.photoCount }
    }
}
