# Test Camera Drivers

This tutorial will cover testing that your cameras, or video sources, has been properly identified.

Acquire supports the following cameras (currently only on Windows):

- [Hamamatsu Orca Fusion BT (C15440-20UP)](https://www.hamamatsu.com/eu/en/product/cameras/cmos-cameras/C15440-20UP.html)
- [Vieworks VC-151MX-M6H00](https://www.visionsystech.com/products/cameras/vieworks-vc-151mx-sony-imx411-sensor-ultra-high-resolution-cmos-camera-151-mp)
- [FLIR Blackfly USB3 (BFLY-U3-23S6M-C)](https://www.flir.com/products/blackfly-usb3/?model=BFLY-U3-23S6M-C&vertical=machine+vision&segment=iis)
- [FLIR Oryx 10GigE (ORX-10GS-51S5M-C)](https://www.flir.com/products/oryx-10gige/?model=ORX-10GS-51S5M-C&vertical=machine+vision&segment=iis)

Acquire provides the following simulated cameras:

- **simulated: uniform random** - Produces uniform random noise for each pixel.
- **simulated: radial sin** - Produces an animated radial sine wave pattern.
- **simulated: empty** - Produces no data, leaving a blank image. This camera simulates acquiring as fast as possible.

Acquire will only identify cameras whose drivers are present on your machine. The `DeviceManager` class manages selection of cameras and storage. We can create a `DeviceManager` object using the following:

```python
import acquire

# Instantiate a Runtime object
runtime = acquire.Runtime()

# Instantiate a DeviceManager object for the Runtime
dm = runtime.device_manager()
```

`DeviceManager` objects have `device` methods which lists the identifiers for discovered devices. You can iterate over this list to determine which cameras were discovered.

```python
for device in dm.devices():
    print(device)
```

The output of this code is below. All discovered devices, both cameras and storage devices, will be listed. In this tutorial, no cameras were connected to the machine, so only simulated cameras were found. Note that the storage devices also printed.

```
<DeviceIdentifier Camera "simulated: uniform random">
<DeviceIdentifier Camera "simulated: radial sin">
<DeviceIdentifier Camera "simulated: empty">
<DeviceIdentifier Storage "raw">
<DeviceIdentifier Storage "tiff">
<DeviceIdentifier Storage "trash">
<DeviceIdentifier Storage "tiff-json">
<DeviceIdentifier Storage "Zarr">
<DeviceIdentifier Storage "ZarrBlosc1ZstdByteShuffle">
<DeviceIdentifier Storage "ZarrBlosc1Lz4ByteShuffle">
```

For cameras that weren't discovered you will see an error like the one below. These errors will not affect performance and can be ignored.

```
ERROR acquire.runtime 2023-10-20 19:03:17,917 runtime.rs:40 C:\actions-runner\_work\acquire-driver-hdcam\acquire-driver-hdcam\src\acquire-core-libs\src\acquire-device-hal\device\hal\loader.c:114 - driver_load(): Failed to load driver at "acquire-driver-hdcam".
```

[Download this tutorial as a Python script](drivers.py){ .md-button .md-button-center }
