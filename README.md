
<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/12828725/182181033-d0d1a690-8388-472e-8862-e0cacbd4f082.png"/>  

# Convert Labels to Rotated Bboxes

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-to-use">How To Use</a>
</p>

</div>

# Overview

Convert labels in the project or dataset to rotated bounding boxes. Supported shapes: `Polygon`, `Bitmap`, `Line`, `Rectangle` or `Any Shape` with any of the mentioned shapes. Resulting label names will be added suffix `ro_bbox`, e.g `plane` -> `ro_bbox_plane`. If you want to keep labels from original project or dataset leave checkbox `Keep original annotations` in the modal window enabled. Application always converts data to the new project, original project will remain unchanged.

<table>
  <tr>
    <th>Original (Image of Labeling tool before convertion)</th>
    <th>Converted (Image of Labeling tool after convertion)</th>
  </tr>
  <tr>
    <td><img src=""/></td>
    <td><img src=""/></td>
  </tr>
</table>

# How to use

App can be launched from ecosystem, images project or images dataset

## Run from Ecosystem

**Step 1.** Run the app from Ecosystem

<img src="" width="80%" style='padding-top: 10px'>  

**Step 2.** Select input project or dataset, select options and press the Run button

<img src="" width="80%" style='padding-top: 10px'>

## Run from Images Project or Dataset

**Step 1.** Run the application from the context menu of the Images Project or Dataset

<img src="" width="80%" style='padding-top: 10px'>  

**Step 2.** Select options in the modal window and press the Run button

<img src="" width="80%" style='padding-top: 10px'>

## Result

<img src="Image of Workspace tasks with result project" width="80%" style='padding-top: 10px'>
