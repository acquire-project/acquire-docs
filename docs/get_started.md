# Getting started

You can use `acquire-zarr` to stream data in either Python or C/C++ programs.
This document provides a quick overview of how to get started with both languages.

> [!TIP]
> New to Zarr streaming? Check out our [Core concepts](core_concepts.md) page to understand the key terminology used throughout this guide.

## Getting started with Python

### Installation

The `acquire-zarr` Python library is supported for Python versions 3.9-3.13.

To install the library on Windows, macOS, or Linux, run the following command, after ensuring that the `python` command points to the correct Python version you want to use:

```bash
python -m pip install acquire-zarr
```

We recommend installing `acquire-zarr` in a fresh conda environment or virtualenv.
For example, to install `acquire-zarr` in a conda environment named `acquire`:

```shell
conda create -n acquire python=3.13 # or python=3.12, python=3.11, etc.
conda activate acquire
python -m pip install acquire-zarr
```

or with virtualenv:

```shell
$ python -m venv venv
$ . ./venv/bin/activate # or on Windows: .\venv\Scripts\Activate
(venv) $ python -m pip install acquire-zarr
```

Now in your scripts or notebooks, import acquire-zarr with:

```python
import acquire_zarr as aqz # or simply `import acquire_zarr`
```

### Usage

The typical workflow for acquiring data in Python is to create a stream by configuring it with the desired settings, and then to append data to the stream.

The *stream* represents a Zarr dataset that can be written to.
You can write data to one or more *arrays* in the stream, where each array corresponds to a separate subset of the data.
For example, you might have a stream for a multi-camera acquisition, where each camera's data is stored in a separate array.

Here's how you might configure a stream for a 4-dimensional acquisition (time, channel, height, width) with a single array and append data to it:

```python
import acquire_zarr as aqz
import numpy as np

settings = aqz.StreamSettings(
    store_path="my_stream.zarr",
    version=aqz.ZarrVersion.V3,
    overwrite=True,  # this will remove any existing data at my_stream.zarr
    arrays=[
        aqz.ArraySettings(
            output_key="array1",
            data_type=np.uint16,
            dimensions = [
                aqz.Dimension(
                    name="t",
                    type=aqz.DimensionType.TIME,
                    array_size_px=0,
                    chunk_size_px=32,
                    shard_size_chunks=10
                ),
                aqz.Dimension(
                    name="c",
                    type=aqz.DimensionType.CHANNEL,
                    array_size_px=3,
                    chunk_size_px=1,
                    shard_size_chunks=1
                ),
                aqz.Dimension(
                    name="y",
                    type=aqz.DimensionType.SPACE,
                    array_size_px=1080,
                    chunk_size_px=270,
                    shard_size_chunks=2
                ),
                aqz.Dimension(
                    name="x",
                    type=aqz.DimensionType.SPACE,
                    array_size_px=1920,
                    chunk_size_px=480,
                    shard_size_chunks=2
                )
            ]
        )
    ]
)

# Generate some random data: one time point, all channels, full frame
my_frame_data = np.random.randint(0, 2 ** 16, (3, 1080, 1920), dtype=np.uint16)

stream = aqz.ZarrStream(settings)
stream.append(my_frame_data)

# ... append more data as needed ...

# When done, close the stream to flush any remaining data
stream.close()
```

When all is said and done, the data will be stored in a Zarr dataset on disk at `my_stream.zarr`, which can be read by any Zarr-compatible library.
It will contain one array named `array1` with the data organized in the specified dimensions according to the chunk and shard layout you specified.

If you instead had a multichannel acquisition with both brightfield and fluorescence channels, you could create a stream with two arrays, one for each channel type:

```python
import acquire_zarr as aqz
import numpy as np

# configure the stream with two arrays
settings = aqz.StreamSettings(
    store_path="experiment.zarr",
    version=aqz.ZarrVersion.V3,
    overwrite=True,  # this will remove any existing data at experiment.zarr
    arrays=[
        aqz.ArraySettings(
            output_key="sample1/brightfield",
            data_type=np.uint16,
            dimensions=[
                aqz.Dimension(
                    name="t",
                    type=aqz.DimensionType.TIME,
                    array_size_px=0,
                    chunk_size_px=100,
                    shard_size_chunks=1
                ),
                aqz.Dimension(
                    name="c",
                    type=aqz.DimensionType.CHANNEL,
                    array_size_px=1,
                    chunk_size_px=1,
                    shard_size_chunks=1
                ),
                aqz.Dimension(
                    name="y",
                    type=aqz.DimensionType.SPACE,
                    array_size_px=1080,
                    chunk_size_px=270,
                    shard_size_chunks=2
                ),
                aqz.Dimension(
                    name="x",
                    type=aqz.DimensionType.SPACE,
                    array_size_px=1920,
                    chunk_size_px=480,
                    shard_size_chunks=2
                )
            ]
        ),
        aqz.ArraySettings(
            output_key="sample1/fluorescence",
            data_type=np.uint16,
            dimensions=[
                aqz.Dimension(
                    name="t",
                    type=aqz.DimensionType.TIME,
                    array_size_px=0,
                    chunk_size_px=100,
                    shard_size_chunks=1
                ),
                aqz.Dimension(
                    name="c",
                    type=aqz.DimensionType.CHANNEL,
                    array_size_px=2,  # two fluorescence channels
                    chunk_size_px=1,
                    shard_size_chunks=1
                ),
                aqz.Dimension(
                    name="y",
                    type=aqz.DimensionType.SPACE,
                    array_size_px=1080,
                    chunk_size_px=270,
                    shard_size_chunks=2
                ),
                aqz.Dimension(
                    name="x",
                    type=aqz.DimensionType.SPACE,
                    array_size_px=1920,
                    chunk_size_px=480,
                    shard_size_chunks=2
                )
            ]
        )
    ]
)

stream = aqz.ZarrStream(settings)

# ... append data ...
brightfield_frame_data = ... # define your brightfield frame data here
fluorescence_frame_data = ... # define your fluorescence frame data here

stream.append(brightfield_frame_data, key="sample1/brightfield")
stream.append(fluorescence_frame_data, key="sample1/fluorescence")

# ... append more data as needed ...

# When done, close the stream to flush any remaining data
stream.close()
```

