# API Reference

Information on the classes in `acquire-imaging` along with the attributes and methods associated with them.

## Class `AvailableData`

The `AvailableData` class represents the collection of frames that have been captured since the last call to runtime.get_available_data(). `AvailableData` objects should be set to have a short lifetime, since these objects reserve space on the video queue and will eventually block camera acquisition to ensure no data is overwritten before it can be processed.

```python
class AvailableData:
    def frames(self) -> Iterator[VideoFrame]:
    """Returns an iterator over the video frames in the available data."""

    def get_frame_count(self) -> int:
    """Returns the total number of video frames in the available data."""

    def __iter__(self) -> Iterator[VideoFrame]:
    """Returns an iterator over the video frames in the available data."""
```

- The `frames` method provides an iterator over these frames.

- Call `get_frame_count()` to query the number of frames in an `AvailableData` object.

- The `__iter__` method enables `AvailableData` objects to be iterated.

## Class `AvailableDataContext`

The `AvailableDataContext` class is the context manager for available data for the given VideoStream ID.

```python
class AvailableDataContext:
    def __enter__(self) -> AvailableData: ...
    """Get the available data from the runtime and return it."""

    def __exit__(
        self, exc_type: Any, exc_value: Any, traceback: Any
    ) -> None: ...
    """Clean up any references to the available data returned when entering this context."""
```

## Class `Camera`
The `Camera` class is used to describe cameras or other video sources.

```python
class Camera:
    identifier: Optional[DeviceIdentifier]
    settings: CameraProperties

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    """Initializes a Camera object with optional arguments."""

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the Camera attributes."""
```

- `identifier`: An optional attribute which contains an instance of the `DeviceIdentifier` class. `DeviceIdentifier` has `id` and `kind` attributes assigned by `Acquire` if the device is natively supported. Otherwise, it is of type `None`.

- `settings`: An instance of the `CameraProperties` class which contains the settings for the camera.

- The `dict` method creates a dictionary of a `Camera` object's attributes.

## Class `CameraCapabilities`
The `CameraCapabilities` class is used to describe the camera’s supported properties.

```python
class CameraCapabilities:
    exposure_time_us: Property
    line_interval_us: Property
    readout_direction: Property
    binning: Property
    offset: OffsetShapeCapabilities
    shape: OffsetShapeCapabilities
    supported_pixel_types: List[SampleType]
    digital_lines: DigitalLineCapabilities
    triggers: TriggerCapabilities

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the CameraCapabilities attributes."""
```

- `exposure_time_us`: An instance of the `Property` class that captures the range and type of supported values in microseconds for the camera's exposure time, which is how long in microseconds the camera collects light from the sample for a single frame.
  
- `line_interval_us`: An instance of the `Property` class that captures the range and type of supported values in microseconds for a rolling shutter camera to scan one line.
  
- `readout_direction`: An instance of the `Property` class that specifies whether the data is read out of the camera forwards or backwards and if that direction can be chosen by the user.
  
- `binning`: An instance of the `Property` class that captures the range and type of support values for binning, which is combining adjacent pixels by averaging in each direction, and whether the binning factor can be chosen by the user.
  
- `offset`: An instance of the `OffsetShapeCapabilities` class that represents the horizontal and vertical offset for the region of interest on the camera chip.
  
- `shape`: An instance of the `OffsetShapeCapabilities` class that represents the width and height of the region of interest on the camera chip.
  
- `supported_pixel_types`: A list containing instances of the `SampleType` class representing each of the supported pixel types, such as 8-bit unsigned integer (uint8). 
  
- `digital_lines`: An instance of the `DigitalLineCapabilities` class which indicates the number and names of the available lines. Up to 8 lines are supported with the last line typically being the camera software trigger.
  
- `triggers`: An instance of the `TriggerCapabilities` class which indicate what kinds of triggers (start acquisition, start exposure, or start a frame) are supported.

- The `dict` method create a dictionary of a `CameraCapabilities` object's attributes.


## Class `CameraProperties`
The `CameraProperties` class is used to set the desired camera properties for acquisition.

```python
class CameraProperties:
    exposure_time_us: float
    line_interval_us: float
    binning: float
    pixel_type: SampleType
    readout_direction: Direction
    offset: Tuple[int, int]
    shape: Tuple[int, int]
    input_triggers: InputTriggers
    output_triggers: OutputTriggers

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    """Initializes a CameraProperties object with optional arguments."""

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the CameraProperties attributes."""
```

