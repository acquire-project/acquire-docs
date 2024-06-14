# Livestream to napari

The below script can be used to livestream data to the [napari viewer](https://napari.org/stable/). You may also utilize the `Acquire` napari plugin, which is provided in the package upon install. You can access the plugin in the napari plugins menu once `Acquire` is installed. You can review the [plugin code here](https://github.com/acquire-project/acquire-python/blob/main/python/acquire/__init__.py#L131). You may also stream using other packages such at `matplotlib`.

~~~python
{% include "../examples/livestream_napari.py" %}
~~~

[Download this tutorial as a Python script](../examples/livestream_napari.py){ .md-button .md-button-center }
