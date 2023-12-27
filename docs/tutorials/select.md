# Device Selection

This tutorial illustrates the difference between the `select` and `select_one_of` methods in the `DeviceManager` class. `select` chooses the first discovered device of a specific kind, camera or storage device. You can also, optionally, select a specific device by passing the device name as a string to `select`. Whereas, `select_one_of` requires that you specify both the kind of device to select and a list of possible device names. `select_one_of` will iterate through the list and select the first device in the list of names that is discovered on your machine.

To start, instantiate `Runtime` and `DeviceManager` objects and subsequently print the discovered devices.

```python
import acquire

# Instantiate a Runtime object
runtime = acquire.Runtime()

# Instantiate a DeviceManager object for the Runtime
manager = runtime.device_manager()

# List devices discovered by DeviceManager
for device in manager.devices():
    print(device)
```

Output of the above code is below:

```
<DeviceIdentifier Camera "simulated: uniform random">
<DeviceIdentifier Camera "simulated: radial sin">
<DeviceIdentifier Camera "simulated: empty">
<DeviceIdentifier Storage "raw">
<DeviceIdentifier Storage "tiff">
<DeviceIdentifier Storage "trash">
<DeviceIdentifier Storage "tiff-json">
<DeviceIdentifier Storage "Zarr">
<DeviceIdentifier Storage "ZarrBlosc1ZstdByteShuffle">
<DeviceIdentifier Storage "ZarrBlosc1Lz4ByteShuffle">
```

All identified devices will be listed, and in the case of this tutorial, no cameras were connected to the machine, so only simulated cameras were found. Note that discovered storage devices will also print.

The order of those printed devices matters. Below are two examples of how the `select` method works. In the first, without a specific device name provided, `select` will choose the first device of the specified kind in the list of discovered devices. In the second example, a specific device name is provided, so `select` will grab that device if it was discovered by `Runtime`.

```python
# specify that the device should be a camera and not a storage device
kind = acquire.DeviceKind.Camera

# 1st example: select the first camera in the list of discovered devices
selected = manager.select(kind)

# 2nd example: select a specific camera
specific = manager.select(kind, "simulated: empty")

# print the 2 devices
print(selected)
print(specific)
```
The output of the code is below:
```
<DeviceIdentifier Camera "simulated: uniform random">
<DeviceIdentifier Camera "simulated: empty">
```

The `select_one_of` method allows more flexibility since you provide a list of names of acceptable devices for it to iterate through until a discovered device is located.

```python
# specify that the device should be a camera and not a storage device
kind = acquire.DeviceKind.Camera

selected = manager.select_one_of(kind, ["Hamamatsu_DCAMSDK4_v22126552",
    "simulated: radial sin", "simulated: empty"])

# print which camera was selected
print(selected)
```
The output of the code is below. The Hamamatsu camera was not discovered by `Runtime`, so `select_one_of` iterates until it finds a device discovered by `Runtime`. In this case, the next item in the list is a simulated camera that was discovered by `Runtime`.
```
<DeviceIdentifier Camera "simulated: radial sin">
```

[Download this tutorial as a Python script](select.py){ .md-button .md-button-center }
