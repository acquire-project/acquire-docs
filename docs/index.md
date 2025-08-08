---
title: Acquire Zarr Streaming
template: home_zarr.html
hide:
    - toc
---

## Background

Cloud-native file streaming solutions (e.g. file writers) are essential for building efficient image data acquisition
workflows, especially when acquiring more data than fits into memory or a single external hard drive.
[Zarr](https://zarr-specs.readthedocs.io/en/latest/specs.html) is a cloud-native data format that supports imaging data
and has strong early adoption within the imaging community. The [Acquire project](https://github.com/acquire-project) developed
this standalone Zarr streaming library with interfaces in both Python and C. This library easily integrates into custom
acquisition workflows since it does not rely on runtime or hardware support.

## Installation

See our [Getting Started](get_started.md) page for installation instructions.

## Guides

<div class="cards">
    <div class="card">
        <h4>Python API Reference</h4>
        <p>A detailed description of the Python API. Assumes understanding of <a href="core_concepts">core concepts</a>.</p>
        <a href="api_reference/zarr_api" class="button">Python API Reference</a>
    </div>
    <div class="card">
        <h4>C API Reference</h4>
        <p>A detailed description of the C API. Assumes understanding of <a href="core_concepts">core concepts</a>.</p>
        <a href="api_reference/c_api" class="button">C API Reference</a>
    </div>
    <div class="card">
        <h4>Examples in Python</h4>
        <p>Code examples demonstrating library usage</p>
        <a href="examples/python_examples" class="button">Python Examples</a>
    </div>
    <div class="card">
        <h4>Examples in C</h4>
        <p>Code examples demonstrating library usage</p>
        <a href="examples/c_examples" class="button">C Examples</a>
    </div>
</div>

## Citing `acquire-zarr`

~~~
authors:
- affiliation: Chan Zuckerberg Initiative (United States)
  family-names: Liddell
  given-names: Alan
- affiliation: Chan Zuckerberg Initiative (United States)
  family-names: Eskesen
  given-names: Justin
- affiliation: Chan Zuckerberg Initiative (United States)
  family-names: Clack
  given-names: Nathan
  orcid: 0000-0001-6236-9282
cff-version: 1.2.0
date-released: '2025-02-06'
doi: 10.5280/zenodo.14828040
license:
- apache-2.0
title: 'acquire-zarr: Software for fast streaming to Zarr on the filesystem or in thecloud'
type: software
~~~

## Acquire Zarr License

`acquire-zarr `is provided under an [Apache 2.0 license](https://github.com/acquire-project/acquire-zarr/blob/main/LICENSE).
[Learn more about the Apache license](https://www.apache.org/licenses/LICENSE-2.0).
