# Watermark Removal Guide for WP2 Images

## Current Status
WP2 reverted to use original images from `wp2-images/` directory.

## Manual Watermark Removal Options

### Option 1: Google Photos Magic Eraser (Recommended)
1. Upload images to Google Photos
2. Open image in editor
3. Use "Magic Eraser" tool
4. Select watermark areas
5. Google AI will remove them automatically
6. Download cleaned images

### Option 2: Photoshop Generative Fill
1. Open image in Photoshop
2. Select watermark with lasso tool
3. Choose "Generative Fill"
4. Leave prompt empty or type "remove"
5. AI will fill area intelligently
6. Save cleaned version

### Option 3: GIMP (Free)
1. Download GIMP (free Photoshop alternative)
2. Open image
3. Use "Clone Stamp" or "Healing Tool"
4. Manually remove watermarks
5. Takes more time but effective

### Option 4: Online Tools
- **Cleanup.pictures** - AI-powered removal
- **Remove.bg** - For simple watermarks
- **Photopea** - Free online Photoshop-like tool

## Recommended Workflow

For WP2 figures:
1. Use Google Photos Magic Eraser for fastest results
2. Or use Photoshop Generative Fill if you have access
3. Save cleaned images as: `wp2-fig1-clean.png`, `wp2-fig2-clean.png`, etc.
4. Place in `white-papers/wp2-images-clean/`
5. Update WP2 to reference cleaned versions

## Current WP2 Images

- Figure 1: `Smarter_AI_Not_Bigger_Models_page3_img1.png`
- Figure 2: `Beyond_Scale_Structure_Truth_page4_img1.png`
- Figure 3: `Smarter_AI_Not_Bigger_Models_page7_img1.png`
- Figure 4: `Smarter_AI_Not_Bigger_page5_img1.png`

## Decision

For now, using original images with watermarks is acceptable for:
- Internal review
- Draft versions
- Knowledge base documentation

For final publication, use one of the manual removal methods above.
