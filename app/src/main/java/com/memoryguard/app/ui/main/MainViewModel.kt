package com.memoryguard.app.ui.main

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.memoryguard.app.BuildConfig
import com.memoryguard.app.R
import com.memoryguard.app.data.ai.PhotoGroupingRepository
import com.memoryguard.app.data.drive.DriveGroupUploadState
import com.memoryguard.app.data.drive.GoogleAuthHelper
import com.memoryguard.app.data.drive.GoogleDriveRepository
import com.memoryguard.app.data.model.GroupingStage
import com.memoryguard.app.data.model.PhotoGroup
import com.memoryguard.app.localization.AppLanguage
import com.memoryguard.app.localization.LanguagePreferences
import com.memoryguard.app.util.PermissionUtils
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

/**
 * Handles permission state, gallery scan, AI grouping, and Google Drive uploads.
 */
class MainViewModel(application: Application) : AndroidViewModel(application) {

    private val groupingRepository = PhotoGroupingRepository(application)
    private val languagePreferences = LanguagePreferences(application)
    private val googleAuthHelper = GoogleAuthHelper(application)
    private val googleDriveRepository = GoogleDriveRepository(application)

    private val _uiState = MutableStateFlow(
        MainUiState(
            hasGalleryPermission = PermissionUtils.hasGalleryPermission(application),
            language = languagePreferences.getLanguage(),
            isUsingAi = hasVisionApiKey()
        )
    )
    val uiState: StateFlow<MainUiState> = _uiState.asStateFlow()

    private val _languageChangeEvents = MutableSharedFlow<AppLanguage>()
    val languageChangeEvents: SharedFlow<AppLanguage> = _languageChangeEvents.asSharedFlow()

    /** Activity should launch Google Sign-In when this fires. */
    private val _googleSignInRequests = MutableSharedFlow<Unit>(extraBufferCapacity = 1)
    val googleSignInRequests: SharedFlow<Unit> = _googleSignInRequests.asSharedFlow()

    /** Group to upload after sign-in completes. */
    private var pendingDriveGroupId: String? = null

    init {
        viewModelScope.launch {
            groupingRepository.stage.collect { stage ->
                _uiState.update { it.copy(stage = stage) }
            }
        }
    }

    fun onPermissionResult(granted: Boolean) {
        _uiState.update {
            it.copy(
                hasGalleryPermission = granted,
                errorMessage = if (granted) null else it.errorMessage
            )
        }
    }

    fun refreshPermissionState() {
        val granted = PermissionUtils.hasGalleryPermission(getApplication())
        _uiState.update { it.copy(hasGalleryPermission = granted) }
    }

    fun scanAndGroupPhotos() {
        if (!_uiState.value.hasGalleryPermission) return
        viewModelScope.launch {
            _uiState.update { it.copy(errorMessage = null, snackbarMessage = null) }
            groupingRepository.resetStage()
            val result = groupingRepository.scanAndGroup()
            result.fold(
                onSuccess = { data ->
                    _uiState.update {
                        it.copy(
                            groups = data.groups,
                            stage = GroupingStage.DONE,
                            isUsingAi = hasVisionApiKey()
                        )
                    }
                },
                onFailure = { error ->
                    groupingRepository.resetStage()
                    val app = getApplication<Application>()
                    val message = when {
                        !PermissionUtils.hasGalleryPermission(app) ->
                            app.getString(R.string.error_permission_denied)
                        else ->
                            error.message ?: app.getString(R.string.error_generic)
                    }
                    _uiState.update {
                        it.copy(
                            errorMessage = message,
                            stage = GroupingStage.IDLE,
                            groups = emptyList()
                        )
                    }
                }
            )
        }
    }

    fun toggleLanguage() {
        val next = _uiState.value.language.toggle()
        languagePreferences.setLanguage(next)
        _uiState.update { it.copy(language = next) }
        viewModelScope.launch { _languageChangeEvents.emit(next) }
    }

    /** User tapped Save to Google Drive — show explainer first. */
    fun onSaveToDriveRequested(groupId: String) {
        _uiState.update { it.copy(driveExplainerGroupId = groupId) }
    }

    fun dismissDriveExplainer() {
        _uiState.update { it.copy(driveExplainerGroupId = null) }
    }

