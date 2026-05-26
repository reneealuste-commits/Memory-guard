package com.memoryguard.app.data.model

/**
 * Stages shown on the main screen while photos are being processed.
 */
enum class GroupingStage {
    IDLE,
    SCANNING_GALLERY,
    PREPARING_THUMBNAILS,
    ANALYZING_WITH_AI,
    DONE
}
