---
name: gemini-image-gen
description: Generate images with Google Gemini 3 Pro Image. Use when writing image prompts, setting up the Gemini image generation API, troubleshooting generation failures, or building prompt-as-file workflows.
---

# Gemini Image Generation

Generate high-quality images using Google Gemini 3 Pro Image (`gemini-3-pro-image-preview`). This skill covers API setup, prompt engineering for image generation, aspect ratio selection, batch workflows, and failure mitigation.

## When to Use

- Writing image prompts for Gemini 3 Pro Image
- Setting up a Python script to call the Gemini image generation API
- Debugging 503 errors, text rendering issues, or quota problems
- Building a prompt-as-file workflow for batch image generation
- Choosing aspect ratios and resolutions for specific use cases

## Model Reference

| Property | Value |
|---|---|
| Model ID | `gemini-3-pro-image-preview` |
| SDK | `google-genai` Python package |
| Install | `uv add google-genai` |
| Cost (3 Pro) | ~$0.13/image |
| Cost (2.5 Flash) | ~$0.04/image (lower quality) |
| Free Tier Quota | **Zero** -- billing MUST be enabled |

### Supported Aspect Ratios

`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### Supported Resolutions

`1K`, `2K`, `4K` -- uppercase K required (lowercase fails silently)

### 4K Dimensions by Aspect Ratio

| Aspect Ratio | Dimensions | Print Size (300 DPI) |
|---|---|---|
| 16:9 | 5504x3072 | ~18x10 in |
| 9:16 | 3072x5504 | ~10x18 in |
| 1:1 | ~4096x4096 | ~14x14 in |

## API Setup

### Minimal Working Example

```python
from google import genai
from google.genai import types
from pathlib import Path

MODEL = "gemini-3-pro-image-preview"

client = genai.Client(api_key="YOUR_API_KEY")  # or GOOGLE_API_KEY env var

config = types.GenerateContentConfig(
    response_modalities=["IMAGE"],
    image_config=types.ImageConfig(
        aspect_ratio="16:9",
        image_size="2K",
    ),
)

response = client.models.generate_content(
    model=MODEL,
    contents=prompt_text,
    config=config,
)

for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save(str(Path("output.png")))
```

### Configuration Notes

- `response_modalities` MUST be `["IMAGE"]` for image output
- `aspect_ratio` accepts any supported ratio string (e.g., `"16:9"`)
- `image_size` accepts `"1K"`, `"2K"`, or `"4K"` -- uppercase K required
- Billing MUST be enabled on the Google Cloud project -- free tier has zero image quota

## Prompt Engineering

### Core Principle: Essays, Not Tag Lists

Write 300-500 word prose descriptions. The model responds to narrative context far better than comma-separated keywords. Think of it as writing a scene for a cinematographer, not filing metadata.

### Structured Prompt Flow

Organize prompts in this order for best results:

1. **Subject** -- who or what is the focal point, with exact position and materials
2. **Environment** -- setting, background, spatial relationships
3. **Secondary elements** -- supporting objects, atmospheric effects
4. **Lighting** -- direction, color temperature, time of day
5. **Mood** -- emotional tone, atmosphere (build implicitly through prior sections)
6. **Style** -- medium, color constraints, texture, camera/lens, artistic reference

Use `###` markdown headers to separate sections. Both humans and the model benefit from structural markers.

### Hyper-Specificity Wins

| Weak | Strong |
|---|---|
| "fantasy armor" | "ornate elven plate armor, etched with silver leaf patterns" |
| "vintage car" | "1950s American sedan -- rounded fenders, chrome bumper" |
| "night sky" | "deep indigo sky scattered with cold white pinprick stars" |
| "old building" | "crumbling limestone facade with iron balconets, moss in the mortar joints" |

Every vague noun is a coin flip. Every specific detail is a constraint the model can honor.

### Positive Descriptions Over Exclusion Lists

Describe what SHOULD be in the image rather than listing what should not. The model interprets positive instructions more reliably than negatives.

**Mandatory exception:** Always include `No text anywhere in the image.` as the final line. Text rendering is unreliable and this directive consistently suppresses garbled lettering.