    /** User confirmed the Drive explainer dialog. */
    fun onDriveExplainerConfirmed(groupId: String) {
        _uiState.update { it.copy(driveExplainerGroupId = null) }
        if (googleAuthHelper.isSignedIn()) {
            startDriveUpload(groupId)
        } else {
            pendingDriveGroupId = groupId
            _googleSignInRequests.tryEmit(Unit)
        }
    }

    fun onGoogleSignInSuccess(account: GoogleSignInAccount) {
        val groupId = pendingDriveGroupId
        pendingDriveGroupId = null
        if (groupId != null) {
            startDriveUpload(groupId, account)
        }
    }

    fun onGoogleSignInFailed() {
        pendingDriveGroupId = null
        _uiState.update {
            it.copy(snackbarMessage = SNACKBAR_DRIVE_SIGN_IN_FAILED)
        }
    }

    fun onGoogleSignInCancelled() {
        pendingDriveGroupId = null
    }

    private fun startDriveUpload(
        groupId: String,
        account: GoogleSignInAccount = googleAuthHelper.getLastSignedInAccount()
            ?: return
    ) {
        val group = _uiState.value.groups.find { it.id == groupId } ?: return
        if (_uiState.value.driveUploads[groupId]?.isUploading == true) return

        viewModelScope.launch {
            val total = group.photoIds.size.coerceAtMost(40)
            _uiState.update { state ->
                state.copy(
                    driveUploads = state.driveUploads + (
                        groupId to DriveGroupUploadState(
                            isUploading = true,
                            uploadedCount = 0,
                            totalCount = total
                        )
                        )
                )
            }

            val result = googleDriveRepository.uploadMemoryBundle(
                account = account,
                group = group,
                onProgress = { uploaded, uploadTotal ->
                    _uiState.update { state ->
                        state.copy(
                            driveUploads = state.driveUploads + (
                                groupId to DriveGroupUploadState(
                                    isUploading = true,
                                    uploadedCount = uploaded,
                                    totalCount = uploadTotal
                                )
                                )
                        )
                    }
                }
            )

            result.fold(
                onSuccess = {
                    _uiState.update { state ->
                        state.copy(
                            groups = state.groups.map { g ->
                                if (g.id == groupId) g.copy(isSavedToDrive = true) else g
                            },
                            driveUploads = state.driveUploads + (
                                groupId to DriveGroupUploadState(
                                    isUploading = false,
                                    uploadedCount = it.uploadedPhotoCount,
                                    totalCount = it.uploadedPhotoCount
                                )
                                ),
                            snackbarMessage = SNACKBAR_DRIVE_SUCCESS
                        )
                    }
                },
                onFailure = { error ->
                    val message = error.message ?: getApplication<Application>()
                        .getString(R.string.error_drive_upload)
                    _uiState.update { state ->
                        state.copy(
                            driveUploads = state.driveUploads + (
                                groupId to DriveGroupUploadState(
                                    isUploading = false,
                                    errorMessage = message
                                )
                                ),
                            snackbarMessage = SNACKBAR_DRIVE_FAILED
                        )
                    }
                }
            )
        }
    }

    fun onMarkSafeToDelete(groupId: String) {
        _uiState.update { state ->
            state.copy(
                groups = state.groups.map { group ->
                    if (group.id == groupId) group.copy(isMarkedSafeToDelete = true) else group
                },
                snackbarMessage = SNACKBAR_MARKED_SAFE
            )
        }
    }

    fun clearSnackbar() {
        _uiState.update { it.copy(snackbarMessage = null) }
    }

    fun clearError() {
        _uiState.update { it.copy(errorMessage = null) }
    }

    private fun hasVisionApiKey(): Boolean =
        BuildConfig.GEMINI_API_KEY.isNotBlank() || BuildConfig.OPENAI_API_KEY.isNotBlank()

    companion object {
        const val SNACKBAR_MARKED_SAFE = "marked_safe_to_delete"
        const val SNACKBAR_DRIVE_SUCCESS = "drive_upload_success"
        const val SNACKBAR_DRIVE_FAILED = "drive_upload_failed"
        const val SNACKBAR_DRIVE_SIGN_IN_FAILED = "drive_sign_in_failed"
    }
}
