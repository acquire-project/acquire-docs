# Finite Triggered Acquisition
Acquire (`acquire-imaging` [on PyPI](https://pypi.org/project/acquire-imaging/)) is a Python package providing a multi-camera video streaming library focused on performant microscopy, with support for up to two simultaneous, independent, video streams.

This tutorial shows an example of setting up triggered acquisition of a finite number of frames with one of Acquire's supported devices and saving the data to a Zarr file.

## Initialize Acquisition

To start, we'll import `Acquire` and create an acquisition `Runtime` object, which initializes the driver adaptors needed for the supported cameras.

```python
import acquire
runtime = acquire.Runtime()
```

## Configure Camera

All camera settings can be captured by an instance of the `Properties` class, which will be associated will a given camera acquisition. The settings can be stored in a dictionary (e.g: `Properties.dict()`). These settings can be saved to a JSON file to be subsequently loaded, (e.g. ` Properties(**json.load('acquire.json'))` ), using the [json library](https://docs.python.org/3/library/json.html#).

```python
props = runtime.get_configuration()

import json
with open("/path/to/acquire.json", "w") as f:
    json.dump(props.dict(), f)
```

The current configuration settings can be checked and assigned to an instance of the `Properties` class with:

```python
p = runtime.get_configuration() 
```

Since `Acquire` supports 2 video streams, each camera, or source, must be configured separately. In this example, we will only use 1 source for the acquisition, so we will only need to configure `props.video[0]`. To set the first video stream to [Hamamatsu Orca Fusion BT (C15440-20UP)](https://www.hamamatsu.com/eu/en/product/cameras/cmos-cameras/C15440-20UP.html), you can use the following with a regular expression to grab the Hamamatsu camera:

```python
p.video[0].camera.identifier = runtime.device_manager().select(acquire.DeviceKind.Camera, 'Hamamatsu C15440.*')
```

Next we'll choose the settings for the Hamamatsu camera. The `CameraProperties` class describes the available settings, which include exposure time (in microseconds), binning, pixel data type (e.g. u16), and how many frames to acquire.

Every property can be set using the following, but in this example, we will only change a few of the available settings.

```python
p.video[0].camera.settings.binning = 1 # no pixels will be combined
p.video[0].camera.settings.shape = (1700, 512) # shape of the image to be acquired in pixels
p.video[0].camera.settings.offset = (302, 896) # centers the image region of interest on the camera sensor
p.video[0].camera.settings.pixel_type = acquire.SampleType.U16 # sets the pixel data type to a 16-bit unsigned integer
p.video[0].max_frame_count = 10 # finite acquisition of 10 frames. Use 0 for infinite acquisition.
```

Triggers can also be set in the `CameraProperties` object. You can construct a `Trigger` from a JSON file (e.g. `acquire.Trigger(**json.loads(open('trigger.json')))` ), using the [json library](https://docs.python.org/3/library/json.html#). 

```python
trig = acquire.Trigger()

import json
with open("/path/to/trigger.json", "w") as f:
    json.dump(trig.dict(), f)
```

In this example, we'll only use output triggers.

By default, the camera's internal triggering is used, but you may explicitly disable external input triggers using:

```python
p.video[0].camera.settings.input_triggers = acquire.InputTriggers() # default: disabled
```

Output triggers can be set to begin exposure, start a new frame, and wait before acquiring. We can enable an exposure trigger to start on the rising edge with:

```python
p.video[0].camera.settings.output_triggers.exposure = acquire.Trigger(
	enable=True, line=1, edge="Rising"
)
```

## Select Storage

`Storage` objects have identifiers which specify the file type (e.g. Zarr or tif) and settings described by an instance of the `StorageProperties` class. We can set the file type to Zarr and set the file name to "out" with:

```python
p.video[0].storage.identifier = runtime.device_manager().select(acquire.DeviceKind.Storage,'zarr') 
p.video[0].storage.settings.filename="out.zarr"
```

## Save configuration
None of these settings will be updated in until you call the `set_configuration` method. This method reads what the current configuration settings are on the device.

We'll set the configuration with:

```python
p = runtime.set_configuration(p)
```

You can optionally print out these settings using the [Rich](https://rich.readthedocs.io/en/stable/introduction.html) python library to save for your records with:

```python
from rich.pretty import pprint
pprint(p.dict())
```

## Acquire data

To begin acquisition:

```python
runtime.start()
```

You can stop acquisition with `runtime.stop()` to stop after the specified number of frames is collected or `runtime.abort()` to immediately stop acquisition.