- `exposure_time_us`: How long in microseconds your camera should collect light from the sample. However, for simulated cameras, this is just a waiting period before generating the next frame.

- `line_interval_us`: The time to scan one line in microseconds in a rolling shutter camera.

- `binning`: How many adjacent pixels in each direction to combine by averaging. For example, if `binning` is set to 2, a 2x2 square of pixels will be combined by averaging. If `binning` is set to 1, no pixels will be combined.

- `pixel_type`: An instance of the `SampleType` class which specifies the numerical data type, for example Uint16, a 16-bit unsigned integer type.

- `readout_direction`: An instance of the `Direction` class which specifies whether the data is readout forwards or backwards.

- `offset`: A tuple of two integers representing the (x, y) offset in pixels of the image region of interest on the camera.

- `shape`: A tuple of two integers representing the (x, y)size in pixels of the image region of interest on the camera.

- `input_triggers`: An instance of the `InputTriggers` class, which describes the trigger signals for starting acquisition, camera exposure, and acquiring a frame.

- `output_triggers`: An instance of the `OutputTriggers` class, which describes the trigger signals for the camera exposure, acquiring a frame, as well as any wait times for sending the trigger signal.

- The `dict` method create a dictionary of a `CameraProperties` object's attributes.

## Class `Capabilities`

The `Capabilities` class contains representations of each of the 2 supported VideoStream objects.

```python
class Capabilities:
    video: Tuple[VideoStreamCapabilities, VideoStreamCapabilities]

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    """Initializes a Capabilities object with optional arguments."""

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the Capabilities attributes."""
```

- `video`: A tuple containing two `VideoStreamCapabilities` instances since `Acquire` supports simultaneous streaming from 2 video sources. 

- The `dict` method creates a dictionary of a `Capabilities` object's attributes. 

## Class `DeviceIdentifier`
The `DeviceIdentifier` class represents an identifier for a supported device, including its unique id and type, such as a camera or storage.

```python
class DeviceIdentifier:
    id: Tuple[int, int]
    kind: DeviceKind
    name: str

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    """Initializes a DeviceIdentifier object with optional arguments."""

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the DeviceIdentifier attributes."""

    @staticmethod
    def none() -> DeviceIdentifier: ...
    """Returns a "None" type DeviceIdentifier.
    Useful when a DeviceIdentifier is not needed."""

    def __eq__(self, other: object) -> bool:
    """Checks if two DeviceIdentifier objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this DeviceIdentifier is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this DeviceIdentifier is greater than another."""

    def __le__(self, other: object) -> bool:
    """Checks if this DeviceIdentifier is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this DeviceIdentifier is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two DeviceIdentifier objects are not equal."""
```

- `id`: A tuple (driver_id, device_id) containing two Uint8 integers that serve to identify each driver and device uniquely for a given run.

- `kind`: An instance of the `DeviceKind` class that represents the type or kind of the device.

- `name`: A string representing the name or label of the device.

- The `dict` method creates a dictionary of a `DeviceIdentifier` object's attributes.

## Class `DeviceKind`

The `DeviceKind` class represents the types of devices in a given system.

```python
class DeviceKind:
    Camera: ClassVar[DeviceKind]
    NONE: ClassVar[DeviceKind]
    Signals: ClassVar[DeviceKind]
    StageAxis: ClassVar[DeviceKind]
    Storage: ClassVar[DeviceKind]

    def __init__(self, *args: None, **kwargs: Any) -> None:
    """Initializes the DeviceKind class."""

    def __eq__(self, other: object) -> bool:
    """Checks if two DeviceKind objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this DeviceKind is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this DeviceKind is greater than another."""

    def __int__(self) -> int:
    """Converts the DeviceKind to an integer."""

    def __le__(self, other: object) -> bool:
    """Checks if this DeviceKind is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this DeviceKind is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two DeviceKind objects are not equal."""
```

- `Camera`: Enum-type class variable of `DeviceKind` that specifies a device is a camera.

- `NONE`: Enum-type class variable of `DeviceKind` for if a device's kind is unavailable.

- `Signals`: Enum-type class variable of `DeviceKind` that specifies a device is a signal.

- `StageAxis`: Enum-type class variable of `DeviceKind` that specifies a device is a stage.

- `Storage`: Enum-type class variable of `DeviceKind` that specifies a device is for storage.

## Class `DeviceManager`

The `DeviceManager` class manages selection of available devices in the system. Regular expressions are accepted for the name argument.

