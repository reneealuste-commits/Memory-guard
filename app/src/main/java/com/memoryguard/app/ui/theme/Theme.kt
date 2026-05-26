package com.memoryguard.app.ui.theme

import android.app.Activity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val LightColorScheme = lightColorScheme(
    primary = WarmTerracotta,
    onPrimary = WarmCream,
    primaryContainer = WarmPeach,
    onPrimaryContainer = WarmBrown,
    secondary = WarmGreen,
    onSecondary = WarmCream,
    tertiary = WarmRose,
    background = WarmCream,
    onBackground = WarmBrown,
    surface = WarmSand,
    onSurface = WarmBrown,
    surfaceVariant = WarmPeach,
    onSurfaceVariant = WarmBrownMuted,
    outline = WarmPeach
)

private val DarkColorScheme = darkColorScheme(
    primary = WarmPeach,
    onPrimary = WarmBrown,
    primaryContainer = WarmTerracotta,
    onPrimaryContainer = WarmCream,
    secondary = WarmGreen,
    background = WarmBrown,
    onBackground = WarmCream,
    surface = WarmBrownMuted,
    onSurface = WarmCream
)

@Composable
fun MemoryGuardTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.background.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = MemoryGuardTypography,
        content = content
    )
}
