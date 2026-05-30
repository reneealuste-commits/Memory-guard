package com.memoryguard.app.data.ai

import com.memoryguard.app.data.model.PhotoGroup
import com.memoryguard.app.data.model.PhotoItem

/**
 * Abstraction for vision-based photo grouping (Gemini, GPT-4o, or local fallback).
 */
interface PhotoGrouper {
    suspend fun groupPhotos(
        photos: List<PhotoItem>,
        thumbnailsByPhotoId: Map<Long, ByteArray>
    ): List<PhotoGroup>
}