```python
class DeviceManager:
    def devices(self) -> List[DeviceIdentifier]:
    """Returns a list of all available device identifiers."""

    @overload
    def select(self, kind: DeviceKind, name: Optional[str]) -> Optional[DeviceIdentifier]:
    """Selects a specified device.

    Args:
        kind (DeviceKind): The type of device to select.
        name (Optional[str]): The name of the device to select. Regular expressions supported.

    Returns:
        Optional[DeviceIdentifier]: The selected device identifier, or None if the specified device is not available.
    """

    def select_one_of(self, kind: DeviceKind, names: List[str]) -> Optional[DeviceIdentifier]:
    """Selects the first device in the list of devices that is of one of the specified kinds.

    Args:
        kind (DeviceKind): The type of device to select.
        names (List[str]): A list of device names to choose from. Regular expressions supported.

    Returns:
        Optional[DeviceIdentifier]: The selected device identifier, or None if none of the specified devices are available.
    """
```

- Call `devices` to list the `DeviceIdentifier` of each available device.

- Call `select` to choose the first available device of a given type or to select a specific device by name.

- Call `select_one_of` to choose one device from a list of acceptable devices of a given kind.

## Class `DeviceState`

The `DeviceState` class represents the acquisition status of a device.

```python
class DeviceState:
    Closed: ClassVar[DeviceState]
    AwaitingConfiguration: ClassVar[DeviceState]
    Armed: ClassVar[DeviceState]
    Running: ClassVar[DeviceState]

    def __eq__(self, other: object) -> bool:
    """Checks if two DeviceState objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this DeviceState is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this DeviceState is greater than another."""

    def __int__(self) -> int:
    """Converts the DeviceState to an integer."""

    def __le__(self, other: object) -> bool:
    """Checks if this DeviceState is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this DeviceState is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two DeviceState objects are not equal."""
```

- `Closed`: Enum-type class variable of `DeviceState` that species when a device is not ready for configuration.

- `AwaitingConfiguration`: Enum-type class variable of `DeviceState` that species when a device is ready for configuration.

- `Armed`: Enum-type class variable of `DeviceState` that species when a device ready to stream data.

- `Running`: Enum-type class variable of `DeviceState` that species when a device is streaming data.

## Class `DigitalLineCapabilities`

The `DigitalLineCapabilities` class represents the digital lines supported by the device.

```python
class DigitalLineCapabilities:
    line_count: int
    names: Tuple[str, str, str, str, str, str, str, str]

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the DigitalLineCapabilities attributes."""
```

- line_count: Integer number representing the number of digital lines supported.

- names: Tuple of strings to name each of the digital lines, typically the last one is the camera software trigger.

- The `dict` method creates a dictionary of a `DigitalLineCapabilities` object's attributes.

## Class `DimensionType`

The `DimensionType` class is used to specify the physical meaning of a dimension, such as space or time dimension. When downsampling, Space and Time dimensions are downsampled by the same factor. Channel and Other dimensions are not downsampled.

This value is also reflected in the dimension metadata of an OME-Zarr dataset.

```python
class DimensionType:
    Space: ClassVar[DimensionType]
    Channel: ClassVar[DimensionType]
    Time: ClassVar[DimensionType]
    Other: ClassVar[DimensionType]

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    """Initializes a DimensionType object with optional arguments."""

    def __eq__(self, other: object) -> bool:
    """Checks if two DimensionType objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this DimensionType is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this DimensionType is greater than another."""

    def __int__(self) -> int:
    """Converts the DimensionType to an integer."""

    def __le__(self, other: object) -> bool:
    """Checks if this DimensionType is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this DimensionType is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two DimensionType objects are not equal."""
```

- `Space`: Enum-type class variable of `DimensionType` that indicates a spatial dimension.
  
- `Channel`: Enum-type class variable of `DimensionType` that indicates a color channel dimension.
  
- `Time`: Enum-type class variable of `DimensionType` that indicates a time dimension.

- `Other`: Enum-type class variable of `DimensionType` that indicates the dimension is not a space, channel, or time.

## Class `Direction`

The `Direction` class represents the direction that data is read for streaming.

```python
class Direction:
    Backward: ClassVar[Direction]
    Forward: ClassVar[Direction]

    def __eq__(self, other: object) -> bool:
    """Checks if two Direction objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this Direction is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this Direction is greater than another."""

    def __int__(self) -> int:
    """Converts the Direction to an integer."""

    def __le__(self, other: object) -> bool:
    """Checks if this Direction is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this Direction is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two Direction objects are not equal."""
```

