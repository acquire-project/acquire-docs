# Getting Started with Acquire

Acquire (`acquire-imaging` [on PyPI](https://pypi.org/project/acquire-imaging/)) is a Python package providing a multi-camera video streaming library focused on performant microscopy, with support for up to two simultaneous, independent, video streams.

This tutorial covers Acquire installation and shows an example of using Acquire with its provided simulated cameras to demonstrate the acquisition process.

## Installation

To install Acquire on Windows, macOS, or Ubuntu, simply run the following command:

```
python -m pip install acquire-imaging
```

We recommend installing `Acquire` in a fresh conda environment or virtualenv.
For example, to install `Acquire` in a conda environment named `acquire`:

```
conda create -n acquire python=3.10 # follow the prompts and proceed with the defaults
conda activate acquire
python -m pip install acquire-imaging
```

or with virtualenv:

```shell
$ python -m venv venv
$ . ./venv/bin/activate # or on Windows: .\venv\Scripts\Activate.bat or .\venv\Scripts\Activate.ps1
(venv) $ python -m pip install acquire-imaging
```

Once you have Acquire installed, simply call `import acquire` in your script, notebook, or module to start utilizing the package.

```python
import acquire
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
To see all the devices that Acquire supports, you can run the following script:

```python
import acquire

for device in acquire.Runtime().device_manager().devices():
    print(device)
```

## Tutorial Prerequisites

We will be writing to and reading from the [Zarr format](https://zarr.readthedocs.io/en/stable/), using the [Dask library](https://www.dask.org/) to load and inspect the data, and visualizing the data using [napari](https://napari.org/stable/).

You can install these prerequisites with:

```
python -m pip install dask "napari[all]" zarr
```

## Setup for Acquisition

We will use one of Acquire's simulated cameras to generate data and use Zarr for our output file format, which is called "storage device" in `Acquire`.

To begin, instantiate `Runtime` and `DeviceManager` and list the currently supported devices.

```python
import acquire

runtime = acquire.Runtime()
dm = runtime.device_manager()

for device in dm.devices():
    print(device)
```
The **runtime** is the main entry point in Acquire.
Through the runtime, you configure your devices, start acquisition, check acquisition status, inspect data as it streams from your cameras, and terminate acquisition.

Let's configure our devices now.
To do this, we'll get a copy of the current runtime configuration.
We can update the configuration with identifiers from the the runtime's **device manager**, but these devices won't instantiate until we start acquisition.

Acquire supports up to two video streams.
These streams consist of a **source** (i.e., a camera), optionally a **filter**, and a **sink** (an output, like a Zarr dataset or a Tiff file).
Before configuring the streams, grab the current configuration of the `Runtime` object with:

```python
config = runtime.get_configuration()
```

Video streams are configured independently. Configure the first video stream by setting properties on `config.video[0]` and the second video stream with `config.video[1]`. We'll be using simulated cameras, one generating a radial sine pattern and one generating a random pattern.

```python
config.video[0].camera.identifier = dm.select(acquire.DeviceKind.Camera, "simulated: radial sin")

# how many adjacent pixels in each direction to combine by averaging; here, 1 means not to combine
config.video[0].camera.settings.binning = 1

# how long (in microseconds) your camera should collect light from the sample; for simulated cameras,
# this is just a waiting period before generating the next frame
config.video[0].camera.settings.exposure_time_us = 5e4  # 50 ms

# the data type representing each pixel; here we choose unsigned 8-bit integer
config.video[0].camera.settings.pixel_type = acquire.SampleType.U8

# the shape, in pixels, of the image; width first, then height
config.video[0].camera.settings.shape = (1024, 768)
```


```python
config.video[1].camera.identifier = dm.select(acquire.DeviceKind.Camera, "simulated: uniform random")

# how many adjacent pixels in each direction to combine by averaging; here, 1 means not to combine
config.video[1].camera.settings.binning = 1

# how long (in microseconds) your camera should collect light from the sample; for simulated cameras,
# this is just a waiting period before generating the next frame
config.video[1].camera.settings.exposure_time_us = 1e4  # 10 ms

# the data type representing each pixel; here we choose unsigned 8-bit integer
config.video[1].camera.settings.pixel_type = acquire.SampleType.U8

# the shape, in pixels, of the image; width first, then height
config.video[1].camera.settings.shape = (1280, 720)
```

Now we'll configure each output, or sink device.
For both simulated cameras, we'll be writing to Zarr, a format which supports chunked arrays.


```python
config.video[0].storage.identifier = dm.select(acquire.DeviceKind.Storage, "Zarr")

# what file or directory to write the data to
config.video[0].storage.settings.filename = "output1.zarr"

# where applicable, how large should a chunk file get before opening the next chunk file
config.video[0].storage.settings.chunking.max_bytes_per_chunk = 32 * 2**20  # 32 MiB chunk sizes
```


```python
config.video[1].storage.identifier = dm.select(acquire.DeviceKind.Storage, "Zarr")

# what file or directory to write the data to
config.video[1].storage.settings.filename = "output2.zarr"

# where applicable, how large should a chunk file get before opening the next chunk file
config.video[1].storage.settings.chunking.max_bytes_per_chunk = 64 * 2**20  # 64 MiB chunk sizes
```

Finally, let's specify how many frames to generate for each camera before stopping our simulated acquisition.
We also need to register our configuration with the runtime using the `set_configuration` method.

If you want to let the runtime just keep acquiring effectively forever, you can set `max_frame_count` to `2**64 - 1`.

```python
config.video[0].max_frame_count = 100 # collect 100 frames
config.video[1].max_frame_count = 150 # collect 150 frames

config = runtime.set_configuration(config)
```

!!! note

    If you run this tutorial multiple times, you can clear output from previous runs with:

    ```python
    import os
    import shutil

    if config.video[0].storage.settings.filename in os.listdir("."):
        shutil.rmtree(config.video[0].storage.settings.filename)

    if config.video[1].storage.settings.filename in os.listdir("."):
        shutil.rmtree(config.video[1].storage.settings.filename)
    ```

## Acquire Data

To start aquiring data:

```python
runtime.start()
```

Acquisition happens in a separate thread, so at any point we can check on the status by calling the  `get_state` method.


```python
runtime.get_state()
```

Finally, once we're done acquiring, we call `runtime.stop()`.
This method will wait until you've reached the number of frames to collect specified in `config.video[0].max_frame_count` or `config.video[1].max_frame_count`, whichever is larger.

```python
runtime.stop()
```

## Visualizing the Data with napari

Let's take a look at what we've written.
We'll load each Zarr dataset as a Dask array and inspect its dimensions, then we'll use napari to view it.

```python
import dask.array as da
import napari

data1 = da.from_zarr(config.video[0].storage.settings.filename, component="0")
data1

data2 = da.from_zarr(config.video[1].storage.settings.filename, component="0")

viewer1 = napari.view_image(data1)

viewer2 = napari.view_image(data2)
```

## Conclusion

For more examples of using Acquire, check out our [tutorials page](tutorials/index.md).
