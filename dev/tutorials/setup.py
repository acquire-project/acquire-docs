# # Utilizing the Setup Method
#
# This tutorial will provide an example of utilizing the [setup method](https://github.com/acquire-project/acquire-python/blob/ce0764e86bf1d10eb3a447eb670c28808ab3da3b/python/acquire/__init__.py#L41) to configure `Runtime` and specify some basic properties.
#
# ## Setup Function Definition

def setup(
    runtime: Runtime,
    camera: Union[str, List[str]],
    storage: Union[str, List[str]],
    output_filename: Optional[str],
) -> Properties


# The `setup` function can be used as a shorthand to simplify the `Runtime` configuration process. `setup` takes a `Runtime` object and strings of the camera and storage device names and returns a `Properties` object. You may also optionally specify the filename for writing the data.
#
# ## Example

# +
import acquire

# Initialize a Runtime object
runtime = acquire.Runtime()

# use setup to get configuration and set the camera, storage, and filename
config = acquire.setup(runtime, "simulated: radial sin", "Zarr", "out.zarr")
# -
# You can subsequently use `config` to specify additional settings and set those configurations before beginning acquisition.
#
# Without using setup, the process would take a few additional lines of codes. The below code is equivalent to the example above.

# +
import acquire

# Initialize a Runtime object
runtime = acquire.Runtime()

# Grab the current configuration
config = runtime.get_configuration()

# Select the radial sine simulated camera as the video source
config.video[0].camera.identifier = runtime.device_manager().select(acquire.DeviceKind.Camera, "simulated: radial sin")

# Set the storage to Zarr to have the option to save multiscale data
config.video[0].storage.identifier = runtime.device_manager().select(acquire.DeviceKind.Storage, "Zarr")

# Set the output file to out.zarr
config.video[0].storage.settings.filename = "out.zarr"
# -

# In either case, we can update the configuration settings using:

config = runtime.set_configuration(config)

# [Download this tutorial as a Python script](setup.py){ .md-button .md-button-center }