- `Backward`: Enum-type class variable of `Direction` that species when data is streamed backward.

- `Forward`: Enum-type class variable of `Direction` that species when data is streamed forward.

## Class `InputTriggers`

The `InputTriggers` class represents input triggers for a camera device.

```python
class InputTriggers:
    acquisition_start: Trigger
    exposure: Trigger
    frame_start: Trigger

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the InputTriggers attributes."""
```

- `acquisition_start`: An instance of the `Trigger` class representing the trigger for starting acquisition.

- `exposure`: An instance of the `Trigger` class representing the trigger for exposure.

- `frame_start`: An instance of the `Trigger` class representing the trigger for starting a frame.

- The `dict` method creates a dictionary of a `InputTriggers` object's attributes.

## Class `OffsetShapeCapabilities`

The `OffsetShapeCapabilities` class represents the size of the offset or the shape of the region of interest on the camera. The sum of the offset and shape is the size of the full camera chip.

```python
class OffsetShapeCapabilities:
    x: Property
    y: Property

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the OffsetShapeCapabilities attributes."""
```

- `x`: An instance of the `Property` class which represents the width of the region of interest on the camera or the horizontal offset of the region of interest on the camera chip.

- `y`: An instance of the `Property` class which represents the height of the region of interest on the camera or the vertical offset of the region of interest on the camera chip.

- The `dict` method creates a dictionary of a `OffsetShapeCapabilities` object's attributes.


## Class `OutputTriggers`

The `OutputTriggers` class represents output triggers for a camera device.

```python
class OutputTriggers:
    exposure: Trigger
    frame_start: Trigger
    trigger_wait: Trigger

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the OutputTriggers attributes."""
```

- `exposure`: An instance of the `Trigger` class representing the trigger for exposure.

- `frame_start`: An instance of the `Trigger` class representing the trigger for starting a frame.

- `trigger_wait`: An instance of the `Trigger` class representing the trigger for waiting before continuing acquisition.

- The `dict` method creates a dictionary of a `OutputTriggers` object's attributes.

## Class `PID`

The `PID` class represents proportional-integral-derivative (PID) values.

```python
class PID:
    derivative: float
    integral: float
    proportional: float

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    """Initializes a PID object with optional arguments."""

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the PID attributes."""
```

- `derivative`: The derivative value for the PID.

- `integral`: The integral value for the PID.

- `proportional`: The proportional value for the PID.

- The `dict` method creates a dictionary of a `PID` object's attributes.

## Class `Properties`

The `Properties` class represents properties related to video streams.

```python
class Properties:
    video: Tuple[VideoStream, VideoStream]

    def __init__(self, *args: None, **kwargs: Any) -> None: ..
    """Initializes a Properties object with optional arguments.""".

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the Properties attributes."""
```

- `video`: A tuple containing two `VideoStream` instances since `Acquire` supports simultaneous streaming from 2 video sources. `VideoStream` objects have 2 attributes `camera` and `storage` to set the source and sink for the stream.

- The `dict` method creates a dictionary of a `Properties` object's attributes.

## Class `Property`

The `Property` class indicates the type of and whether the property can be overwritten. For numerical values, it also captures the accepted range of values.

```python
class Property:
    writable: bool
    low: float
    high: float
    kind: PropertyType

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    """Initializes a Property object with optional arguments."""

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the Property attributes."""
```

- `writable`: A boolean indicating whether the property can be written.

- `low`: Floating point number for the lower bound of the property, if applicable.

- `high`: Floating point number for the upper bound of the property, if applicable.

- `kind`: An instance of the `PropertyType` class which indicates the type of the property (fixed precision, floating-point, enum, or string).

- The `dict` method creates a dictionary of a `Property` object's attributes.

## Class `PropertyType`

The `PropertyType` class indicates the type of the property (fixed precision, floating-point, enum, or string).

```python
class PropertyType:
    FixedPrecision: ClassVar[PropertyType]
    FloatingPrecision: ClassVar[PropertyType]
    Enum: ClassVar[PropertyType]
    String: ClassVar[PropertyType]

    def __eq__(self, other: object) -> bool:
    """Checks if two PropertyType objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this PropertyType is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this PropertyType is greater than another."""

    def __int__(self) -> int:
    """Converts the PropertyType to an integer."""

    def __le__(self, other: object) -> bool:
    """Checks if this PropertyType is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this PropertyType is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two PropertyType objects are not equal."""
```

