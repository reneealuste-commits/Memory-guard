package com.memoryguard.app.ui.main

import com.memoryguard.app.data.drive.DriveGroupUploadState
import com.memoryguard.app.data.model.GroupingStage
import com.memoryguard.app.data.model.PhotoGroup
import com.memoryguard.app.localization.AppLanguage

/**
 * UI state for the main (home) screen.
 */
data class MainUiState(
    val hasGalleryPermission: Boolean = false,
    val language: AppLanguage = AppLanguage.ENGLISH,
    val stage: GroupingStage = GroupingStage.IDLE,
    val groups: List<PhotoGroup> = emptyList(),
    val errorMessage: String? = null,
    val isUsingAi: Boolean = true,
    val snackbarMessage: String? = null,
    /** Group id for the Drive "why" dialog; null when hidden. */
    val driveExplainerGroupId: String? = null,
    /** Upload progress keyed by photo group id. */
    val driveUploads: Map<String, DriveGroupUploadState> = emptyMap()
) {
    val isLoading: Boolean
        get() = stage == GroupingStage.SCANNING_GALLERY ||
            stage == GroupingStage.PREPARING_THUMBNAILS ||
            stage == GroupingStage.ANALYZING_WITH_AI

    val showGroups: Boolean
        get() = groups.isNotEmpty() && stage == GroupingStage.DONE

    fun driveUploadFor(groupId: String): DriveGroupUploadState? = driveUploads[groupId]
}
