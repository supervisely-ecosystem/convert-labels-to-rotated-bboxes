
<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/115161827/204101369-d3ca96fe-d252-4c9f-8dbe-01d86ab377d3.png"/>  

# Convert Labels to Rotated Bboxes

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-to-use">How To Use</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/convert-labels-to-rotated-bboxes)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/convert-labels-to-rotated-bboxes)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/convert-labels-to-rotated-bboxes.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/convert-labels-to-rotated-bboxes.png)](https://supervise.ly)

</div>

# Overview

Convert labels in the project or dataset to rotated bounding boxes (`Polygon` with properties of rotated bbox). Supported shapes: `Polygon`, `Bitmap`, `Line`, `Rectangle` or `Any Shape` with any of the mentioned shapes. Resulting label names will be added suffix `ro_bbox`, e.g `plane` -> `plane_ro_bbox`. Disable `Keep original annotations` checkbox if you don't want to copy original labels. Application always converts data to the new project, original project will remain unchanged.

You can use this app along with [`Export to DOTA`](https://ecosystem.supervise.ly/apps/export-to-dota) app.

<table>
  <tr>
    <th>Original (Image of Labeling tool before convertion)</th>
    <th>Converted (Image of Labeling tool after convertion)</th>
  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/115161827/204102964-bb07db56-f60a-4f62-b487-72e90ea72d55.png"/></td>
    <td><img src="https://user-images.githubusercontent.com/115161827/204103375-d6aa6cc7-d5e9-422b-aaea-a356cc333604.png"/></td>
  </tr>
</table>

# How to use

App can be launched from ecosystem, images project or images dataset

## Option 1. Run from Ecosystem

**Step 1.** Run the app from Ecosystem

<img src="https://user-images.githubusercontent.com/115161827/204102957-c406e786-3ecc-49fc-93f0-44c7ab513471.jpg" width="80%" style='padding-top: 10px'>  

**Step 2.** Select input project or dataset, select options and press the Run button

<img src="https://user-images.githubusercontent.com/115161827/204102955-7854af24-a847-4d7a-a633-4f1639ab370f.gif" width="80%" style='padding-top: 10px'>

## Option 2. Run from Images Project or Dataset

**Step 1.** Run the application from the context menu of the Images Project or Dataset

<img src="https://user-images.githubusercontent.com/115161827/204102960-40fa831c-3a20-4289-9c30-90046de4d992.png" width="80%" style='padding-top: 10px'>  

**Step 2.** Select options in the modal window and press the Run button

<img src="https://user-images.githubusercontent.com/115161827/204102963-70a22077-c265-4c21-895b-e76abe4b791f.png" width="80%" style='padding-top: 10px'>

## Result

<img src="https://user-images.githubusercontent.com/115161827/204251652-e36e941a-9023-4009-b813-61243c98a164.png" width="80%" style='padding-top: 10px'>
