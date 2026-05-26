package com.memoryguard.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.memoryguard.app.localization.AppLanguage
import com.memoryguard.app.localization.LanguagePreferences
import com.memoryguard.app.localization.LocaleContextWrapper
import com.memoryguard.app.ui.main.MainScreen
import com.memoryguard.app.ui.main.MainViewModel
import com.memoryguard.app.ui.theme.MemoryGuardTheme
import com.memoryguard.app.util.PermissionUtils
import kotlinx.coroutines.launch

/**
 * Host activity for Memory Guard. Manages gallery permission and hosts the main Compose UI.
 */
class MainActivity : ComponentActivity() {

    private val viewModel: MainViewModel by viewModels()

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { results ->
        val granted = results.values.all { it }
        viewModel.onPermissionResult(granted)
        if (granted) {
            viewModel.scanAndGroupPhotos()
        }
    }

    override fun attachBaseContext(newBase: android.content.Context) {
        val language = LanguagePreferences(newBase).getLanguage()
        super.attachBaseContext(LocaleContextWrapper.wrap(newBase, language))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.languageChangeEvents.collect { language ->
                    (application as MemoryGuardApplication).applyLocale(language)
                    recreate()
                }
            }
        }

        setContent {
            val uiState by viewModel.uiState.collectAsState()

            MemoryGuardTheme {
                MainScreen(
                    uiState = uiState,
                    onRequestPermission = ::requestGalleryPermission,
                    onScanPhotos = viewModel::scanAndGroupPhotos,
                    onToggleLanguage = viewModel::toggleLanguage,
                    onSaveToDrive = { groupId ->
                        uiState.groups.find { it.id == groupId }?.let(viewModel::onSaveToDrive)
                    },
                    onSafeToDelete = viewModel::onMarkSafeToDelete,
                    onRetry = viewModel::scanAndGroupPhotos,
                    onSnackbarShown = viewModel::clearSnackbar
                )
            }
        }
    }

    override fun onResume() {
        super.onResume()
        viewModel.refreshPermissionState()
    }

    private fun requestGalleryPermission() {
        if (PermissionUtils.hasGalleryPermission(this)) {
            viewModel.onPermissionResult(true)
            viewModel.scanAndGroupPhotos()
        } else {
            permissionLauncher.launch(PermissionUtils.galleryPermissions)
        }
    }
}
