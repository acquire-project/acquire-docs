---
title: Acquire Docs
template: home.html
hide:
    - toc
---

## Tiles

- Getting Started: Install Acquire and use simulated cameras

- API Reference: Information on classes and methods

- Tutorials: Guides on using Acquire for specific tasks

- For contributors: Learn how to contribute code or documentation to Acquire


##  About Acquire

[Acquire](https://github.com/acquire-project/acquire-python) (`acquire-imaging` on [PyPI](https://pypi.org/project/acquire-imaging/)) provides high-speed, multi-camera, video streaming and image acquisition with a [programming interface](api_reference.md) for streaming video data directly to [napari](https://napari.org/stable/), Python and cloud-friendly file formats.

## Installation

To install Acquire on Windows, macOS, or Ubuntu, simply run the following command:

```
python -m pip install acquire-imaging
```

## Supported Cameras and File Formats
Acquire supports the following cameras (currently only on Windows):

- [Hamamatsu Orca Fusion BT (C15440-20UP)](https://www.hamamatsu.com/eu/en/product/cameras/cmos-cameras/C15440-20UP.html)
- [Vieworks VC-151MX-M6H00](https://www.visionsystech.com/products/cameras/vieworks-vc-151mx-sony-imx411-sensor-ultra-high-resolution-cmos-camera-151-mp)
- [FLIR Blackfly USB3 (BFLY-U3-23S6M-C)](https://www.flir.com/products/blackfly-usb3/?model=BFLY-U3-23S6M-C&vertical=machine+vision&segment=iis)
- [FLIR Oryx 10GigE (ORX-10GS-51S5M-C)](https://www.flir.com/products/oryx-10gige/?model=ORX-10GS-51S5M-C&vertical=machine+vision&segment=iis)

Acquire also supports the following output file formats:

- [Tiff](https://en.wikipedia.org/wiki/TIFF)
- [Zarr](https://zarr.dev/)

For testing and demonstration purposes, Acquire provides a few simulated cameras, as well as raw and trash output devices.

## Citing Acquire
Provide the [CITATION.cff file](https://github.com/acquire-project/acquire-python/blob/main/CITATION.cff)

## Acquire License
`Acquire` is provided under an [Apache 2.0 license](https://github.com/acquire-project/acquire-python/blob/main/LICENSE). You can learn more about the Apache license in the [documentation here](https://www.apache.org/licenses/LICENSE-2.0).
