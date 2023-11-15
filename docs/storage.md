# Storage Device Selection

This tutorial illustrates the storage device options in `Acquire`.

## Description of Storage Devices

To start, we'll create a `Runtime` object and print the storage device options.

```python
import acquire 

# Instantiate a Runtime object
runtime = acquire.Runtime()

# Instantiate a DeviceManager object for the Runtime
manager = runtime.device_manager()

# Print devices in DeviceManager of kind Storage
for device in manager.devices():
    if device.kind == acquire.DeviceKind.Storage:
        print(device)
```
The output of that script will be:

```
# Storage Devices printed

<DeviceIdentifier Storage "raw">
<DeviceIdentifier Storage "tiff">
<DeviceIdentifier Storage "trash">
<DeviceIdentifier Storage "tiff-json">
<DeviceIdentifier Storage "Zarr">
<DeviceIdentifier Storage "ZarrBlosc1ZstdByteShuffle">
<DeviceIdentifier Storage "ZarrBlosc1Lz4ByteShuffle">
```
- **raw** - Streams to a raw binary file.
- **tiff** - Streams to a [bigtiff](http://bigtiff.org/) file. Metadata is stored in the `ImageDescription` tag for each frame as a `JSON` string.
- **trash** - Writes nothing. Discards incoming data. Useful for live streaming applications.
- **tiff-json** - Stores the video stream in a [bigtiff](http://bigtiff.org/), and stores metadata in a `JSON` file. Both are located in a folder identified by the `filename` property.
- **Zarr** - Streams data to a [Zarr V2](https://zarr.readthedocs.io/en/stable/spec/v2.html) file with associated metadata.
- **ZarrBlosc1ZstdByteShuffle** - Streams compressed data (_zstd_ codec) to a [Zarr V2](https://zarr.readthedocs.io/en/stable/spec/v2.html) file with associated metadata. 
- **ZarrBlosc1Lz4ByteShuffle** - Streams compressed data (_lz4_ codec) to a [Zarr V2](https://zarr.readthedocs.io/en/stable/spec/v2.html) file with associated metadata.

`Acquire` supports streaming data to [bigtiff](http://bigtiff.org/) and [Zarr V2](https://zarr.readthedocs.io/en/stable/spec/v2.html). 

Zarr has additional capabilities relative to the basic storage devices, namely _chunking_, _compression_, and _multiscale storage_. You can learn more about the Zarr capabilities in `Acquire` [here](https://github.com/acquire-project/acquire-driver-zarr).

## Select the Storage Device and Specify where to Store the Data

We'll use our instance of `Runtime` and specify that the data from one video source should be streamed to a file `out.tif` in the example below:

```python
# get the current configuration
config = runtime.get_configuration()

# Select the tiff storage device
config.video[0].storage.identifier = manager.select( acquire.DeviceKind.Storage, "tiff")

# Set the data filename to out.tif in your current directory (provide the whole filetree to save to a different directory)
config.video[0].storage.settings.filename = "out.tif" 
```

Before proceeding, complete the `Camera` setup and call `runtime.set_configuration(config)` to save those new configuration settings.