### Building the Python library from source

If you want to [contribute](for_contributors/index.md) to acquire-zarr, or customize the installation for your own system, you'll need to be able to build the Python bindings from source.
The first step is to install the system dependencies as found in the ["Installing dependencies" section](https://github.com/acquire-project/acquire-zarr/blob/main/README.md#installing-dependencies) of the README.md file in the `acquire-zarr` repository.
In your Python environment, you also need the following dependencies:

- cmake<4.0.0
- ninja
- pybind11[global]
- setuptools
- wheel

You can install these dependencies with:

```bash
python -m pip install cmake<4.0.0 ninja pybind11[global] setuptools wheel
```

Then, clone the `acquire-zarr` repository and install acquire-zarr in your Python environment:
```
git clone --recursive https://github.com/acquire-project/acquire-zarr.git
cd acquire-zarr
python -m pip install .
```

## Get Started with C Bindings

### Install the C Library

The `acquire-zarr` C library is distributed as a binary and headers, which you can download for your system from our [Releases page](https://github.com/acquire-project/acquire-zarr/releases). You will also need to install the following dependencies:

  - [c-blosc](https://github.com/Blosc/c-blosc) >= 1.21.5
  - [nlohmann-json](https://github.com/nlohmann/json) >= 3.11.3
  - [minio-cpp](https://github.com/minio/minio-cpp)  >= 0.3.0
  - [crc32c](https://github.com/google/crc32c) >= 1.1.2

We suggest using [vcpkg](https://github.com/microsoft/vcpkg) or another package manager to handle dependencies.

[Here](https://github.com/acquire-project/acquire-zarr/blob/main/examples/CMakeLists.txt) is an example CMakeLists.txt file of C executables using acquire-zarr.

#### Usage

The library provides two main structs. First, `ZarrStream`, representing an output stream to a Zarr dataset.
Second, `ZarrStreamSettings` to configure a Zarr stream.

A typical use case for a 4-dimensional acquisition in C might look like this:

```c
#include "acquire.zarr.h"
#include "assert.h"

int main() {
    ZarrStreamSettings settings = (ZarrStreamSettings){
        .store_path = "my_stream.zarr",
        .data_type = ZarrDataType_uint16,
        .version = ZarrVersion_3,
    };

    ZarrStreamSettings_create_dimension_array(&settings, 4);
    settings.dimensions[0] = (ZarrDimensionProperties){
        .name = "t",
        .type = ZarrDimensionType_Time,
        .array_size_px = 0,      // this is the append dimension
        .chunk_size_px = 100,    // 100 time points per chunk
        .shard_size_chunks = 10, // 10 chunks per shard
    };

    settings.dimensions[1] = (ZarrDimensionProperties){
        .name = "c",
        .type = ZarrDimensionType_Channel,
        .array_size_px = 3,     // 3 channels
        .chunk_size_px = 1,     // 1 channel per chunk
        .shard_size_chunks = 1, // 1 chunk per shard
    };

    settings.dimensions[2] = (ZarrDimensionProperties){
        .name = "y",
        .type = ZarrDimensionType_Space,
        .array_size_px = 1080,  // height
        .chunk_size_px = 270,   // 4 x 4 tiles of size 270 x 480
        .shard_size_chunks = 2, // 2 x 2 tiles per shard
    };

    settings.dimensions[3] = (ZarrDimensionProperties){
        .name = "x",
        .type = ZarrDimensionType_Space,
        .array_size_px = 1920,  // width
        .chunk_size_px = 480,   // 4 x 4 tiles of size 270 x 480
        .shard_size_chunks = 2, // 2 x 2 tiles per shard
    };

    ZarrStream* stream = ZarrStream_create(&settings);

    size_t bytes_written;
    ZarrStream_append(stream, my_frame_data, my_frame_size, &bytes_written);
    assert(bytes_written == my_frame_size);
}
```

Look at [acquire.zarr.h](include/acquire.zarr.h) for more details.

### Building the C Library from Source

The library must be built from source to contribute to the latest development version or to incorporate the library into an existing program.
To build the C library from source, follow [these instructions](https://github.com/acquire-project/acquire-zarr/blob/main/README.md#building).
