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

- `identifier`: An optional attribute which contains an instance of the `DeviceIdentifier` class that describes the camera, or video source, if that device is natively supported. Otherwise, it is of type `None`.

- `settings`: An instance of the `CameraProperties` class which contains the settings for the camera.

- The `dict` method creates a dictionary of a `Camera` object's attributes.

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

- `pixel_type`: An instance of the `SampleType` class which specifies the numerical data type, for example u16, a 16-bit unsigned integer type.

- `readout_direction`: An instance of the `Direction` class which specifies whether the data is readout forwards or backwards.

- `offset`: A tuple of two integers representing the (x, y) offset in pixels of the image region of interest on the camera.

- `shape`: A tuple of two integers representing the size in pixels of the image region of interest on the camera.

- `input_triggers`: An instance of the `InputTriggers` class, which describes the trigger signals for starting acquisition, camera exposure, and acquiring a frame.

- `output_triggers`: An instance of the `OutputTriggers` class, which describes the trigger signals for the camera exposure, acquiring a frame, as well as any wait times for sending the trigger signal.

- The `dict` method create a dictionary of a `CameraProperties` object's attributes.

## Class `ChunkingProperties`
The `ChunkingProperties` class represents properties related to data chunking for storage in a Zarr container.

```python
class ChunkingProperties:
    max_bytes_per_chunk: int
    tile: TileShape

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the ChunkingProperties attributes."""
```

- `max_bytes_per_chunk`: The maximum number of bytes per data chunk.

- `tile`: An instance of the `TileShape` class representing the shape of the data chunk tile.

- The `dict` method creates a dictionary of a `ChunkingProperties` object's attributes.

## Class `DeviceIdentifier`
The `DeviceIdentifier` class represents an identifier for a device, such as a camera or video source.

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
    """Returns a "None" type DeviceIdentifier. Useful when a DeviceIdentifier is not needed."""

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

- `id`: A tuple (driver_id, device_id) containing two U8 integers that serve to identify each driver and device uniquely for a given run.

- `kind`: An instance of the `DeviceKind` class that represents the type or kind of the device.

- `name`: A string representing the name or label of the device.

- The `dict` method creates a dictionary of a `DeviceIdentifier` object's attributes.

## Class `DeviceKind`

The `DeviceKind` class represents properties for supported devices, such as a camera or video source, in a given system.

```python
class DeviceKind:
    Camera: ClassVar[DeviceKind] = DeviceKind.Camera
    NONE: ClassVar[DeviceKind] = DeviceKind.NONE
    Signals: ClassVar[DeviceKind] = DeviceKind.Signals
    StageAxis: ClassVar[DeviceKind] = DeviceKind.StageAxis
    Storage: ClassVar[DeviceKind] = DeviceKind.Storage

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

- `Camera`: Enum-type class variable of `DeviceKind` that defines the cameras supported by the system. 

- `NONE`: Enum-type class variable of `DeviceKind` that is set to None if no device of the specified kind is available.

- `Signals`: Enum-type class variable of `DeviceKind` that defines the signals supported by the system.

- `StageAxis`: Enum-type class variable of `DeviceKind` that defines the stage axes supported by the system.

- `Storage`: Enum-type class variable of `DeviceKind` that defines the storage supported by the system.

## Class `DeviceManager` 

The `DeviceManager` class manages selection of available devices in the system.

```python
class DeviceManager:
    def devices(self) -> List[DeviceIdentifier]:
        """Returns a list of all available device identifiers."""
    
    @overload
    def select(self, kind: DeviceKind) -> Optional[DeviceIdentifier]:
        """Selects the first available device of `kind`.
        
        Args:
            kind (DeviceKind): The type of device to select.
            
        Returns:
            Optional[DeviceIdentifier]: The identifier of the first available device of `kind`, or `None` if no such device is available.
        """
    
    @overload
    def select(self, kind: DeviceKind, name: Optional[str]) -> Optional[DeviceIdentifier]:
        """Selects a specified device.
        
        Args:
            kind (DeviceKind): The type of device to select.
            name (Optional[str]): The name of the device to select.
            
        Returns:
            Optional[DeviceIdentifier]: The selected device identifier, or None if the specified device is not available.
        """
    
    def select_one_of(self, kind: DeviceKind, names: List[str]) -> Optional[DeviceIdentifier]:
        """Selects the first device in the list of devices that is of one of the specified kinds.
        
        Args:
            kind (DeviceKind): The type of device to select.
            names (List[str]): A list of device names to choose from.
            
        Returns:
            Optional[DeviceIdentifier]: The selected device identifier, or None if none of the specified devices are available.
        """
```

- Call `devices` to list all available devices. 

- Call `select` to choose a type of device for acquisition.

- Call `select_one_of` to choose a particular instance in a category of devices for acquisition.

## Class `DeviceState`

The `DeviceState` class represents the acquisition status of a device.

```python
class DeviceState:
    Closed: ClassVar[DeviceState] = DeviceState.Closed
    AwaitingConfiguration: ClassVar[DeviceState] = DeviceState.AwaitingConfiguration
    Armed: ClassVar[DeviceState] = DeviceState.Armed
    Running: ClassVar[DeviceState] = DeviceState.Running

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

## Class `Direction`

The `Direction` class represents the direction that data is read for streaming.

