package com.memoryguard.app.data.ai

import com.squareup.moshi.Json

/**
 * JSON schema returned by vision models for photo categorization.
 */
data class AiGroupDto(
  @Json(name = "categoryName") val categoryName: String,
  @Json(name = "description") val description: String,
  @Json(name = "photoIndices") val photoIndices: List<Int>
)
