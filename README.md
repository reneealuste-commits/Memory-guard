# Memory Guard

A clean Android app built with **Kotlin** and **Jetpack Compose** that helps you organize phone photos, back up important groups to Google Drive, and safely free up storage.

This iteration implements the **main screen**: gallery permission flow, recent photo scanning, and AI-powered grouping (Gemini or GPT-4o vision), with a warm Material 3 UI and **English / Estonian** language toggle.

## Features (current)

- Request `READ_MEDIA_IMAGES` (Android 13+) or legacy storage permission
- Scan the most recent gallery photos via MediaStore
- Group photos with **Gemini** or **GPT-4o** vision APIs (configurable)
- Offline **month-based fallback** when no API key is set (for local development)
- Material 3 UI with grouped cards: category, count, thumbnail, description
- Placeholder actions: **Save to Google Drive** and **Safe to Delete** (wired in UI, full flow coming next)
- Secondary language: **Estonian** (`values-et`)

## Requirements

- Android Studio Ladybug or newer
- JDK 17+
- Android SDK 35
- A device or emulator running **API 26+**

## Setup

1. Clone the repository and open it in Android Studio.
2. Copy `local.properties.example` to `local.properties` and set your SDK path:

   ```properties
   sdk.dir=/Users/you/Library/Android/sdk
   ```

3. Add a vision API key (optional for UI testing — fallback grouping works without a key):

   ```properties
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_key_here
   # or
   AI_PROVIDER=openai
   OPENAI_API_KEY=your_key_here
   ```

4. Run the **app** configuration on a device with photos in the gallery.

## Project structure

```
app/src/main/java/com/memoryguard/app/
├── data/
│   ├── ai/          # Gemini, OpenAI, fallback grouping
│   ├── gallery/     # MediaStore scanner
│   └── model/       # PhotoItem, PhotoGroup
├── localization/    # EN / ET preferences & locale wrapper
├── ui/
│   ├── components/  # PhotoGroupCard, PermissionPromptCard
│   ├── main/        # MainScreen, MainViewModel
│   └── theme/       # Material 3 warm palette
├── util/            # Permissions, thumbnail encoding
└── MainActivity.kt
```

## Extending the app

Planned next steps (hooks are already in the UI):

- Google Sign-In + Drive folder creation and upload
- Completion screen after backup
- Actual safe-delete flow (MediaStore delete / user confirmation)

## License

MIT (add your preferred license as needed).