### Spatial Anchoring

Place elements using concrete spatial language:

- **Grid positions**: "lower-right third," "upper-left quadrant," "center-frame"
- **Relative placement**: "behind and to the left," "extending from edge to edge"
- **Scale relationships**: "disproportionately large," "tiny against the horizon"
- **Depth planes**: "foreground," "middle ground," "far distance"

Vague spatial language ("in the scene," "nearby") produces vague compositions. Be a set designer, not a narrator.

### Color Strategy

Define a constrained palette and assign roles:

- **Warm isolation**: Reserve one warm color for the emotional anchor. Everything else stays cool (or vice versa). A single warm element in a cool scene draws the eye like a campfire in the dark
- **Layer order**: Describe which colors print on top of which (matters for screen-print and layered styles)
- **Limit**: 4-6 colors maximum. More colors = less cohesion

### The Subject Rule

One primary subject per image. If there are two figures, one leads. If there's a landscape and a figure, decide which dominates. Every element should serve the subject -- supporting it spatially, tonally, or narratively.

### Physical Metaphors Beat Abstract Concepts

Describe tangible, visible qualities rather than abstract feelings. "Warm golden light pooling on weathered wood" lands. "A sense of nostalgia" does not.

### Containment Language Prevents Edge Bleed

When visual effects (glow, smoke, light rays) should stay within the composition, explicitly describe containment boundaries. Without this, effects bleed to frame edges and overwhelm the subject.

## Style Specification

The Style section is the technical contract with the model. Include:

1. **Medium**: What this image looks like physically (screen-print, oil painting, photograph, patent drawing)
2. **Color constraints**: Exact palette, number of layers/inks
3. **Texture**: Halftone grain, paper stock, film grain, brush strokes -- where and how heavy
4. **Imperfections**: Misregistration, foxing, scratches, light leaks. Perfect images feel sterile
5. **Mood summary**: 3-5 evocative words capturing the emotional target
6. **Exclusions**: "No text anywhere in the image" (always include this)

### Style Archetypes

**Screen-print poster**