- `FixedPrecision`: Enum-type class variable of `PropertyType` that indicates fixed precision or integer values.

- `FloatingPrecision`: Enum-type class variable of `PropertyType` that indicates floating point precision values.

- `Enum`: Enum-type class variable of `PropertyType` that indicates enum-type values.

- `String`: Enum-type class variable of `PropertyType` that indicates string values.

## Class `Runtime`

The `Runtime` class coordinates the devices with the storage disc including selecting the devices, setting their properties, and starting and stopping acqusition.

```python
class Runtime:
    def __init__(self, *args: None, **kwargs: Any) -> None:
    """Initializes the Runtime object with optional arguments."""

    def device_manager(self) -> DeviceManager:
    """Returns the DeviceManager instance associated with this Runtime."""

    def get_available_data(self, stream_id: int) -> AvailableDataContext:
    """Returns the AvailableDataContext instance for the given stream ID.

    Args:
        stream_id (int): The ID of the stream for which available data is requested.

    Returns:
        AvailableDataContext: Context manager for available data for the given VideoStream ID.
    """

    def get_configuration(self) -> Properties:
    """Returns the current configuration properties of the runtime."""

    def get_capabilities(self) -> Capabilities: ...
    """Returns the current capabilites of the runtime as an instance of Capabilities."""

    def get_state(self) -> DeviceState:
    """Returns the current state of the device."""

    def set_configuration(self, properties: Properties) -> Properties:
    """Applies the provided configuration properties to the runtime.

    Args:
        properties (Properties): The properties to be set.

    Returns:
        Properties: The updated configuration properties.
    """

    def start(self) -> None:
    """Starts the runtime, allowing it to collect data."""

    def execute_trigger(self, stream_id: int) -> None:
    """Executes a trigger for the given stream ID."""

    def stop(self) -> None:
    """Stops the runtime, ending data collection after the max number of frames is collected."""

    def abort(self) -> None:
    """Aborts the runtime, terminating it immediately."""
```

- Call `device_manager()` to return the `DeviceManager` object associated with this `Runtime` instance.

- Call `get_available_data` with a specific `stream_id`, 0 or 1, to return the context manager, `AvailableDataContext`, associated with the 1st or 2nd video source, respectively.

- Call `get_configuration()` to return the `Properties` object associated with this `Runtime` instance.

- Call `get_capabilities()` to return the `Capabilities` object associated with this `Runtime` instance.

- Call `get_state()` to return the `DeviceState` object associated with this `Runtime` instance.

- Call `set_configuration` with a `Properties` object to change the properties of this `Runtime` instance.

- Call `start()` to begin data acquisition.

- Call `execute_trigger` with a specific `stream_id`, 0 or 1, to execute a trigger for that video source.

- Call `stop()` to end data acquisition once the max number of frames specified in `acquire.VideoStream.max_frame_count` is collected. All objects are deleted to free up disk space upon shutdown of `Runtime`.

- Call `abort()` to immediately end data acqusition. All objects are deleted to free up disk space upon shutdown of `Runtime`.

## Class `SampleRateHz`

The `SampleRateHz` class represents the sampling rate in hertz.

```python
class SampleRateHz:
    numerator: int
    denominator: int

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    """Initializes a SampleRateHz object with optional arguments."""

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the SampleRateHz attributes."""
```

- `numerator`: The numerator part of the sampling rate fraction.

- `denominator`: The denominator part of the sampling rate fraction.

- The `dict` method creates a dictionary of a `SampleRateHz` object's attributes.

## Class `SampleType`

The `SampleType` class defines the type of the values in the streamed data.

```python
class SampleType:
    F32: ClassVar[SampleType]
    I16: ClassVar[SampleType]
    I8: ClassVar[SampleType]
    U16: ClassVar[SampleType]
    U8: ClassVar[SampleType]
    U10: ClassVar[SampleType]
    U12: ClassVar[SampleType]
    U14: ClassVar[SampleType]

    def __eq__(self, other: object) -> bool:
    """Checks if two SampleType objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this SampleType is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this SampleType is greater than another."""

    def __int__(self) -> int:
    """Converts the SampleType to an integer."""

    def __le__(self, other: object) -> bool:
    """Checks if this SampleType is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this SampleType is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two SampleType objects are not equal."""
```

- `F32`: Enum-type class variable of `SampleType` that specifies values of 32-bit floating point type.

- `I16`: Enum-type class variable of `SampleType` that specifies values of 16-bit signed integer type.

