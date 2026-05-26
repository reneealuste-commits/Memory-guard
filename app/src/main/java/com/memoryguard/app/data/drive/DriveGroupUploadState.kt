package com.memoryguard.app.data.drive

/**
 * Per-group upload progress shown on photo cards.
 */
data class DriveGroupUploadState(
    val isUploading: Boolean = false,
    val uploadedCount: Int = 0,
    val totalCount: Int = 0,
    val errorMessage: String? = null
)
