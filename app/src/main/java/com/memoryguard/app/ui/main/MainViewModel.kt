package com.memoryguard.app.ui.main

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.memoryguard.app.BuildConfig
import com.memoryguard.app.R
import com.memoryguard.app.data.ai.PhotoGroupingRepository
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
 * Handles permission state, gallery scan, and AI grouping for the main screen.
 */
class MainViewModel(application: Application) : AndroidViewModel(application) {

    private val groupingRepository = PhotoGroupingRepository(application)
    private val languagePreferences = LanguagePreferences(application)

    private val _uiState = MutableStateFlow(
        MainUiState(
            hasGalleryPermission = PermissionUtils.hasGalleryPermission(application),
            language = languagePreferences.getLanguage(),
            isUsingAi = hasVisionApiKey()
        )
    )
    val uiState: StateFlow<MainUiState> = _uiState.asStateFlow()

    /** Emitted when language changes so the Activity can recreate with a new locale. */
    private val _languageChangeEvents = MutableSharedFlow<AppLanguage>()
    val languageChangeEvents: SharedFlow<AppLanguage> = _languageChangeEvents.asSharedFlow()

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

    /** Placeholder for Drive upload — wired in a future iteration. */
    fun onSaveToDrive(group: PhotoGroup) {
        _uiState.update { it.copy(snackbarMessage = SNACKBAR_COMING_SOON) }
    }

    /** Marks a group as safe to delete locally (does not delete files yet). */
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
        // ViewModel uses string keys; Activity maps them to resources after locale change.
        const val SNACKBAR_COMING_SOON = "coming_soon"
        const val SNACKBAR_MARKED_SAFE = "marked_safe_to_delete"
    }
}
