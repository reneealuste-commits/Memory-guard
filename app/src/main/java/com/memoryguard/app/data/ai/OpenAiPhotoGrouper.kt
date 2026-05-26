package com.memoryguard.app.data.ai

import android.util.Base64
import com.memoryguard.app.data.model.PhotoGroup
import com.memoryguard.app.data.model.PhotoItem
import com.squareup.moshi.Moshi
import com.squareup.moshi.Types
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.UUID
import java.util.concurrent.TimeUnit

/**
 * Groups photos using OpenAI GPT-4o vision (chat completions API).
 */
class OpenAiPhotoGrouper(
    private val apiKey: String,
    private val model: String = "gpt-4o"
) : PhotoGrouper {

    private val client = OkHttpClient.Builder()
        .connectTimeout(60, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .build()

    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    private val groupListType = Types.newParameterizedType(List::class.java, AiGroupDto::class.java)
    private val groupListAdapter = moshi.adapter<List<AiGroupDto>>(groupListType)

    override suspend fun groupPhotos(
        photos: List<PhotoItem>,
        thumbnailsByPhotoId: Map<Long, ByteArray>
    ): List<PhotoGroup> = withContext(Dispatchers.IO) {
        if (photos.isEmpty()) return@withContext emptyList()

        val allGroups = mutableListOf<PhotoGroup>()
        photos.chunked(BATCH_SIZE).forEach { batch ->
            allGroups += analyzeBatch(batch, thumbnailsByPhotoId)
        }
        mergeGroupsByCategory(allGroups)
    }

    private fun analyzeBatch(
        batch: List<PhotoItem>,
        thumbnails: Map<Long, ByteArray>
    ): List<PhotoGroup> {
        val content = JSONArray()
        content.put(
            JSONObject().put(
                "type",
                "text"
            ).put(
                "text",
                """
                Organize these phone photos (indices 0-${batch.lastIndex}) into meaningful groups.
                Categories examples: Kids, Family Trips, Friends, Events, Random Items.
                Return ONLY a JSON array:
                [{"categoryName":"...","description":"...","photoIndices":[0]}]
                """.trimIndent()
            )
        )

        batch.forEachIndexed { index, photo ->
            val bytes = thumbnails[photo.id] ?: return@forEachIndexed
            val base64 = Base64.encodeToString(bytes, Base64.NO_WRAP)
            content.put(
                JSONObject()
                    .put("type", "text")
                    .put("text", "Photo index $index.")
            )
            content.put(
                JSONObject()
                    .put("type", "image_url")
                    .put(
                        "image_url",
                        JSONObject().put(
                            "url",
                            "data:image/jpeg;base64,$base64"
                        )
                    )
            )
        }

        val body = JSONObject()
            .put("model", model)
            .put(
                "messages",
                JSONArray().put(
                    JSONObject()
                        .put("role", "user")
                        .put("content", content)
                )
            )
            .put("max_tokens", 2048)
            .put("temperature", 0.2)

        val request = Request.Builder()
            .url("https://api.openai.com/v1/chat/completions")
            .addHeader("Authorization", "Bearer $apiKey")
            .post(body.toString().toRequestBody(JSON_MEDIA))
            .build()

        val response = client.newCall(request).execute()
        val responseBody = response.body?.string()
            ?: throw IllegalStateException("Empty OpenAI response")
        if (!response.isSuccessful) {
            throw IllegalStateException("OpenAI error ${response.code}: $responseBody")
        }

        val text = JSONObject(responseBody)
            .getJSONArray("choices")
            .getJSONObject(0)
            .getJSONObject("message")
            .getString("content")

        val dtos = parseGroupJson(text)
        return dtos.mapNotNull { dto ->
            val ids = dto.photoIndices.mapNotNull { idx -> batch.getOrNull(idx)?.id }
            if (ids.isEmpty()) return@mapNotNull null
            PhotoGroup(
                id = UUID.randomUUID().toString(),
                categoryName = dto.categoryName.trim(),
                photoCount = ids.size,
                thumbnailUri = batch.firstOrNull { it.id == ids.first() }?.uri,
                description = dto.description.trim(),
                photoIds = ids
            )
        }
    }

    private fun parseGroupJson(raw: String): List<AiGroupDto> {
        val start = raw.indexOf('[')
        val end = raw.lastIndexOf(']')
        val json = if (start >= 0 && end > start) raw.substring(start, end + 1) else raw.trim()
        return groupListAdapter.fromJson(json)
            ?: throw IllegalStateException("Could not parse AI grouping JSON")
    }

    private fun mergeGroupsByCategory(groups: List<PhotoGroup>): List<PhotoGroup> {
        val merged = linkedMapOf<String, PhotoGroup>()
        groups.forEach { group ->
            val key = group.categoryName.lowercase()
            val existing = merged[key]
            if (existing == null) {
                merged[key] = group
            } else {
                val combinedIds = (existing.photoIds + group.photoIds).distinct()
                merged[key] = existing.copy(
                    photoCount = combinedIds.size,
                    photoIds = combinedIds,
                    thumbnailUri = existing.thumbnailUri ?: group.thumbnailUri
                )
            }
        }
        return merged.values.toList()
    }

    companion object {
        private const val BATCH_SIZE = 10
        private val JSON_MEDIA = "application/json".toMediaType()
    }
}
