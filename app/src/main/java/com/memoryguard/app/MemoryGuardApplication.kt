package com.memoryguard.app

import android.app.Application
import com.memoryguard.app.localization.AppLanguage
import com.memoryguard.app.localization.LanguagePreferences
import com.memoryguard.app.localization.LocaleContextWrapper

/**
 * Application entry point — applies saved locale before any Activity starts.
 */
class MemoryGuardApplication : Application() {

    override fun onCreate() {
        super.onCreate()
        val language = LanguagePreferences(this).getLanguage()
        applyLocale(language)
    }

    fun applyLocale(language: AppLanguage) {
        val wrapped = LocaleContextWrapper.wrap(this, language)
        resources.updateConfiguration(wrapped.resources.configuration, resources.displayMetrics)
    }
}
