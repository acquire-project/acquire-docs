# [Acquire](https://github.com/acquire-project/acquire-python) Documentation

Check out the built site here: https://acquire-project.github.io/acquire-docs/

This repository contains the documentation for [Acquire](https://github.com/acquire-project/acquire-python) (`acquire-imaging` on [PyPI](https://pypi.org/project/acquire-imaging/)), a python package providing a multi-camera video streaming library focusing on performant microscopy..

If you'd like to make a suggestion for new documentation, please submit a [Github issue](https://github.com/acquire-project/acquire-docs/issues/new) to let us know.

## Contribute

We welcome contributions to the Acquire code base and to documentation. Refer to our [contribution guides](https://acquire-project.github.io/acquire-docs/for_contributors/) for more information. The relevant Github repos are linked below.

- [`Acquire` project](https://github.com/acquire-project)
- [`acquire-imaging`](https://github.com/acquire-project/acquire-python)
- [`Acquire` documentation](https://github.com/acquire-project/acquire-docs)

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
