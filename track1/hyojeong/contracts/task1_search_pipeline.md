Contract: Task 1 Search Pipeline

Objective: The objective is to build a search pipeline that automatically collects metadata for at least 500 images from image source APIs (e.g., Unsplash, Pexels) using the search terms defined in space_types.json. The pipeline will save this structured data, ensuring full provenance for every image, into search_results.json.

1. Inputs
* space_types.json: A list of the 15 required room types and their associated search terms.
* image_sources.json: A list of image source configurations, including API availability and license details.
* Environment Variables (.env): Secure storage for API access keys to prevent hardcoding.

2. Processing
* Looping: The script will iterate through each room type defined in space_types.json.
* API Querying: Send HTTP requests to the respective image source APIs using the designated search terms.
* Rate Limiting: Implement time.sleep() between API requests to respect the rate limits of each source and prevent IP bans.
* Error Handling: The script will not silently skip errors. Any zero-result queries or API connection failures will be explicitly logged.

3. Outputs
* search_results.json: A structured JSON file containing the metadata for all collected images.
* Required Fields (per image record): 
- url: The direct URL to the image.
- thumbnail_url: The URL to a smaller, display-friendly version of the image.
- title: The title or description of the image.
- photographer: The name of the photographer (best effort if provided by API).
- source_name: The name of the platform (e.g., "Unsplash").
- source_page_url: The original webpage where the image is hosted (Essential for provenance).
- license: The specific license under which the image is provided.
- space_type: The assigned room category (e.g., "living_room").
- search_query: The specific string used to find the image.
- collected_at: The exact time of collection (ISO 8601 format).

4. Success Conditions
- [ ] API keys are stored in environment variables and are NOT hardcoded in the source code.
- [ ] Every image record strictly contains the required provenance fields (source_page_url, source_name, license).
- [ ] The generated search_results.json is structurally valid and formatted correctly.
- [ ] The script successfully demonstrates rate-limiting logic (e.g., time.sleep).
- [ ] Queries returning zero results are properly logged instead of causing silent failures.