- `I8`: Enum-type class variable of `SampleType` that specifies values of 8-bit signed integer type.

- `U16`: Enum-type class variable of `SampleType` that specifies values of 16-bit unsigned integer type.

- `U8`: Enum-type class variable of `SampleType` that specifies values of 8-bit unsigned integer type.

- `U10`: Enum-type class variable of `SampleType` that specifies values of 10-bit unsigned integer type.

- `U12`: Enum-type class variable of `SampleType` that specifies values of 12-bit unsigned integer type.

- `U14`: Enum-type class variable of `SampleType` that specifies values of 14-bit unsigned integer type.

## Class `SignalIOKind`

The `SignalIOKind` class defines the signal type, input or output, for a trigger.

```python
class SignalIOKind:
    Input: ClassVar[SignalIOKind]
    Output: ClassVar[SignalIOKind]

    def __eq__(self, other: object) -> bool:
    """Checks if two SignalIOKind objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this SignalIOKind is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this SignalIOKind is greater than another."""

    def __int__(self) -> int:
    """Converts the SignalIOKind to an integer."""

    def __le__(self, other: object) -> bool:
    """Checks if this SignalIOKind is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this SignalIOKind is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two SignalIOKind objects are not equal."""
```

- `Input`: Enum-type class variable of `SignalIOKind` that specifies signal coming in to the device.

- `Output`: Enum-type class variable of `SignalIOKind` that specifies signal sent out of the device.

## Class `SignalType`

The `SignalType` class specifies whether a signal is analog or digital.

```python
class SignalType:
    Analog: ClassVar[SignalType]
    Digital: ClassVar[SignalType]

    def __eq__(self, other: object) -> bool:
    """Checks if two SignalType objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this SignalType is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this SignalType is greater than another."""

    def __int__(self) -> int:
    """Converts the SignalType to an integer."""

    def __le__(self, other: object) -> bool:
    """Checks if this SignalType is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this SignalType is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two SignalType objects are not equal."""
```

- `Analog`: Enum-type class variable of `SignalType` that specifies a signal is analog.

- `Input`: Enum-type class variable of `SignalType` that specifies signal coming in to the device.

## Class `Storage`

The `Storage` class represents storage devices and their settings.

```python
class Storage:
    identifier: Optional[DeviceIdentifier]
    settings: StorageProperties

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the Storage attributes."""
```

- `identifier`: An optional attribute which contains an instance of the `DeviceIdentifier` class that describes the storage device if that device is natively supported. Otherwise, it is of type `None`.

- `settings`: An instance of the `StorageProperties` class which contains the settings for the data storage.

- The `dict` method creates a dictionary of a `Storage` object's attributes.

## Class `StorageCapabilities`

The `StorageCapabilities` class represents what types of data handling is supported by the storage device.

```python
class StorageCapabilities:
    chunking_is_supported: bool
    sharding_is_supported: bool
    multiscale_is_supported: bool

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the StorageCapabilities attributes."""
```

- `chunking_is_supported`: A boolean indicating whether chunking is supported for this storage device.
  
- `sharding_is_supported`: A boolean indicating whether sharding is supported for this storage device.
  
- `multiscale_is_supported`: A boolean indicating whether multiscale storage is supported.

- The `dict` method creates a dictionary of a `StorageCapabilities` object's attributes.

## Class `StorageDimension`

The `StorageDimension` represents the type and size of the dimension for storage.

```python
class StorageDimension:
    name: str
    kind: DimensionType
    array_size_px: int
    chunk_size_px: int
    shard_size_chunks: int

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the StorageDimension attributes."""
```

- `name`: A string representing the name or label of the storage dimension.

- `kind`: An instance of the `DimensionType` specifying if the storage dimension is space, channel, time, or a different physical dimension.
  
- `array_size_px`: The size of the output array along this dimension, in pixels. The final (i.e., append) dimension must have size 0.

- `chunk_size_px`: The size of a chunk along this dimension, in pixels.

- `shard_size_chunks`: Integer number of chunks per shard. Shards enable aggregating multiple chunks into a single file. This value is ignored if sharding is not supported by the storage device.

- The `dict` method creates a dictionary of a `StorageDimensions` object's attributes.

## Class `StorageProperties`

The `StorageProperties` class represents properties for data storage.

```python
class StorageProperties:
    external_metadata_json: Optional[str]
    filename: Optional[str]
    first_frame_id: int
    pixel_scale_um: Tuple[float, float]
    acquisition_dimensions: List[StorageDimension]
    enable_multiscale: bool

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the StorageProperties attributes."""
```

