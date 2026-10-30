# Photorealistic scene assets

Generation mode: built-in image_gen, four separate new-image requests, 26 October 2026 (Malaysia time). These are synthetic images, not photographs taken at a real stop. Original generated PNGs are bundled unchanged. The app adds optional manually positioned zone and box overlays at runtime; no YOLO processing or confidence score is claimed for those overlays.

| Asset | Scenario |
|---|---|
| clear.png | Clear boarding bay with a distant bus |
| car.png | Red sedan blocking the bay |
| motorcycle.png | Helmeted rider on scooter occupying the bay |
| cleared.png | Clear bay, blue bus outside in adjacent lane |

Each is an independent generated scene. These are not consecutive frames of a real camera recording. Fixture timestamps, dwell and event history belong to the manual scenario demonstration. The legacy illustrated video is a separate logic replay, not a video of these photos.

## Final prompt set

Shared prompt: Photorealistic natural photographic asset of a fictional Malaysian smart bus stop, landscape 16:9. Elevated fixed CCTV viewpoint about 3 metres above the street, looking along the kerb. Contemporary Cyberjaya-like tropical boulevard, sidewalk and glass/dark-metal shelter on the left, tactile yellow paving, palms and modern low buildings. Yellow-marked asphalt bus bay from wide foreground to narrow middle distance; general traffic lane on the right. Natural slightly overcast daylight, believable proportions and detailed materials. No identifiable faces, readable plates, logos, watermark, bounding boxes, digital annotations, confidence numbers or timestamps.

Scene-specific prompts:

1. Clear: The foreground bay is completely empty. A small distant bus approaches outside the bay; a few anonymous pedestrians are near the shelter.
2. Car: A red compact sedan is stationary centrally in the bay, seen from the rear three-quarter view, approximately x40–70%, y42–80%. It blocks shelter access. A blue bus approaches in the right background lane; no other foreground vehicle.
3. Motorcycle: A black/silver scooter and anonymous helmeted rider are stationary centrally in the bay, approximately x46–62%, y43–82%. No car in the bay. A blue bus is farther away in the right lane.
4. Cleared: The foreground bay is fully empty. A blue accessible city bus approaches in the adjacent right lane in the middle distance; no car or motorcycle occupies the bay.

The generated locations differ slightly; no exact site continuity or real-world geometry is asserted. Presentation polygons are configured per image in photo_scenarios.py. Confidence remains unavailable for all these manual fixtures. Actual authorized uploaded video follows the separate YOLO inference workflow.
