# Configuring Zarr storage with chunking

This tutorial will provide an example of writing chunked data to a Zarr storage device.

Zarr has additional capabilities relative to the basic storage devices, namely _chunking_, _sharding_ (in the case of Zarr V3)_, _compression_, and _multiscale storage_.
To enable _chunking_, set the attributes in an instance of the `ChunkingProperties` class.
You can learn more about the Zarr capabilities in Acquire [here](https://github.com/acquire-project/acquire-driver-zarr).

## Configure the acquisition

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

# Use a storage device that supports chunking, in this case, Zarr
config.video[0].storage.identifier = dm.select(acquire.DeviceKind.Storage, "Zarr")

# Delay between each frame
config.video[0].camera.settings.exposure_time_us = 7e4  # 70 ms

# Size of image region of interest on the camera (x, y)
config.video[0].camera.settings.shape = (1920, 1080)

# Specify the pixel datatype as uint8
config.video[0].camera.settings.pixel_type = acquire.SampleType.U8

# Set the output file to out.zarr
config.video[0].storage.settings.uri = "out.zarr"
```

### Storage dimensions

Because Zarr supports n-dimensional arrays, we need to describe how the data we stream should be interpreted.
We do this by specifying *storage dimensions*, which correspond to the dimensionality of the output array.

Acquire requires at least 3 dimensions: frame width, frame height, and an append dimension.
The first 2 dimensions are required and may be followed by optional internal dimensions.
The final "append" dimension is also required.

Each dimension must have a type, for example, space, channel, time, or other.
This tutorial will use 5 dimensions following the [OME-NGFF specification](https://ngff.openmicroscopy.org/latest/#multiscale-md).
That is, we will use TCZYX order, with T corresponding to time, C to channel, Z to depth, Y to height, and X to width.

```python
dimension_x = acquire.StorageDimension(
    name="x",
    kind="Space",
    array_size_px=1920,
    chunk_size_px=960
)

dimension_y = acquire.StorageDimension(
    name="y",
    kind="Space",
    array_size_px=1080,
    chunk_size_px=540
)

dimension_z = acquire.StorageDimension(
    name="z",
    kind="Space",
    array_size_px=10,
    chunk_size_px=5
)

dimension_c = acquire.StorageDimension(
    name="c",
    kind="Channel",
    array_size_px=3,
    chunk_size_px=1
)

dimension_t = acquire.StorageDimension(
    name="t",
    kind="Time",
    array_size_px=0,
    chunk_size_px=10
)

config.video[0].storage.settings.acquisition_dimensions = [
    dimension_x,
    dimension_y,
    dimension_z,
    dimension_c,
    dimension_t
]
```

Notice that each `StorageDimension` object has several attributes.
- `name` is the name of the dimension. It is used to identify the dimension in the output array and must be unique.
- `kind` is the type of dimension. It can be `Space`, `Channel`, `Time`, or `Other`.
- `array_size_px` is the size of the dimension in pixels. It is the total size of the dimension.
- `chunk_size_px` is the size of the chunks in pixels. It is the size of the chunks in which the data will be stored.

There is an additional field, `shard_size_chunks`, which is used to specify the number of chunks per shard, but it is 
only used in Zarr V3, which we will discuss in a future tutorial.

The order in which we specify the dimensions is important.
The order of the dimensions in the `acquisition_dimensions` list determines the order of the dimensions in the output array.
In this case, the order is `x`, `y`, `z`, `c`, `t`, which corresponds to the order `TCZYX`.

Notice that the first two dimensions' `array_size_px` is the same as the camera's shape.
This is because the first two dimensions correspond to the spatial dimensions of the camera.

Another thing to notice is that the final dimension, `t`, has an `array_size_px` of 0.
This is because the size of the append dimension is not known in advance.
At most, we can say that the size of the append dimension is no larger than the number of frames we want to collect, but
because acquisition may terminate at any point before reaching the maximum frame count, we set the `array_size_px` to 0.

The number of frames to collect will now depend on the sizes of the internal dimensions.
For our example, to fill just one chunk of the `c` dimension, we will need to collect
`dimension_z.array_size_px * dimension_t.chunk_size_px` frames, or in other words, 10 frames.
To fill a single chunk of the `t` dimension, we will need to collect
`dimension_z.array_size_px * dimension_c.array_size_px * dimension_t.chunk_size_px` frames, or in other words, 300
frames.

```python

## Collect and Inspect the Data

```python
config.video[0].max_frame_count = dimension_z.array_size_px * dimension_c.array_size_px * dimension_t.chunk_size_px # 300

config = runtime.set_configuration(config)

# collect data
runtime.start()
runtime.stop()
```

You can inspect the Zarr file directory to check that the data saved as expected. Alternatively, you can inspect the data programmatically with:

```python
# Utilize the zarr library to open the data
import zarr

# create a zarr Group object
group = zarr.open(config.video[0].storage.settings.uri)

# check for the expected # of directories in the zarr container
assert len(group) == 1

# inspect the characteristics of the data
print(group["0"])
```

The output will be:
```
<zarr.core.Array '/0' (1, 3, 10, 1080, 1920) uint8>
```
As expected, we have only 1 top level directory, corresponding to the single array in the group.
We would expect more than 1 array only if we were writing [multiscale data](multiscale.md).
The overall array shape is (10, 1, 1080, 1920), corresponding to 10 frames, 1 channel, and a height and width of 1080
and 1920, respectively, per frame.

[Download this tutorial as a Python script](chunked.py){ .md-button .md-button-center }
