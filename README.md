# [Acquire](https://github.com/acquire-project) Documentation

This repository contains the documentation for [acquire-zarr](https://github.com/acquire-project/acquire-zarr) ([PyPI](https://pypi.org/project/acquire-zarr/)), a C++ library and Python package providing performant streaming to Zarr V3 and Zarr V2 on filesystem or S3. The built site may be viewed at [acquire-project.github.io/acquire-docs](https://acquire-project.github.io/acquire-docs/).

If you'd like to make a suggestion for new documentation, please submit a [Github issue](https://github.com/acquire-project/acquire-docs/issues/new).

## Contribute

We welcome contributions to the Acquire code base and to documentation. Refer to our [contribution guides](https://acquire-project.github.io/acquire-docs/for_contributors/) for more information.
The relevant Github repos are linked below.

- [Acquire project](https://github.com/acquire-project)
- [acquire-zarr](https://github.com/acquire-project/acquire-zarr)
- [Acquire documentation](https://github.com/acquire-project/acquire-docs)

### Discontinued projects

The following projects are no longer maintained but are still linked for reference:

- [acquire-imaging](https://github.com/acquire-project/acquire-python) (PyPI: [acquire-imaging](https://pypi.org/project/acquire-imaging/))
- [acquire-common](https://github.com/acquire-project/acquire-common)
- [acquire-driver-zarr](https://github.com/acquire-project/acquire-driver-zarr)
- [acquire-driver-spinnaker](https://github.com/acquire-project/acquire-driver-spinnaker)
- [acquire-driver-hdcam](https://github.com/acquire-project/acquire-driver-hdcam)
- [acquire-driver-egrabber](https://github.com/acquire-project/acquire-driver-egrabber)
- [acquire-driver-pvcam](https://github.com/acquire-project/acquire-driver-pvcam)

## Build

To build the website locally and serve it, follow the steps below:

1. Install `Doxygen` using your package manager or from the
   [official website](https://www.doxygen.nl/index.html).
2. after cloning and successfully installing `acquire-imaging` and
   `acquire-zarr` in developer mode, run the following commands:

    ```bash
    pip install -r requirements.txt
    mkdocs serve
    ```

> [!NOTE]
> This setup assumes you have acquire-python and acquire-zarr cloned in the same
> parent directory as acquire-docs. If this is not the case, edit the
> [`mkdocs.yml` file](https://github.com/acquire-project/acquire-docs/blob/main/mkdocs.yml) accordingly.
