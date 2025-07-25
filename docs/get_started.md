# Getting started

You can use `acquire-zarr` to stream data in either Python or C/C++ programs.
This document provides a quick overview of how to get started with both languages.

> [!TIP]
> New to Zarr streaming? Check out our [Core concepts](core_concepts.md) page to understand the key terminology used throughout this guide.

## Get Started with Python

### Install the Python library

The `acquire-zarr` Python library is compatible with Python versions 3.9-3.13.

To install the library on Windows, macOS, or Ubuntu, run the following command:

```bash
python -m pip install acquire-zarr
```

We recommend installing `acquire-zarr` in a fresh conda environment or virtualenv.
For example, to install `acquire-zarr` in a conda environment named `acquire`:

```shell
conda create -n acquire python #compatible with python 3.9-3.13
conda activate acquire
python -m pip install acquire-zarr
```

or with virtualenv:

```shell
$ python -m venv venv
$ . ./venv/bin/activate # or on Windows: .\venv\Scripts\Activate.bat or .\venv\Scripts\Activate.ps1
(venv) $ python -m pip install acquire-zarr
```

Once you have `acquire-zarr` installed, simply call `import acquire_zarr` in your script, notebook, or module to start utilizing the package.

```python
import acquire_zarr
```

#### Usage

The library provides two main classes. First, `ZarrStream`, representing an output stream to a Zarr dataset.
Second, `ZarrStreamSettings` to configure a Zarr stream.

A typical use case for a 4-dimensional acquisition in Python might look like this:

```python
import acquire_zarr as aqz
import numpy as np

settings = aqz.StreamSettings(
    store_path="my_stream.zarr",
    data_type=aqz.DataType.UINT16,
    version=aqz.ZarrVersion.V3
)

settings.dimensions.extend([
    aqz.Dimension(
        name="t",
        type=aqz.DimensionType.TIME,
        array_size_px=0,
        chunk_size_px=100,
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
])

# Generate some random data: one time point, all channels, full frame
my_frame_data = np.random.randint(0, 2**16, (3, 1080, 1920), dtype=np.uint16)

stream = aqz.ZarrStream(settings)
stream.append(my_frame_data)
```
### Build Python Bindings from Source

The library must be built from source to contribute to the latest development version or to customize the installation for your system.
To build the Python bindings from source, follow [these instructions](https://github.com/acquire-project/acquire-zarr/blob/main/README.md#building).

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
