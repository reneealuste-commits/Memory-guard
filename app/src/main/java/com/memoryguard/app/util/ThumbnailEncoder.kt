package com.memoryguard.app.util

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.ByteArrayOutputStream
import kotlin.math.max

/**
 * Downscales gallery images for vision API requests to reduce bandwidth and token usage.
 */
object ThumbnailEncoder {

    private const val MAX_EDGE_PX = 384
    private const val JPEG_QUALITY = 72

    suspend fun encodeJpegThumbnail(
        context: Context,
        uri: Uri,
        maxEdgePx: Int = MAX_EDGE_PX
    ): ByteArray? = withContext(Dispatchers.IO) {
        runCatching {
            context.contentResolver.openInputStream(uri)?.use { input ->
                val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
                BitmapFactory.decodeStream(input, null, bounds)
                val sampleSize = calculateInSampleSize(bounds.outWidth, bounds.outHeight, maxEdgePx)
                val decodeOptions = BitmapFactory.Options().apply { inSampleSize = sampleSize }
                context.contentResolver.openInputStream(uri)?.use { stream ->
                    val bitmap = BitmapFactory.decodeStream(stream, null, decodeOptions)
                        ?: return@withContext null
                    val scaled = scaleDown(bitmap, maxEdgePx)
                    if (scaled !== bitmap) bitmap.recycle()
                    ByteArrayOutputStream().use { output ->
                        scaled.compress(Bitmap.CompressFormat.JPEG, JPEG_QUALITY, output)
                        scaled.recycle()
                        output.toByteArray()
                    }
                }
            }
        }.getOrNull()
    }

    private fun calculateInSampleSize(width: Int, height: Int, maxEdge: Int): Int {
        var inSampleSize = 1
        val longest = max(width, height)
        while (longest / inSampleSize > maxEdge * 2) {
            inSampleSize *= 2
        }
        return inSampleSize
    }

    private fun scaleDown(source: Bitmap, maxEdge: Int): Bitmap {
        val width = source.width
        val height = source.height
        val longest = max(width, height)
        if (longest <= maxEdge) return source
        val scale = maxEdge.toFloat() / longest
        val targetW = (width * scale).toInt().coerceAtLeast(1)
        val targetH = (height * scale).toInt().coerceAtLeast(1)
        return Bitmap.createScaledBitmap(source, targetW, targetH, true)
    }
}
