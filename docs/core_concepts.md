# Core concepts

The following sections describe the core concepts and terminology used in the acquire-zarr library.
See the [Concepts and terminology](https://zarr-specs.readthedocs.io/en/latest/v3/core/index.html#concepts-and-terminology) section of the Zarr V3 specification for more details.

![Diagram of Zarr V3 concepts](https://zarr-specs.readthedocs.io/en/latest/_images/terminology-hierarchy.excalidraw.png)

## Zarr

Zarr is a specification for storing large, multi-dimensional arrays in a "cloud-ready" format, i.e., one which is designed to be efficient for both local and remote storage.
Arrays are stored as a grid of chunks, which are (optionally) compressed blocks of data that can be accessed independently.
Zarr supports multiple storage backends, including local filesystems and cloud storage services like S3.
There are two major versions of the Zarr specification: [V2](https://zarr-specs.readthedocs.io/en/latest/v2/v2.0.html) and [V3](https://zarr-specs.readthedocs.io/en/latest/v3/core/index.html).
The acquire-zarr library implements both specifications.

> [!WARNING]
> The V2 specification is currently deprecated and will be removed in a future release.
> We recommend using V3 for new projects.

## OME-Zarr

The [OME-Zarr](https://ngff.openmicroscopy.org/latest/) specification is an extension of the Zarr specification that adds support for additional metadata and multiscale arrays.

## Stream

A *stream* is the primary interface for writing data to Zarr arrays in acquire-zarr.
The stream manages the process of organizing incoming data into chunks and shards, applying compression, and writing to the underlying storage backend.

> [!NOTE]
> acquire-zarr is designed to be used in a streaming fashion, meaning you can append data to the stream incrementally.
> This is particularly useful for large datasets that cannot be loaded into memory all at once.
> This means that random-access writing, i.e., writing to arbitrary locations in the array, is not supported; neither is reading from the stream.
> While this is limiting in some use cases, it provides several advantages:
> - **High throughput**: acquire-zarr is optimized for high-speed data acquisition, allowing you to write large amounts of data quickly.
> - **Low memory usage**: acquire-zarr does not require loading the entire dataset into memory, making it suitable for large datasets.
> - **Real-time data acquisition**: acquire-zarr is designed for real-time data acquisition, allowing you to write data as it is generated.

You configure a stream by specifying one or more arrays, their dimensions, and storage settings.
Once created, you can append data to the stream, and acquire-zarr handles all the details of chunking, compression, and storage.

## Storage

### Store

When we refer to a *store*, we mean a Zarr store, which is a hierarchical key-value store that can be used to store Zarr datasets.
The store can be local (on disk) or remote (e.g., in cloud storage).
We sometimes use this term interchangeably with "Zarr dataset" when the context is clear.
The store contains child *nodes*, which can be either *arrays* or *groups*.

### Array

By *array* we mean a multi-dimensional array that can be stored as a child node in a Zarr store.
Arrays can have any number of dimensions and can consist of one of several data types supported by acquire-zarr.
Those data types are:

- Unsigned integral types:
  - `uint8`
  - `uint16`
  - `uint32`
  - `uint64`
- Signed integral types:
  - `int8`
  - `int16`
  - `int32`
  - `int64`
- Floating-point types:
  - `float32`
  - `float64`

#### Multiscale arrays

In acquire-zarr, arrays may be *multiscale* (see below), meaning they can store data at multiple resolutions or scales.
Multiscale arrays are represented in the hierarchy as a group containing multiple arrays, each representing a different scale, e.g.,

```plaintext
my_array.zarr/
    ├── 0/
    │   └── ... (data)
    ├── 1/
    │   └── ... (data)
    └── 2/
        └── ... (data)
```

An image in the array at scale 0 is the full resolution image, while at scale `n`, the image is downsampled by a factor of `2^n` in x, y, and, if applicable, z.
See [Dimensions](#dimensions) below for more information.

#### Output key

The *output key* is the path within a Zarr store where an array is located.
This allows you to organize multiple arrays within a single store using a hierarchical structure.
For example, you might use output keys like `"sample1/brightfield"` and `"sample1/fluorescence"` to organize different imaging modalities for the same sample, or you might additionally have a `"labels"` array for segmentation data.

### Group

A *group* is a node in a Zarr store that may contain other nodes, such as arrays or other groups.

### S3 storage

The acquire-zarr library can work with S3-compatible storage backends.
When using S3, the Zarr store is represented as a hierarchy of objects in an S3 bucket.
Each object corresponds to a node in the Zarr store, and the hierarchy is maintained using prefixes in the object keys.

```plaintext
s3://my-bucket/my_array.zarr/
    ├── 0/
    │   └── ... (data)
    ├── 1/
    │   └── ... (data)
    └── 2/
        └── ... (data)
```

## Dimensions, chunking, and sharding

### Dimension

A *dimension* is a named axis of an array that can be used to organize and access the data within the array.
Each dimension has a name, a type, and a size.
The dimension type can be one of the following:

- Time
- Channel
- Space (e.g., x, y, z)
- Other (custom types can be defined)

When creating a stream with acquire-zarr, you must specify *at least 3* dimensions: a spatial dimension X, a spatial dimension Y, and a third dimension of any type.
Apart from this constraint, you can define as many dimensions of any type as you like, though you should keep in mind that if you are targeting the OME-Zarr specification, there are [some constraints on the types and order](https://ngff.openmicroscopy.org/latest/#multiscale-md) of your dimensions.

When you configure a dimension in acquire-zarr, you must specify the following properties:
- `name`: The name of the dimension (e.g., "t", "c", "z", "y", "x")
- `type`: The type of the dimension (as above)
- `array_size_px`: The size of the array in pixels for this dimension
- `chunk_size_px`: The size of the chunk (see below) in pixels for this dimension
- `shard_size_chunks`: The size of the shard (see below) in chunks for this dimension (Zarr V3 only)

Dimensions are configured in order of *slowest changing* to *fastest changing*.
For example, if you have a 4D array with dimensions time, channel, y, and x, you would configure the dimensions in that order.

#### Append dimension

The *append dimension* is the slowest-varying dimension in the array, meaning it is the dimension that changes the least frequently as you append data to the stream.
It is called the append dimension because it is the dimension that grows dynamically as you append new data to the stream, with no predetermined limit.
In the example above, the append dimension is the time dimension.
You can set `array_size_px` to any value for this dimension, but it will be ignored in favor of the actual size of the data you append to the stream, so it's typical to set it to 0.
Append dimensions are usually time or spatial dimensions, but can be any type.

### Chunk

A *chunk* is a contiguous block of data within an array that is stored together.
Chunks are used to optimize data access and storage efficiency, and are considered *compressible units*.
When you stream data to an array, acquire-zarr will automatically divide the data into chunks based on the chunk size specified in the stream settings.

When you configure a dimension in acquire-zarr, you must specify the chunk size, in pixels, for that dimension.
The chunk size for a given dimension need not evenly divide the array size for that dimension.
Such a dimension is said to be *ragged* in its chunking.

For example, if you have an array with a size of 1080 pixels in the Y dimension and a chunk size of 256 pixels, the array will be divided into 5 chunks, 4 of which will be of size 256 pixels and the last one will be of size 1080 - 4 * 256 = 56 pixels.

### Shard

A *shard* is a contiguous group of chunks (a superchunk, if you will) that are stored together in a single object in the Zarr store.
Sharding is used to optimize data access and storage efficiency, especially for large arrays.
When you stream data to an array, acquire-zarr will automatically divide the data into chunks as above, and then aggregate those chunks into shards based on the shard size specified in the stream settings.

When you configure a dimension in acquire-zarr, you must specify the shard size, in units of chunks, for that dimension.
The shard size for a given dimension need not evenly divide the number of chunks for that dimension.
For example, if you have an array with 10 chunks in the Y dimension and a shard size of 3 chunks, the array will be divided into 4 shards, 3 of which will contain 3 chunks and the last one will contain 1 chunk.

## Compression

Zarr supports compression of chunks to reduce storage space and improve data transfer speeds.
When you stream data to an array, acquire-zarr can compress the chunks based on the compression settings specified in the stream settings.
Because acquire-zarr uses [Blosc](https://www.blosc.org/pages/blosc-in-depth/) for compression, it supports multiple compression codecs, including LZ4 and Zstandard.
You can also specify the compression level, 0-9, where 0 means no compression and 9 means maximum compression, and the shuffle filter, which can be used to improve compression ratios for certain data types.
(See this article for a discussion of the shuffle filter: [New 'bitshuffle' filter](https://www.blosc.org/posts/new-bitshuffle-filter/).)

## Write behavior

The timing of when data is written to storage depends on the storage backend:

- **Filesystem**: Data is written when chunks are complete, allowing for efficient streaming of large datasets.
- **S3**: Because S3 objects cannot be appended to, data is written when entire shards are complete. This means you may need to configure larger shards when using S3 to avoid frequent uploads. However, you should take care not to make shards too large, as this can lead to inefficient storage and retrieval.