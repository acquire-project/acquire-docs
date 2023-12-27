# Chunking Data for Zarr Storage

This tutorial will provide an example of writing chunked data to a Zarr storage device.

Zarr has additional capabilities relative to the basic storage devices, namely _chunking_, _compression_, and _multiscale storage_. To enable _chunking_, set the attributes in an instance of the `ChunkingProperties` class. You can learn more about the Zarr capabilities in `Acquire` [here](https://github.com/acquire-project/acquire-driver-zarr).

## Configure `Runtime`
To start, we'll create a `Runtime` object and configure the streaming process, selecting `Zarr` as the storage device to enable chunking the data.

```python
import acquire

# Initialize a Runtime object
runtime = acquire.Runtime()

# Initialize the device manager
dm = runtime.device_manager()

# Grab the current configuration
config = runtime.get_configuration()

# Select the radial sine simulated camera as the video source
config.video[0].camera.identifier = dm.select(acquire.DeviceKind.Camera, "simulated: radial sin")

# Set the storage to Zarr to take advantage of chunking
config.video[0].storage.identifier = dm.select(acquire.DeviceKind.Storage, "Zarr")

# Set the time for collecting data for a each frame
config.video[0].camera.settings.exposure_time_us = 5e4  # 50 ms

# size of image region of interest on the camera (x, y)
config.video[0].camera.settings.shape = (1920, 1080)

# specify the pixel datatype as a uint8
config.video[0].camera.settings.pixel_type = acquire.SampleType.U8

# Set the max frame count
config.video[0].max_frame_count = 10 # collect 10 frames

# Set the output file to out.zarr
config.video[0].storage.settings.filename = "out.zarr"
```
Below we'll configure the chunking specific settings and update all settings with the `set_configuration` method.

```python
# Chunk size may need to be optimized for each acquisition.
# See Zarr documentation for further guidance:
# https://zarr.readthedocs.io/en/stable/tutorial.html#chunk-optimizations
config.video[0].storage.settings.chunking.max_bytes_per_chunk = 32 * 2**20 # 32 MB

# x, y dimensions of each chunk
# 1/2 of the width and height of the image, generating 4 chunks
config.video[0].storage.settings.chunking.tile.width = 1920 // 2
config.video[0].storage.settings.chunking.tile.height = 1080 // 2

# Update the configuration with the chosen parameters
config = runtime.set_configuration(config)
```

## Collect and Inspect the Data

```python
# collect data
runtime.start()
runtime.stop()
```

You can inspect the Zarr file directory to check that the data saved as expected. Alternatively, you can inspect the data programmatically with:

```python
# Utilize the zarr library to open the data
import zarr

# create a zarr Group object
group = zarr.open(config.video[0].storage.settings.filename)

# check for the expected # of directories in the zarr container
assert len(group) == 1

# inspect the characteristics of the data
group["0"]
```

The output will be:
```
<zarr.core.Array '/0' (10, 1, 1080, 1920) uint8>
```
As expected, we have only 1 top level directory, corresponding to the single array in the group. We would expect more than 1 array only if we were writing [multiscale data](multiscale.md). The overall array shape is (10, 1, 1080, 1920), corresponding to 10 frames, 1 channel, and a height and width of 1080 and 1920, respectively, per frame.

[Download this tutorial as a Python script](chunked.py){ .md-button .md-button-center }