```python
class Direction:
    Backward: ClassVar[Direction] = Direction.Backward
    Forward: ClassVar[Direction] = Direction.Forward

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

The `InputTriggers` class represents input triggers for a device.

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

## Class `OutputTriggers`

The `OutputTriggers` class represents output triggers for a device.

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

- `video`: A tuple containing two `VideoStream` instances which contain information on the camera was used for acquisition and how the data is stored.

- The `dict` method creates a dictionary of a `Properties` object's attributes.

## Class `Runtime` 

The `Runtime` class coordinates the devices with the storage disc including selecting the devices, setting their properties, and starting and stopping acqusition.

```python
class Runtime:
    def __init__(self, *args: None, **kwargs: Any) -> None:
        """Initializes the Runtime object with optional arguments."""
    
    def device_manager(self) -> DeviceManager:
        """Returns the DeviceManager instance associated with this Runtime."""
    
    def get_available_data(self, stream_id: int) -> AvailableData:
        """Returns the AvailableData instance for the given stream ID.
        
        Args:
            stream_id (int): The ID of the stream for which available data is requested.
            
        Returns:
            AvailableData: The AvailableData instance for the given stream ID.
        """
    
    def get_configuration(self) -> Properties:
        """Returns the current configuration properties of the runtime."""
    
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
    
    def stop(self) -> None:
        """Stops the runtime, ending data collection after the max number of frames is collected."""
    
    def abort(self) -> None:
        """Aborts the runtime, terminating it immediately."""
```

- Call `device_manager()` to return the `DeviceManager` object associated with this `Runtime` instance. 

- Call `get_available_data` with a specific `stream_id` to return the `AvailableData` associated with the `stream_id`.

- Call `get_configuration()` to return the `Properties` object associated with this `Runtime` instance.

- Call `get_state()` to return the `DeviceState` object associated with this `Runtime` instance.

- Call `set_configuration` with a `Properties` object to change the properties of this `Runtime` instance.

- Call `start()` to begin data acquisition.

- Call `stop()` to end data acquisition once the max number of frames specified in `config.video[0].max_frame_count` is collected.

- Call `abort()` to  `Runtime` instance.

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
    F32: ClassVar[SampleType] = SampleType.F32
    I16: ClassVar[SampleType] = SampleType.I16
    I8: ClassVar[SampleType] = SampleType.I8
    U16: ClassVar[SampleType] = SampleType.U16
    U8: ClassVar[SampleType] = SampleType.U8
    U10: ClassVar[SampleType] = SampleType.U10
    U12: ClassVar[SampleType] = SampleType.U12
    U14: ClassVar[SampleType] = SampleType.U14

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

The `SignalIOKind` class defines the type of input and output signals.

```python
class SignalIOKind:
    Input: ClassVar[SignalIOKind] = SignalIOKind.Input
    Output: ClassVar[SignalIOKind] = SignalIOKind.Output

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
    Analog: ClassVar[SignalType] = SignalType.Analog
    Digital: ClassVar[SignalType] = SignalType.Digital

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

The `Storage` class represents storage settings for the acquired data.

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

## Class `StorageProperties`

The `StorageProperties` class represents properties for data storage.

```python
class StorageProperties:
    external_metadata_json: Optional[str]
    filename: Optional[str]
    first_frame_id: int
    pixel_scale_um: Tuple[float, float]
    chunking: ChunkingProperties
    enable_multiscale: bool

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the StorageProperties attributes."""
```

- `external_metadata_json`: An optional attribute representing external metadata in JSON format.

- `filename`: An optional attribute representing the filename.

- `first_frame_id`: An integer representing the ID of the first frame.

- `pixel_scale_um`: A tuple of two floats representing pixel size in micrometers.

- `chunking`: An instance of the `ChunkingProperties` class representing data chunking settings.

- `enable_multiscale`: A boolean indicating whether multiscale storage is desired.

- The `dict` method creates a dictionary of a `StorageProperties` object's attributes.

## Class `TileShape`

The `TileShape` class represents the tile shape, or voxel size, for tile scanning acquisition.

```python
class TileShape:
    width: int
    height: int
    planes: int

    def dict(self) -> Dict[str, Any]: ...
    """Returns a dictionary of the TileShape attributes."""
```

- `width`: The width of the tile.

- `height`: The height of the tile.

- `planes`: The number of planes in the tile.

- The `dict` method creates a dictionary of a `TileShape` object's attributes.

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

- `line`: An integer representing the line of the trigger signal.

- `kind`: An instance of the `SignalIOKind` class specifying if the signal is input or output.

- The `dict` method creates a dictionary of a `Trigger` object's attributes.

## Class `TriggerEdge`

The `TriggerEdge` class represents what edge of the trigger function initiates the trigger.

```python
class TriggerEdge:
    Falling: ClassVar[TriggerEdge] = TriggerEdge.Falling
    NotApplicable: ClassVar[TriggerEdge] = TriggerEdge.NotApplicable
    Rising: ClassVar[TriggerEdge] = TriggerEdge.Rising

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

- Call `metadata()` to query the metadata of `VideoFrame`. 

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

- `timestamps`: An instance of the `VideoFrameTimestamps` class specifying whether the video timestamps are based on the hardware clock or the acquisition clock.

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

- `camera`: An instance of the `Camera` class representing the camera used in the video stream.

- `storage`: An instance of the `Storage` class representing the storage settings for the video stream.

- `max_frame_count`: An integer representing the maximum number of frames in the video stream.

- `frame_average_count`: An integer representing the number of frames to average in the video stream.

- The `dict` method creates a dictionary of a `VideoStream` object's attributes.

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