- Flat color separation, distinct ink layers
- Visible halftone dot grain (specify WHERE it's heaviest)
- Paper stock texture showing through
- Slight ink misregistration between layers
- Bold, graphic, high-contrast

**Cinematic matte painting**

- 35mm film grain
- Photorealistic lighting with painterly atmosphere
- Deep depth of field or selective focus
- Color grading (specify warm/cool, lifted blacks, etc.)

**Vintage document**

- Aged paper with foxing stains, fold creases, fiber texture
- Period-appropriate rendering (ink, watercolor, pencil)
- Institutional formatting (seals, stamps, margins)
- Looks like a photograph of a real physical object

**Illustration / editorial**

- Clean linework or defined shapes
- Limited palette, often with one accent color
- Graphic composition, strong silhouettes
- Can evoke specific decades (1960s travel poster, 1920s deco)

## Mood Through Specifics

Mood emerges from specific choices, not adjectives:

| Mood | How to achieve it |
|---|---|
| Lonesome | Single subject, vast negative space, cool palette, distant horizon |
| Ominous | Low angle, heavy darks, subject backlit or partially obscured |
| Tender | Close framing, warm light, soft edges, intimate scale |
| Epic | Wide aspect ratio, dramatic sky, small figure against large landscape |
| Uncanny | Familiar scene with one wrong element (reversed shadow, missing reflection) |

State the mood explicitly in the Style section, but build it implicitly through every preceding section.

## Aspect Ratio as Storytelling

Aspect ratio drives composition and narrative -- it is not just a technical setting.

| Ratio | Use Case | Example |
|---|---|---|
| 16:9 | Wide landscapes, cinematic establishing shots | Campfire panoramas, desert highway vistas |
| 3:4 | Portraits, character studies, detailed objects | Patent drawings, character concepts |
| 1:1 | Symmetrical compositions, contained scenes | Emblems, face-to-face encounters |
| 9:16 | Phone wallpapers, tall/vertical drama | Towers, waterfalls, vertical compositions |
| 21:9 | Ultra-wide cinematic, banner images | Epic landscapes, film-style frames |

**Critical: 9:16 requires full recomposition.** Simply cropping a 16:9 prompt produces unusable results. Write a dedicated prompt that places subject and environment within the vertical frame from the start.

## Pre-Flight Validation

Image generation is an **expensive** cost tier (~$0.13/call). Every call MUST pass a quality gate before hitting the API. A bad prompt produces a bad image and wastes real money.

### Validation Checklist

Before sending a prompt to Gemini, verify:

| Check | Rule | Why |
|---|---|---|
| Non-empty body | Prompt body has content after frontmatter split | Empty string = $0.13 for nothing |
| Minimum length | At least 50 words | Short prompts produce generic, unusable images |
| Quality floor | At least 150 words for production images | 300-500 words is the sweet spot; under 150 lacks the specificity that makes generation worthwhile |
| Has subject | First section describes a concrete visual subject | Abstract prompts ("a feeling of hope") produce garbage |
| No contradictions | No opposing directives ("vibrant and muted", "minimal and detailed") | Model picks one randomly, wastes the call |
| Style specified | Prompt includes medium, palette, or texture language | Without style, output is generic stock-photo aesthetic |
| Frontmatter valid | `aspect_ratio` is a supported value, `resolution` is `1K`/`2K`/`4K` | Invalid config = API error = wasted call |

### Script-Level Validation

Add this before the API call in generation scripts:

```python
def validate_prompt(body: str, frontmatter: dict) -> list[str]:
    """Pre-flight check before expensive image generation."""
    errors = []
    words = body.split()

    if not body.strip():
        errors.append("Empty prompt body -- refusing to send")
    elif len(words) < 50:
        errors.append(f"Prompt too short ({len(words)} words, minimum 50)")

    if len(words) < 150:
        errors.append(f"Warning: prompt is {len(words)} words (recommend 300-500 for best results)")

    valid_ratios = {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"}
    ratio = frontmatter.get("aspect_ratio", "")
    if ratio and ratio not in valid_ratios:
        errors.append(f"Invalid aspect_ratio '{ratio}' -- must be one of {valid_ratios}")

    valid_sizes = {"1K", "2K", "4K"}
    size = frontmatter.get("resolution", "")
    if size and size not in valid_sizes:
        errors.append(f"Invalid resolution '{size}' -- must be one of {valid_sizes} (uppercase K)")

    return errors
```

Errors are hard stops. Warnings print but proceed. Integrate this into the `generate()` function before the API call.

## Workflow: Prompt-as-File Architecture

For projects generating multiple images, use a file-based workflow:

### Prompt File Format

```yaml
---
name: kebab-case-name
aspect_ratio: '16:9'
resolution: 2K
style: screen-print-poster
last_generated: null
last_updated: '2026-01-15T12:00:00Z'
---

### Subject
[300-500 word prompt body organized with ### headers]

### Environment
...

### Style
...

No text anywhere in the image.
```

### Generation Script Pattern

```python
import sys
import time
import yaml
from pathlib import Path
from datetime import datetime

from google import genai
from google.genai import types

MODEL = "gemini-3-pro-image-preview"
PROMPT_DIR = Path("prompts")
OUTPUT_DIR = Path("output")
MAX_RETRIES = 3

client = genai.Client()  # uses GOOGLE_API_KEY env var


def generate(prompt_path: Path) -> Path | None:
    """Generate an image from a prompt file with retry logic."""
    text = prompt_path.read_text()

    # Split YAML frontmatter from prompt body
    _, fm_raw, body = text.split("---", 2)
    frontmatter = yaml.safe_load(fm_raw)

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio=frontmatter.get("aspect_ratio", "16:9"),
            image_size=frontmatter.get("resolution", "2K"),
        ),
    )

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=body.strip(),
                config=config,
            )
            for part in response.parts:
                if part.inline_data is not None:
                    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
                    name = frontmatter.get("name", prompt_path.stem)
                    output_path = OUTPUT_DIR / f"{name}-{timestamp}.png"
                    part.as_image().save(str(output_path))
                    return output_path
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                wait = 10 * (2 ** attempt)
                print(f"  Retry {attempt + 1}/{MAX_RETRIES} in {wait}s: {e}")
                time.sleep(wait)
            else:
                raise

    print(f"  Failed after {MAX_RETRIES} retries: {prompt_path.name}")
    return None


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)

    if len(sys.argv) > 1:
        # Generate specific prompt
        generate(Path(sys.argv[1]))
    else:
        # Batch: generate all prompts with delay between calls
        for prompt in sorted(PROMPT_DIR.glob("*.md")):
            print(f"Generating: {prompt.name}")
            result = generate(prompt)
            if result:
                print(f"  Saved: {result}")
            time.sleep(15)  # mandatory delay between calls
```

### Batch Shell Pattern

```bash
for prompt in prompts/*.md; do
    python generate.py "$prompt"
    sleep 15
done
```

The 15-second delay between calls is not optional. See "503 UNAVAILABLE" below.

## Failures and Workarounds

### Free Tier Has Zero Quota

The free tier provides zero image generation quota. Billing MUST be enabled on the Google Cloud project. The API returns a quota exhaustion error with no useful message.

### 503 UNAVAILABLE -- Batch Overload

Rapid sequential generation triggers 503 errors from aggressive rate limiting.

**Fix:** Minimum 10-15 second delay between calls, plus exponential backoff:

| Retry | Wait |
|---|---|
| 1 | 10s |
| 2 | 20s |
| 3 | 40s |
| After 3 | Skip and log |

### Text Rendering Is Unreliable

The model cannot reliably render text. Letters come out garbled, misspelled, or stylistically inconsistent.

**Mitigation:** Always include "No text anywhere in the image" in every prompt. For label-like elements, describe the physical object (engraved metal plate, embossed leather tag) rather than the text content.

### Output Format Inconsistency

The API sometimes returns JPEG data even when the output filename ends in `.png`. Verify actual format or convert explicitly if format consistency matters downstream.

### Dense Prompt Timeouts

Complex prompts with heavy detail can timeout on the first attempt. Retry logic handles this -- the same prompt typically succeeds on the second or third call.

### Overly Long Prompts (800+ Words)

The model begins ignoring later instructions in very long prompts. The sweet spot is 300-500 words. If a prompt exceeds this, restructure rather than truncate -- move the most important visual details earlier.

### Multiple Similar Subjects

When a prompt requests multiple instances of similar subjects (e.g., several characters in similar clothing), the model makes them near-identical. Differentiate aggressively with unique physical details for each.

## Iteration Strategy

### Edit, Don't Re-Roll

Refine existing prompts based on output rather than starting from scratch. Small targeted edits converge faster than fresh attempts. The model is sensitive to incremental phrasing changes.

### Archive Every Generation

Use timestamp-based filenames to preserve iterations: `{name}-{YYYY-MM-DD-HHMM}.png`. Each generation costs money -- never overwrite previous output.

### Print-Shop Language for Screen-Print Results

When generating print-style artwork, use vocabulary from the print shop: ink layers, halftone grain, paper stock texture, misregistration effects, spot color separation. The model has strong training signal on print production terminology.

## Common Pitfalls

### What Fails

- **Contradictory instructions**: "vibrant and muted" -- pick one
- **Too many subjects**: Three equally weighted elements compete for attention
- **Abstract concepts without visual anchors**: "the feeling of loss" -- show a specific scene that evokes it
- **Overly long prompts**: 800+ words causes the model to contradict itself
- **Requesting specific text**: Gemini renders text poorly -- always suppress it
- **Relying on negatives**: "no people, no buildings, no cars" -- describe what IS there

### What Succeeds

- **One clear scene**: A single moment, frozen, described spatially
- **Constrained palette**: Fewer colors = stronger visual identity
- **Specific textures**: "visible halftone grain heaviest on the sky gradient" beats "textured"
- **Emotional detail in every section**: Each element carries meaning, not just geometry
- **The final sentence of each section** lands on a feeling, not a measurement
