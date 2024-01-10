# # Finite Triggered Acquisition
#
# Acquire (`acquire-imaging` [on PyPI](https://pypi.org/project/acquire-imaging/)) is a Python package providing a multi-camera video streaming library focused on performant microscopy, with support for up to two simultaneous, independent, video streams.
#
# This tutorial shows an example of setting up triggered acquisition of a finite number of frames with one of Acquire's supported devices and saving the data to a Zarr file.
#
# ## Initialize Acquisition
#
# To start, we'll import `Acquire` and create an acquisition `Runtime` object, which initializes the driver adaptors needed for the supported cameras.

import acquire
runtime = acquire.Runtime()

# ## Configure Camera
#
# All camera settings can be captured by an instance of the `Properties` class, which will be associated with a given camera acquisition. The settings can be stored in a dictionary (e.g: `Properties.dict()`). These settings can be saved to a JSON file to be subsequently loaded, (e.g. `Properties(**json.load(open('acquire.json')))`), using the [json library](https://docs.python.org/3/library/json.html#). Check out [this tutorial](props_json.md) for a more detailed example, but in brief, you would use something like:

# +
config = runtime.get_configuration()

import json
with open("/path/to/acquire.json", "w") as f:
    json.dump(config.dict(), f)
# -

# The current configuration settings can be checked and assigned to an instance of the `Properties` class with:

config = runtime.get_configuration()

# Since `Acquire` supports 2 video streams, each camera, or source, must be configured separately. In this example, we will only use 1 source for the acquisition, so we will only need to configure `config.video[0]`. To set the first video stream to [Hamamatsu Orca Fusion BT (C15440-20UP)](https://www.hamamatsu.com/eu/en/product/cameras/cmos-cameras/C15440-20UP.html), you can use the following with a regular expression to grab the Hamamatsu camera:

config.video[0].camera.identifier = runtime.device_manager().select(acquire.DeviceKind.Camera, 'Hamamatsu C15440.*')

# Next we'll choose the settings for the Hamamatsu camera. The `CameraProperties` class describes the available settings, which include exposure time (in microseconds), binning, pixel data type (e.g. u16), and how many frames to acquire.
#
# Every property can be set using the following syntax, but in this example, we will only change a few of the available settings. [Check out this tutorial](configure.md) for an explanation of camera properties.

config.video[0].camera.settings.binning = 1 # no pixels will be combined
config.video[0].camera.settings.shape = (1700, 512) # shape of the image to be acquired in pixels
config.video[0].camera.settings.offset = (302, 896) # centers the image region of interest on the camera sensor
config.video[0].camera.settings.pixel_type = acquire.SampleType.U16 # sets the pixel data type to a 16-bit unsigned integer
config.video[0].max_frame_count = 10 # finite acquisition of 10 frames. Use 0 for infinite acquisition.

# Triggers can also be set in the `CameraProperties` object. The parameters can be stored in a dictionary (e.g: `Trigger.dict()`). You can construct a `Trigger` from a JSON file (e.g.  `acquire.Trigger(**json.loads(open('trigger.json')))` ), using the [json library](https://docs.python.org/3/library/json.html#). Check out [this tutorial](trig_json.md) for a more detailed example, but in brief, you would use something like:

# +
trig = acquire.Trigger()

import json
with open("/path/to/trigger.json", "w") as f:
    json.dump(trig.dict(), f)
# -

# In this example, we'll only utilize output triggers. By default, the camera's internal triggering is used, but you may explicitly disable external input triggers using:

config.video[0].camera.settings.input_triggers = acquire.InputTriggers() # default: disabled

# Output triggers can be set to begin exposure, start a new frame, or wait before acquiring. We can enable an exposure trigger to start on the rising edge with:

config.video[0].camera.settings.output_triggers.exposure = acquire.Trigger(
	enable=True, line=1, edge="Rising"
)

# ## Select Storage
#
# `Storage` objects have identifiers which specify the file type (e.g. Zarr or tiff) and settings described by an instance of the `StorageProperties` class. We can set the file type to Zarr and set the file name to "out" with:

config.video[0].storage.identifier = runtime.device_manager().select(acquire.DeviceKind.Storage,'zarr')
config.video[0].storage.settings.filename="out.zarr"

# ## Save configuration
# None of these settings will be updated in the `Properties` object until you call the `set_configuration` method. This method updates what the current configuration settings are on the device.
#
# We'll set the configuration with:

config = runtime.set_configuration(config)

# You can optionally print out these settings using the [Rich](https://rich.readthedocs.io/en/stable/introduction.html) python library to save for your records with:

from rich.pretty import pprint
pprint(config.dict())

# Check out [this tutorial](https://acquire-project.github.io/acquire-docs/tutorials/props_json/) for a more detailed example of saving `Properties`.
#
# ## Acquire data
#
# To begin acquisition:

runtime.start()

# You can stop acquisition with `runtime.stop()` to stop after the max number of frames is collected or `runtime.abort()` to immediately stop acquisition. You must call one of these methods at the end of an acquisition, as `Runtime` deletes all of the objects created during acquisition to free up resources upon shutdown. Otherwise, an exception will be raised when trying to restart acquisition.
#
# [Download this tutorial as a Python script](trigger.py){ .md-button .md-button-center }
