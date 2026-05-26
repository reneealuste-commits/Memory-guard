package com.memoryguard.app.localization

import android.content.Context

/**
 * Persists the user's language choice across app restarts.
 */
class LanguagePreferences(context: Context) {

    private val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun getLanguage(): AppLanguage {
        val tag = prefs.getString(KEY_LANGUAGE, AppLanguage.ENGLISH.tag)
        return AppLanguage.entries.firstOrNull { it.tag == tag } ?: AppLanguage.ENGLISH
    }

    fun setLanguage(language: AppLanguage) {
        prefs.edit().putString(KEY_LANGUAGE, language.tag).apply()
    }

    companion object {
        private const val PREFS_NAME = "memory_guard_prefs"
        private const val KEY_LANGUAGE = "app_language"
    }
}