- `external_metadata_json`: An optional attribute of the metadata JSON filename as a string.

- `filename`: An optional attribute representing the filename for storing the image data.

- `first_frame_id`: An integer representing the ID of the first frame for a given acquisition.

- `pixel_scale_um`: A tuple of two floats representing the pixel size of the camera in micrometers.

- `acquisition_dimensions`: A list of instances of the `StorageDimension` class, one for each acquisition dimension. The fastest changing dimension should be first in the list and the append dimension should be last. This value is only applicable for Zarr storage devices.

- `enable_multiscale`: A boolean indicating whether multiscale storage is enabled.

- The `dict` method creates a dictionary of a `StorageProperties` object's attributes.


## Class `Trigger`

The `Trigger` class represents a trigger signal.

```python
class Trigger:
    edge: TriggerEdge
    enable: bool
    line: int
    kind: SignalIOKind

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    """Initializes a Trigger object with optional arguments."""

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the Trigger attributes."""
```

- `edge`: An instance of the `TriggerEdge` class specifying if the trigger is on the rising or falling edge trigger signal.

- `enable`: A boolean indicating whether the trigger is enabled.

- `line`: An integer representing the max value of the trigger signal.

- `kind`: An instance of the `SignalIOKind` class specifying if the signal is input or output.

- The `dict` method creates a dictionary of a `Trigger` object's attributes.

## Class `TriggerCapabilities`

The `TriggerCapabilities` class specifies what types of events the trigger can initiate.

```python
class TriggerCapabilities:
    acquisition_start: TriggerInputOutputCapabilities
    exposure: TriggerInputOutputCapabilities
    frame_start: TriggerInputOutputCapabilities

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the TriggerCapabilities attributes."""
```
- `acquisition_start`: An instance of the `TriggerInputOutputCapabilities` class indicating which lines, either input or output, are supported for starting acquisition.
  
- `exposure`: An instance of the `TriggerInputOutputCapabilities` class indicating which lines, either input or output, are supported for starting exposure.
  
- `frame_start`: An instance of the `TriggerInputOutputCapabilities` class indicating which lines, either input or output, are supported for starting a frame.

- The `dict` method creates a dictionary of a `TriggerCapabilities` object's attributes.


## Class `TriggerEdge`

The `TriggerEdge` class represents what edge of the trigger function initiates the trigger.

```python
class TriggerEdge:
    Falling: ClassVar[TriggerEdge]
    NotApplicable: ClassVar[TriggerEdge]
    Rising: ClassVar[TriggerEdge]
    AnyEdge: ClassVar[TriggerEdge]
    LevelLow: ClassVar[TriggerEdge]
    LevelHigh: ClassVar[TriggerEdge]

    def __eq__(self, other: object) -> bool:
    """Checks if two TriggerEdge objects are equal."""

    def __ge__(self, other: object) -> bool:
    """Checks if this TriggerEdge is greater than or equal to another."""

    def __gt__(self, other: object) -> bool:
    """Checks if this TriggerEdge is greater than another."""

    def __int__(self) -> int:
    """Converts the TriggerEdge to an integer."""

    def __le__(self, other: object) -> bool:
    """Checks if this TriggerEdge is less than or equal to another."""

    def __lt__(self, other: object) -> bool:
    """Checks if this TriggerEdge is less than another."""

    def __ne__(self, other: object) -> bool:
    """Checks if two TriggerEdge objects are not equal."""
```

- `Falling`: Enum-type class variable of `TriggerEdge` that defines the falling edge of the trigger.

- `NotApplicable`: Enum-type class variable of `TriggerEdge` that defines if a trigger does not have a rising or falling edge.

- `Rising`: Enum-type class variable of `TriggerEdge` that defines the rising edge of the trigger.

- `AnyEdge`: Enum-type class variable of `TriggerEdge` that defines any edge of the trigger.

- `LevelLow`: Enum-type class variable of `TriggerEdge` that defines the low level of the trigger.

- `LevelHigh`: Enum-type class variable of `TriggerEdge` that defines the high level of the trigger.

## Class TriggerInputOutputCapabilities

The `TriggerInputOutputCapabilities` class specifies which of the up to 8 supported digital lines can be used for either input or output triggering. The 2 attributes, input and output, each are read-only values and 8-bit integers from the conversion of the 8 binary digit representation of the digital lines to a decimal integer. For example, if lines 0 and 2 were available for input triggers, the 8 binary digit representation would be 0b00000101, since the 8 available lines are zero indexed. 00000101 binary is 5 in the decimal system, so the input attribute would have a value of 5. 

