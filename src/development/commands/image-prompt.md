---
description: Write a structured image prompt for Gemini 3 Pro Image generation
argument-hint: "<subject description or creative direction>"
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Image Prompt -- Gemini 3 Pro Image

Write a structured image generation prompt for `gemini-3-pro-image-preview`. The user provides a subject or creative direction; you produce a complete prompt file ready for generation.

## Instructions

1. Read the gemini-image-gen skill at `src/development/skills/gemini-image-gen/SKILL.md` for full reference on prompt structure, style archetypes, and best practices
2. Ask the user for any missing context:
   - **Subject**: What is the image of?
   - **Mood/tone**: What should it feel like?
   - **Style**: Screen-print, cinematic, vintage document, illustration, or other?
   - **Aspect ratio**: 16:9 (landscape), 3:4 (portrait), 1:1 (square), 9:16 (phone), 21:9 (ultra-wide)?
   - **Resolution**: 1K, 2K, or 4K?
3. Write a 300-500 word prompt as a markdown file with YAML frontmatter
4. Save to the user's preferred location (default: `prompts/{name}.md`)

## Output Format

```yaml
---
name: kebab-case-name
aspect_ratio: '16:9'
resolution: 2K
style: screen-print-poster
last_generated: null
last_updated: '<current ISO 8601 UTC>'
---

### Subject
[Detailed description of the primary subject with position, materials, colors]

### Environment
[Setting, background, spatial relationships grounding the subject]

### Secondary Elements
[Supporting objects, atmospheric effects]

### Lighting
[Direction, color temperature, time of day, quality]

### Style
[Medium, color constraints, texture, imperfections, mood summary]

No text anywhere in the image.
```

## Key Rules

- Write prose essays, not keyword lists
- Use spatial anchoring ("lower-right third", not "in the scene")
- Constrain palette to 4-6 colors with assigned roles
- One primary subject per image -- everything else supports it
- Describe what SHOULD be present, not what shouldn't
- Always end with "No text anywhere in the image."
- Physical metaphors over abstract concepts
- 300-500 words is the sweet spot -- longer prompts degrade quality
