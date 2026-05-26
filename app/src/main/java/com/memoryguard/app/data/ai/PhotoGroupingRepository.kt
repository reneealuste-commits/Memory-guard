package com.memoryguard.app.data.ai

import android.content.Context
import com.memoryguard.app.BuildConfig
import com.memoryguard.app.data.gallery.GalleryRepository
import com.memoryguard.app.data.model.GroupingStage
import com.memoryguard.app.data.model.PhotoGroup
import com.memoryguard.app.data.model.PhotoItem
import com.memoryguard.app.util.ThumbnailEncoder
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * Orchestrates gallery scan, thumbnail preparation, and AI grouping.
 */
class PhotoGroupingRepository(
    context: Context,
    private val galleryRepository: GalleryRepository = GalleryRepository(context),
    private val photoGrouper: PhotoGrouper = createGrouperFromBuildConfig()
) {
    private val appContext = context.applicationContext

    private val _stage = MutableStateFlow(GroupingStage.IDLE)
    val stage: StateFlow<GroupingStage> = _stage.asStateFlow()

    suspend fun scanAndGroup(): Result<ScanAndGroupResult> = runCatching {
        _stage.value = GroupingStage.SCANNING_GALLERY
        val photos = galleryRepository.loadRecentPhotos()

        _stage.value = GroupingStage.PREPARING_THUMBNAILS
        val thumbnails = buildThumbnails(photos)

        _stage.value = GroupingStage.ANALYZING_WITH_AI
        val groups = photoGrouper.groupPhotos(photos, thumbnails)

        _stage.value = GroupingStage.DONE
        ScanAndGroupResult(photos = photos, groups = groups)
    }.also { result ->
        if (result.isFailure) {
            _stage.value = GroupingStage.IDLE
        }
    }

    fun resetStage() {
        _stage.value = GroupingStage.IDLE
    }

    private suspend fun buildThumbnails(photos: List<PhotoItem>): Map<Long, ByteArray> {
        val map = linkedMapOf<Long, ByteArray>()
        photos.forEach { photo ->
            ThumbnailEncoder.encodeJpegThumbnail(appContext, photo.uri)?.let { bytes ->
                map[photo.id] = bytes
            }
        }
        return map
    }

    data class ScanAndGroupResult(
        val photos: List<PhotoItem>,
        val groups: List<PhotoGroup>
    )

    companion object {
        fun createGrouperFromBuildConfig(): PhotoGrouper {
            val provider = BuildConfig.AI_PROVIDER.lowercase()
            return when {
                provider == "openai" && BuildConfig.OPENAI_API_KEY.isNotBlank() ->
                    OpenAiPhotoGrouper(BuildConfig.OPENAI_API_KEY)
                BuildConfig.GEMINI_API_KEY.isNotBlank() ->
                    GeminiPhotoGrouper(BuildConfig.GEMINI_API_KEY)
                BuildConfig.OPENAI_API_KEY.isNotBlank() ->
                    OpenAiPhotoGrouper(BuildConfig.OPENAI_API_KEY)
                else -> LocalFallbackGrouper()
            }
        }
    }
}
