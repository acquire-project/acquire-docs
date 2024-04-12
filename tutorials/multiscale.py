# # Multiscale Data Acqusition
#
# This tutorial will provide an example of writing multiscale data to a Zarr file.
#
# Zarr has additional capabilities relative to Acquire's basic storage devices, namely _chunking_, _compression_, and _multiscale storage_. To enable _chunking_ and _multiscale storage_, set those attributes in instances of the `ChunkingProperties` and `StorageProperties` classes, respectively. You can learn more about the Zarr capabilities in `Acquire` [here](https://github.com/acquire-project/acquire-driver-zarr).
#
# ## Configure `Runtime`
# To start, we'll create a `Runtime` object and begin to configure the streaming process, selecting `Zarr` as the storage device so that writing multiscale data is possible.

# +
import acquire

# Initialize a Runtime object
runtime = acquire.Runtime()

# Initialize the device manager
dm = runtime.device_manager()

# Grab the current configuration
config = runtime.get_configuration()

# Select the radial sine simulated camera as the video source
config.video[0].camera.identifier = dm.select(acquire.DeviceKind.Camera, "simulated: radial sin")

# Set the storage to Zarr to have the option to save multiscale data
config.video[0].storage.identifier = dm.select(acquire.DeviceKind.Storage, "Zarr")

# Set the time for collecting data for a each frame
config.video[0].camera.settings.exposure_time_us = 5e4  # 50 ms

# Set the size of image region of interest on the camera (x, y)
config.video[0].camera.settings.shape = (1920, 1080)

# Set the max frame count
config.video[0].max_frame_count = 5 # collect 5 frames

# Set the image data type as a Uint8
config.video[0].camera.settings.pixel_type = acquire.SampleType.U8

# Set the scale of the pixels
config.video[0].storage.settings.pixel_scale_um = (1, 1) # 1 micron by 1 micron

# Set the output file to out.zarr
config.video[0].storage.settings.filename = "out.zarr"
# -

# To complete configuration, we'll configure the multiscale specific settings and update all settings with the `set_configuration` method.

# +
# Chunk size may need to be optimized for each acquisition.
# See Zarr documentation for further guidance:
# https://zarr.readthedocs.io/en/stable/tutorial.html#chunk-optimizations
config.video[0].storage.settings.chunking.max_bytes_per_chunk = 16 * 2**20 # 16 MB

# x, y dimensions of each chunk
# 1/3 of the width and height of the image, generating 9 chunks
config.video[0].storage.settings.chunking.tile.width = (config.video[0].camera.settings.shape[0] // 3)
config.video[0].storage.settings.chunking.tile.height = (config.video[0].camera.settings.shape[1] // 3)

# turn on multiscale mode
config.video[0].storage.settings.enable_multiscale = True

# Update the configuration with the chosen parameters
config = runtime.set_configuration(config)
# -
# ## Collect and Inspect the Data

# +

# collect data
runtime.start()
runtime.stop()
# -

# You can inspect the Zarr file directory to check that the data saved as expected. This zarr file should have multiple subdirectories, one for each resolution in the multiscale data. Alternatively, you can inspect the data programmatically with:

# +
# Utilize the zarr python library to read the data
import zarr

# Open the data to create a zarr Group
group = zarr.open("out.zarr")
# -
# With multiscale mode enabled, an image pyramid will be formed by rescaling the data by a factor of 2 progressively until the rescaled image is smaller than the specified zarr chunk size in both dimensions. In this example, the original image dimensions are (1920, 1080), and we chunked the data using tiles 1/3 of the size of the image, namely (640, 360). To illustrate this point, we'll inspect the sizes of the various levels in the multiscale data and compare it to our specified chunk size.

group["0"], group["1"], group["2"]

# The output will be:
#
# ```
# (<zarr.core.Array '/0' (10, 1, 1080, 1920) uint8>,
#  <zarr.core.Array '/1' (5, 1, 540, 960) uint8>,
#  <zarr.core.Array '/2' (2, 1, 270, 480) uint8>)
# ```
#
# Here, the `"0"` directory contains the full-resolution array of frames of size 1920 x 1080, with a single channel, saving all 10 frames.
# The `"1"` directory contains the first rescaled array of frames of size 960 x 540, averaging every two frames, taking the frame count from 10 to 5.
# The `"2"` directory contains a further rescaled array of frames of size 480 x 270, averaging every four frames, taking the frame count from 10 to 2. Notice that both the frame width and frame height are now smaller than the chunk width and chunk height of 640 and 360, respectively, so this should be the last array in the group.
#
# [Download this tutorial as a Python script](multiscale.py){ .md-button .md-button-center }
