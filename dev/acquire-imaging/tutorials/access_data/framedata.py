# %% [markdown]
# # Accessing Data during Acquisition
#
# This tutorial will provide an example of accessing data from a video source during acquisition.
#
# ## Configure `Runtime`
#
# To start, we'll create a `Runtime` object and configure the streaming process.

# %%
import acquire

# Initialize a Runtime object
runtime = acquire.Runtime()

# Initialize the device manager
dm = runtime.device_manager()

# Grab the current configuration
config = runtime.get_configuration()

# Select the radial sine simulated camera as the video source
config.video[0].camera.identifier = dm.select(acquire.DeviceKind.Camera, "simulated: radial sin")

# Set the storage to trash to avoid saving the data
config.video[0].storage.identifier = dm.select(acquire.DeviceKind.Storage, "Trash")

# Set the time for collecting data for a each frame
config.video[0].camera.settings.exposure_time_us = 5e4  # 50 ms

# Set the shape of the region of interest on the camera chip
config.video[0].camera.settings.shape = (1024, 768)

# Set the max frame count to 2**(64-1) the largest number supported by Uint64 for essentially infinite acquisition
config.video[0].max_frame_count = 100 # collect 100 frames

# Update the configuration with the chosen parameters
config = runtime.set_configuration(config)
# %% [markdown]
# ## Working with `AvailableData` objects
#
# During Acquisition, the `AvailableData` object is the streaming interface. We can create an `AvailableData` object by calling `get_available_data` in a `with` statement, and work with the `AvailableData` object while it exists inside of the `with` loop. The data is invalidated after exiting the `with` block, so make a copy of the `AvailableData` object to work with the data outside of the `with` block. In this example, we'll simply use the `AvailableData` object inside of the `with` block.
#
# There may not be data available. To increase the likelihood of `AvailableData` containing data, we'll utilize the `time` python package to introduce a delay before we create our `AvailableData` object.
#
# If there is data, we'll use the `AvailableData` `frames` method, which iterates over the `VideoFrame` objects in `AvailableData`, and the python `list` method to create a variable `video_frames`, a list of the `VideoFrame` objects one for each stream. 
#
# `VideoFrame` has a `data` method which provides the frame as an `NDArray`. The shape of this NDArray corresponds to the image dimensions used internally by Acquire namely [planes, height, width, channels]. Since we have a single channel, both the first and the last dimensions will be 1. The interior dimensions are height and width, respectively. We can use the `numpy.squeeze` method to grab the desired NDArray image data since the other dimensions are 1. This is equivalent to `image = first_frame[0][:, :, 0]`.

# %%
# package for introducing time delays
import time

# start acquisition
runtime.start()

# time delay of 0.5 seconds
time.sleep(0.5)

# grab the packet of data available on disk for video stream 0.
# This is an AvailableData object.
with runtime.get_available_data(0) as available_data:

    # NoneType if there is no available data.
    # We can only grab frames if data is available.
    if available_data.get_frame_count() > 0:
    
        # frames is an iterator over available_data
        # we'll use this iterator to make a list of the frames
        video_frames = list(available_data.frames())

    # grab the first VideoStream object in frames and convert it to an NDArray
    first_frame = video_frames[0].data()
    
    #inspect the dimensions of the first_frame
    print(first_frame.shape)
    
    # Selecting the image data. Equivalent to image = first_frame[0][:, :, 0]
    image = first_frame.squeeze()
    
    # inspect the dimensions of the squeezed first_frame
    print(image.shape)

# stop runtime
runtime.stop()

# %% [markdown]
# The output will be:
# ```
# (1, 768, 1024, 1)
# (768, 1024)
# ```
#
# [Download this tutorial as a Python script](framedata.py){ .md-button .md-button-center }