```python
class TriggerInputOutputCapabilities:
    input: int
    output: int

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the TriggerInputOutputCapabilities attributes."""
```

- `input`: 8-bit integer representing which digital lines can be used for input triggering. For example, if lines 0 and 2 were available for input triggers, the 8 binary digit representation of the lines is 00000101, which is 5 in the decimal system.

- `output`: 8-bit integer representing which digital lines can be used for output triggering. For example, if lines 3 and 5 were available for output triggers, the 8 binary digit representation of the lines is 00101000, which is 40 in the decimal system.

- The `dict` method creates a dictionary of a `TriggerInputOutputCapabilities` object's attributes.

## Class `VideoFrame`

The `VideoFrame` class represents data from acquisition of a frame.

```python
class VideoFrame:
    def data(self) -> NDArray[Any]:
    """Returns the data of the video frame as an NDArray."""

    def metadata(self) -> VideoFrameMetadata:
    """Returns the metadata associated with the video frame."""
```

- Call `data()` to create an NDArray of the `VideoFrame` data.

- Call `metadata()` to create a `VideoFrameMetadata` object containing the metadata of `VideoFrame`.

## Class `VideoFrameMetadata`

The `VideoFrameMetadata` class represents metadata related to a video frame.

```python
class VideoFrameMetadata:
    frame_id: int
    timestamps: VideoFrameTimestamps

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the VideoFrameMetadata attributes."""
```

- `frame_id`: An integer representing the ID of the video frame.

- `timestamps`: An instance of the `VideoFrameTimestamps` class specifying the video timestamps based on the hardware clock and the acquisition clock.

- The `dict` method creates a dictionary of a `VideoFrameTimestamps` object's attributes.

## Class `VideoFrameTimestamps`

The `VideoFrameTimestamps` class represents timestamps related to a video frame.

```python
class VideoFrameTimestamps:
    hardware: int
    acq_thread: int

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the VideoFrameTimestamps attributes."""
```

- `hardware`: An integer representing hardware timestamps.

- `acq_thread`: An integer representing timestamps from the acquisition thread.

- The `dict` method creates a dictionary of a `VideoFrameTimestamps` object's attributes.

## Class `VideoStream`

The `VideoStream` class represents a video stream.

```python
class VideoStream:
    camera: Camera
    storage: Storage
    max_frame_count: int
    frame_average_count: int

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the VideoStream attributes."""
```

- `camera`: An instance of the `Camera` class representing the camera device for the video stream.

- `storage`: An instance of the `Storage` class representing the storage device for the video stream.

- `max_frame_count`: An integer representing the maximum number of frames to acquire.

- `frame_average_count`: An integer representing the number of frames to average, if any, before streaming. The default value is 0, which disables this feature. Setting this to 1 will also prevent averaging.

- The `dict` method creates a dictionary of a `VideoStream` object's attributes.

## Class `VideoStreamCapabilities`

The `VideoStreamCapabilities` class captures the capabilities for a video stream.

```python
class VideoStreamCapabilities:
    camera: CameraCapabilities
    storage: StorageCapabilities
    max_frame_count: Property
    frame_average_count: Property

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the VideoStreamCapabilities attributes."""
```

- `camera`: An instance of the CameraCapabilities class which represents the capabilities for the camera in this video stream.
  
- `storage`: An instance of the StorageCapabilities class which represents the capabilities for the storage device in this video stream.
  
- `max_frame_count`: An instance of the Property class.
  
- `frame_average_count`: An instance of the Property class.

- The `dict` method creates a dictionary of a `VideoStreamCapabilities` object's attributes.

## Class `VoltageRange`

The `VoltageRange` class represents a range of voltage values.

```python
class VoltageRange:
    mn: float
    mx: float

    @overload
    def __init__(self) -> None: ...
    """Initializes a VoltageRange object"""

    @overload
    def __init__(self, mn: float, mx: float) -> None: ...
    """Initializes a VoltageObject object with mn and mx provided."""

    def dict(self) -> Dict[str, float]: ...
    """Returns a dictionary of the VoltageRange attributes."""
```

- `mn`: A float representing the minimum voltage value.

- `mx`: A float representing the maximum voltage value.

- The `dict` method creates a dictionary of a `VoltageRange` object's attributes.
