# Natural Language Processing using Multimodal Capabilities

<img src="./assets/multimodal.webp" alt="prompt" width="500" height="auto">


## Course Overview

### Introduction


In AI, "multimodal" refers to systems that can understand and generate responses across different types of data, such as text, images, audio, and video, instead of relying on just one data type. Multimodal APIs enable developers to build applications that integrate these varied data sources, making it possible for AI to interpret complex real-world inputs more naturally and cohesively. For example, a multimodal AI could analyze an image (visual modality) and respond with descriptive text, or it could interpret spoken language (audio modality) and generate related visuals. This capability allows applications to deliver richer, more human-like interactions by processing and integrating multiple data forms simultaneously.


## Exploring Google Gemini Vision APIs Capabilities

The Gemini API is capable of performing inference on images and videos provided to it. When given an image, a series of images, or a video, Gemini can:

- Describe or respond to questions about the content
- Summarize what the content shows
- Make inferences based on the content

This lesson showcases methods for prompting the Gemini API with image inputs, with all outputs presented as text only. Your practice will allow you to also create images with Python and Gemini.


## Image Generation

Image Generation is a technique that uses AI to create realistic images that don't exist in the real world. Unfortunately, there is currently no free way to create images, but the [Gemini Imagen API](https://ai.google.dev/gemini-api/docs/imagen) is in beta with a limited private preview at the time of writing this as well, of course, as the paid version of OpenAI's DALL-E.

## Lesson Takeaways

In this lesson, we will build the foundational component of a multimodal application: a system that safely downloads and validates images from URLs. This code serves as the preprocessing step necessary before implementing Gemini API functionality.

In today's lesson you will be able to:
- Accept user input for two image URLs
- Validate URL structure and file types
- Safely download and saves images locally
- Implement error handling and validation checks

[Lesson](./lesson.ipynb)