# Grok Imagine — Cover Prompts

**Series:** The Unplugged Man by The Unplugged Al  
**Aspect ratio:** 2:3 vertical (1600×2560)  
**Style for all prompts:** Cinematic, premium editorial book cover photography. Moody atmospheric lighting. Subtle film grain. No text in image — leave clean dark space in top 40% for typography overlay. No faces. No women. Masculine but not aggressive. High-end publishing quality.

---

## Book 1: Frame First

**Subtitle:** How to hold your ground when she tests you, gets emotional, or tries to pull you off mission.

```
Premium book cover background, vertical 2:3 ratio. A single weathered stone pillar or column standing firm in dark fog, shot from low angle. Charcoal and deep navy gradient sky. Warm bronze light hitting one edge of the stone. Symbol of unshakeable structure and grounded strength. Cinematic moody atmosphere, shallow depth of field, subtle film grain. Empty dark negative space in upper third for title text. No people, no faces, no text, no logos. Editorial nonfiction aesthetic, high-end masculine self-development book cover art, photorealistic, 8k quality.
```

**Alt prompt (minimal):**
```
Minimalist premium book cover art. One solid bronze geometric frame or doorframe standing alone in dark charcoal void. Single dramatic side light. Massive empty dark space at top for typography. Cinematic, elegant, masculine, no people, no text.
```

---

## Book 2: Vetting Her

**Subtitle:** How to see who she really is before you give her your time, heart, or resources.

```
Premium book cover background, vertical 2:3 ratio. Close-up of a man's hand holding a vintage brass magnifying glass over a blurred warm light source, shot in dramatic chiaroscuro lighting. Dark charcoal and navy background. The glass is sharp, everything else softly out of focus — symbol of clarity and discernment. Bronze and gold light reflections. Cinematic editorial photography style, subtle grain. Large empty dark space in upper third for title overlay. No faces visible, no text, no logos. High-end nonfiction book cover.
```

**Alt prompt:**
```
Premium book cover. A clear glass prism refracting a single beam of warm gold light into sharp lines against a dark navy background. Symbol of seeing truth clearly. Cinematic, minimal, masculine editorial style. Empty dark top third. No people, no text.
```

---

## Book 3: Stop Simping

**Subtitle:** Why you keep over-investing, pedestalizing, and choosing the same pain — and how to finally stop.

```
Premium book cover background, vertical 2:3 ratio. A marble pedestal or column cracked down the middle, one half fallen, shot in dark moody studio lighting. Charcoal black environment with single bronze spotlight. Symbol of breaking the habit of putting others above yourself. Cinematic dramatic shadows, editorial nonfiction aesthetic, subtle film grain. Empty dark negative space in upper 40% for title text. No people, no faces, no text. Photorealistic high-end book cover art.
```

**Alt prompt:**
```
Premium book cover. A thick iron chain lying broken on dark wet stone floor, single warm light from above. Symbol of freedom from old patterns. Cinematic, moody, masculine. Empty dark space at top. No people, no text.
```

---

## Book 4: Male Space

**Subtitle:** Why you need other men and a mission bigger than any woman.

```
Premium book cover background, vertical 2:3 ratio. Two worn leather chairs angled toward each other beside a dark wooden table with a single dim lamp, empty room, shot in cinematic low-key lighting. Deep navy and charcoal tones with warm bronze lamp glow. Symbol of brotherhood, male friendship, and private honest conversation. No people in frame. Atmospheric, intimate, editorial quality. Large empty dark space in upper third for typography. No text, no logos. High-end masculine self-help book cover.
```

**Alt prompt:**
```
Premium book cover. A compass resting on a rugged map on a dark wooden desk, warm side lighting, navy shadows. Symbol of mission and direction. Cinematic editorial style. Empty dark top third. No people, no text.
```

---

## Book 5: Money & Women

**Subtitle:** How to protect your resources without becoming stingy or paranoid.

```
Premium book cover background, vertical 2:3 ratio. A solid vault door slightly ajar with warm gold light spilling through the crack, dark charcoal environment. Shot in cinematic dramatic lighting with bronze highlights on metal texture. Symbol of protected resources and financial boundaries. Moody, premium, editorial nonfiction aesthetic. Subtle film grain. Empty dark space in upper 40% for title overlay. No people, no faces, no text, no logos. Photorealistic 8k book cover art.
```

**Alt prompt:**
```
Premium book cover. A balanced brass scale on a dark marble surface, one side glowing warm gold, perfect equilibrium, dramatic side lighting. Symbol of generosity with standards. Cinematic, masculine, editorial. Empty dark top. No people, no text.
```

---

## Book 6: The Unplugged Man's Code

**Subtitle:** The final principles for self-respect, strong relationships, and peace.

```
Premium book cover background, vertical 2:3 ratio. A lone figure silhouette from behind standing at a cliff edge looking at a vast pre-dawn horizon, sky transitioning from deep navy to warm bronze gold at the horizon line. Cinematic epic atmosphere, sense of arrival and clarity after a long journey. Not heroic pose — calm, grounded, contemplative. Subtle film grain, editorial nonfiction capstone aesthetic. Large empty dark space in upper third for title text. No identifiable face, no text, no logos. Highest quality photorealistic book cover art.
```

**Alt prompt:**
```
Premium book cover. An open ancient book with blank glowing pages on a dark stone surface, warm bronze light rising from the pages. Symbol of the final code and inner clarity. Cinematic, reverent, masculine. Empty dark top third. No people, no text.
```

---

## Series Box Set (optional bonus cover)

```
Premium book cover, vertical 2:3. Six thin book spines arranged in a slight fan on dark charcoal surface, each spine a different shade of navy with thin bronze lines, warm dramatic side lighting. Symbol of complete series. Cinematic editorial product photography. Empty dark space in upper half for series title. No text in image, no logos. Ultra high-end publishing aesthetic.
```

---

## Grok Imagine Tips

1. Run each prompt **2–3 times** — pick the cleanest negative space at top.
2. If Grok adds text, regenerate with: `no text, no words, no letters, no typography`
3. Import winning image into **Canva** (1600×2560 template).
4. Apply typography from `BRAND_GUIDE.md`.
5. Export PNG and upload to KDP.

## Adding Covers to EPUBs

After saving covers as `cover.jpg` in each book folder:

```yaml
# book.yaml
cover: cover.jpg
```

Then rebuild:

```bash
ebook-factory build books/the-unplugged-al/01-frame-first
```
