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
 * Groups photos using Google Gemini vision (generateContent API).
 */
class GeminiPhotoGrouper(
    private val apiKey: String,
    private val model: String = "gemini-2.0-flash"
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
            val batchGroups = analyzeBatch(batch, thumbnailsByPhotoId)
            allGroups += batchGroups
        }
        mergeGroupsByCategory(allGroups)
    }

    private fun analyzeBatch(
        batch: List<PhotoItem>,
        thumbnails: Map<Long, ByteArray>
    ): List<PhotoGroup> {
        val parts = JSONArray()
        parts.put(
            JSONObject().put(
                "text",
                """
                You are organizing a user's phone photo gallery into warm, meaningful groups.
                Look at each image (index 0 to ${batch.lastIndex}) and assign every index to exactly one group.
                Use category names like: Kids, Family Trips, Friends, Events, Random Items, Pets, Food, Nature.
                Reply with ONLY a JSON array (no markdown), each element:
                {"categoryName":"...","description":"Short friendly sentence.","photoIndices":[0,1]}
                """.trimIndent()
            )
        )

        batch.forEachIndexed { index, photo ->
            val bytes = thumbnails[photo.id] ?: return@forEachIndexed
            val base64 = Base64.encodeToString(bytes, Base64.NO_WRAP)
            parts.put(
                JSONObject().put(
                    "inline_data",
                    JSONObject()
                        .put("mime_type", "image/jpeg")
                        .put("data", base64)
                )
            )
            // Help the model track indices (lightweight text part between images).
            if (index < batch.lastIndex) {
                parts.put(JSONObject().put("text", "Image index $index."))
            }
        }

        val body = JSONObject()
            .put(
                "contents",
                JSONArray().put(JSONObject().put("parts", parts))
            )
            .put(
                "generationConfig",
                JSONObject().put("temperature", 0.2).put("maxOutputTokens", 2048)
            )

        val url =
            "https://generativelanguage.googleapis.com/v1beta/models/$model:generateContent?key=$apiKey"
        val request = Request.Builder()
            .url(url)
            .post(body.toString().toRequestBody(JSON_MEDIA))
            .build()

        val response = client.newCall(request).execute()
        val responseBody = response.body?.string()
            ?: throw IllegalStateException("Empty Gemini response")
        if (!response.isSuccessful) {
            throw IllegalStateException("Gemini error ${response.code}: $responseBody")
        }

        val text = extractTextFromGeminiResponse(responseBody)
        val dtos = parseGroupJson(text)
        return dtos.mapNotNull { dto ->
            val ids = dto.photoIndices.mapNotNull { idx ->
                batch.getOrNull(idx)?.id
            }
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

    private fun extractTextFromGeminiResponse(json: String): String {
        val root = JSONObject(json)
        val candidates = root.optJSONArray("candidates") ?: return ""
        if (candidates.length() == 0) return ""
        val content = candidates.getJSONObject(0).optJSONObject("content") ?: return ""
        val parts = content.optJSONArray("parts") ?: return ""
        val builder = StringBuilder()
        for (i in 0 until parts.length()) {
            val part = parts.getJSONObject(i)
            if (part.has("text")) builder.append(part.getString("text"))
        }
        return builder.toString()
    }

    private fun parseGroupJson(raw: String): List<AiGroupDto> {
        val json = extractJsonArray(raw)
        return groupListAdapter.fromJson(json)
            ?: throw IllegalStateException("Could not parse AI grouping JSON")
    }

    private fun extractJsonArray(text: String): String {
        val start = text.indexOf('[')
        val end = text.lastIndexOf(']')
        if (start >= 0 && end > start) return text.substring(start, end + 1)
        return text.trim()
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
                    thumbnailUri = existing.thumbnailUri ?: group.thumbnailUri,
                    description = existing.description.ifBlank { group.description }
                )
            }
        }
        return merged.values.toList()
    }

    companion object {
        private const val BATCH_SIZE = 12
        private val JSON_MEDIA = "application/json".toMediaType()
    }
}
