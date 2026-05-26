package com.memoryguard.app.ui.main

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Language
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.memoryguard.app.R
import com.memoryguard.app.data.model.GroupingStage
import com.memoryguard.app.localization.AppLanguage
import com.memoryguard.app.ui.components.DriveExplainerDialog
import com.memoryguard.app.ui.components.PermissionPromptCard
import com.memoryguard.app.ui.components.PhotoGroupCard

/**
 * Main screen: permission gate, scan action, loading states, grouped cards, Drive upload.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(
    uiState: MainUiState,
    onRequestPermission: () -> Unit,
    onScanPhotos: () -> Unit,
    onToggleLanguage: () -> Unit,
    onSaveToDrive: (String) -> Unit,
    onDriveExplainerConfirm: (String) -> Unit,
    onDriveExplainerDismiss: () -> Unit,
    onSafeToDelete: (String) -> Unit,
    onRetry: () -> Unit,
    onSnackbarShown: () -> Unit,
    modifier: Modifier = Modifier
) {
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(uiState.snackbarMessage) {
        val key = uiState.snackbarMessage ?: return@LaunchedEffect
        val message = when (key) {
            MainViewModel.SNACKBAR_MARKED_SAFE -> stringResource(R.string.marked_safe_to_delete)
            MainViewModel.SNACKBAR_DRIVE_SUCCESS -> stringResource(R.string.drive_upload_success)
            MainViewModel.SNACKBAR_DRIVE_FAILED -> stringResource(R.string.error_drive_upload)
            MainViewModel.SNACKBAR_DRIVE_SIGN_IN_FAILED -> stringResource(R.string.drive_sign_in_failed)
            else -> key
        }
        snackbarHostState.showSnackbar(message)
        onSnackbarShown()
    }

    val explainerGroup = uiState.driveExplainerGroupId?.let { id ->
        uiState.groups.find { it.id == id }
    }
    if (explainerGroup != null) {
        DriveExplainerDialog(
            categoryName = explainerGroup.categoryName,
            onConfirm = { onDriveExplainerConfirm(explainerGroup.id) },
            onDismiss = onDriveExplainerDismiss
        )
    }

    Scaffold(
        modifier = modifier.fillMaxSize(),
        containerColor = MaterialTheme.colorScheme.background,
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = stringResource(R.string.main_title),
                        style = MaterialTheme.typography.titleLarge
                    )
                },
                actions = {
                    IconButton(onClick = onToggleLanguage) {
                        Icon(
                            imageVector = Icons.Outlined.Language,
                            contentDescription = if (uiState.language == AppLanguage.ENGLISH) {
                                stringResource(R.string.language_toggle)
                            } else {
                                stringResource(R.string.language_toggle_en)
                            }
                        )
                    }
                    TextButton(onClick = onToggleLanguage) {
                        Text(
                            text = if (uiState.language == AppLanguage.ENGLISH) {
                                stringResource(R.string.language_toggle)
                            } else {
                                stringResource(R.string.language_toggle_en)
                            }
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background
                )
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Text(
                    text = stringResource(R.string.main_subtitle),
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Start
                )
            }

            if (!uiState.hasGalleryPermission) {
                item {
                    PermissionPromptCard(onRequestPermission = onRequestPermission)
                }
            } else {
                item {
                    ScanSection(
                        uiState = uiState,
                        onScanPhotos = onScanPhotos,
                        onRetry = onRetry
                    )
                }
            }

            if (uiState.isLoading) {
                item {
                    LoadingSection(stage = uiState.stage)
                }
            }

            if (uiState.showGroups) {
                item {
                    Text(
                        text = stringResource(R.string.groups_header),
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.padding(top = 8.dp)
                    )
                }
                items(uiState.groups, key = { it.id }) { group ->
                    PhotoGroupCard(
                        group = group,
                        driveUpload = uiState.driveUploadFor(group.id),
                        onSaveToDrive = { onSaveToDrive(group.id) },
                        onSafeToDelete = { onSafeToDelete(group.id) }
                    )
                }
            } else if (uiState.hasGalleryPermission && !uiState.isLoading && uiState.errorMessage == null) {
                item {
                    Text(
                        text = stringResource(R.string.no_groups_yet),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(vertical = 24.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun ScanSection(
    uiState: MainUiState,
    onScanPhotos: () -> Unit,
    onRetry: () -> Unit
) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Button(
            onClick = onScanPhotos,
            enabled = !uiState.isLoading,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            shape = RoundedCornerShape(16.dp)
        ) {
            Text(stringResource(R.string.scan_photos))
        }

        uiState.errorMessage?.let { message ->
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = message,
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodyMedium
            )
            TextButton(onClick = onRetry) {
                Text(stringResource(R.string.retry))
            }
        }
    }
}

@Composable
private fun LoadingSection(stage: GroupingStage) {
    val message = when (stage) {
        GroupingStage.SCANNING_GALLERY -> stringResource(R.string.scanning_photos)
        GroupingStage.PREPARING_THUMBNAILS,
        GroupingStage.ANALYZING_WITH_AI -> stringResource(R.string.analyzing_photos)
        else -> stringResource(R.string.scanning_photos)
    }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 32.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = message,
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
