# Storage Device Selection

This tutorial describes the storage device options in `Acquire`.

## Description of Storage Devices

To start, we'll create a `Runtime` object and print the storage device options.

```python
import acquire

# Instantiate a Runtime object
runtime = acquire.Runtime()

# Instantiate a DeviceManager object for the Runtime
dm = runtime.device_manager()

# Print devices in DeviceManager of kind Storage
for device in dm.devices():
    if device.kind == acquire.DeviceKind.Storage:
        print(device)
```
The output of that script will be:

```
<DeviceIdentifier Storage "raw">
<DeviceIdentifier Storage "tiff">
<DeviceIdentifier Storage "trash">
<DeviceIdentifier Storage "tiff-json">
<DeviceIdentifier Storage "Zarr">
<DeviceIdentifier Storage "ZarrBlosc1ZstdByteShuffle">
<DeviceIdentifier Storage "ZarrBlosc1Lz4ByteShuffle">
<DeviceIdentifier Storage "ZarrV3">
<DeviceIdentifier Storage "ZarrV3Blosc1ZstdByteShuffle">
<DeviceIdentifier Storage "ZarrV3Blosc1Lz4ByteShuffle">
```

`Acquire` supports streaming data to [bigtiff](http://bigtiff.org/), [Zarr V2](https://zarr-specs.readthedocs.io/en/latest/v2/v2.0.html), [Zarr V3](https://zarr-specs.readthedocs.io/en/latest/specs.html). For both Zarr V2 and Zarr V3, Acquire provides OME metadata.

Zarr has additional capabilities relative to the basic storage devices, namely _chunking_, _compression_, and _multiscale storage_. You can learn more about the Zarr capabilities in `Acquire` in [the Acquire Zarr documentation](https://github.com/acquire-project/acquire-driver-zarr/blob/main/README.md).

- **raw** - Streams to a raw binary file.

- **tiff** - Streams to a [bigtiff](http://bigtiff.org/) file. Metadata is stored in the `ImageDescription` tag for each frame as a `JSON` string.

- **trash** - Writes nothing. Discards incoming data. Useful for live streaming applications.

- **tiff-json** - Stores the video stream in a [bigtiff](http://bigtiff.org/), and stores metadata in a `JSON` file. Both are located in a folder identified by the `uri` property.

- **Zarr** - Streams data to a [Zarr V2](https://zarr.readthedocs.io/en/stable/spec/v2.html) file with associated metadata.

- **ZarrBlosc1ZstdByteShuffle** - Streams compressed data (_zstd_ codec) to a [Zarr V2](https://zarr.readthedocs.io/en/stable/spec/v2.html) file with associated metadata.

- **ZarrBlosc1Lz4ByteShuffle** - Streams compressed data (_lz4_ codec) to a [Zarr V2](https://zarr.readthedocs.io/en/stable/spec/v2.html) file with associated metadata.

- - **ZarrV3** - Streams data to a [Zarr V3](https://zarr-specs.readthedocs.io/en/latest/specs.html) file with associated metadata.

- **ZarrV3Blosc1ZstdByteShuffle** - Streams compressed data (_zstd_ codec) to a [Zarr V3](https://zarr-specs.readthedocs.io/en/latest/specs.html) file with associated metadata.

- **ZarrV3Blosc1Lz4ByteShuffle** - Streams compressed data (_lz4_ codec) to a [Zarr V3](https://zarr-specs.readthedocs.io/en/latest/specs.html) file with associated metadata.

## Configure the Storage Device

In the example below, the the `tiff` storage device is selected, and the data from one video source will be streamed to a file `out.tif`.

```python
# get the current configuration
config = runtime.get_configuration()

# Select the tiff storage device
config.video[0].storage.identifier = dm.select(acquire.DeviceKind.Storage, "tiff")

# Set the data filename to out.tif in your current directory (provide the whole filetree to save to a different directory)
config.video[0].storage.settings.uri = "out.tif"
```

Before proceeding, complete the `Camera` setup and call `set_configuration` to save those new configuration settings.

[Download this tutorial as a Python script](storage.py){ .md-button .md-button-center }
