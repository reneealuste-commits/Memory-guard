package com.memoryguard.app.localization

/**
 * Supported UI languages. Estonian is offered as a secondary option alongside English.
 */
enum class AppLanguage(val tag: String) {
    ENGLISH("en"),
    ESTONIAN("et");

    fun toggle(): AppLanguage = if (this == ENGLISH) ESTONIAN else ENGLISH
}
