package com.memoryguard.app.data.drive

/**
 * Outcome of uploading a memory bundle to Google Drive.
 */
data class DriveUploadResult(
    val folderId: String,
    val folderName: String,
    val uploadedPhotoCount: Int
)
