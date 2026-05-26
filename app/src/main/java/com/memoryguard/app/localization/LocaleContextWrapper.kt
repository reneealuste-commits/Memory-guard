package com.memoryguard.app.localization

import android.content.Context
import android.content.res.Configuration
import java.util.Locale

/**
 * Applies a locale override so [stringResource] and XML strings resolve correctly.
 */
object LocaleContextWrapper {

    fun wrap(context: Context, language: AppLanguage): Context {
        val locale = Locale.forLanguageTag(language.tag)
        Locale.setDefault(locale)
        val config = Configuration(context.resources.configuration)
        config.setLocale(locale)
        return context.createConfigurationContext(config)
    }
}
