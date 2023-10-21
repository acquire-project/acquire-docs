# Saving and Loading Properties from a JSON file

This tutorial will provide an example of saving and subsequently loading a `Properties` object from a JSON file.

## Initialize Runtime

To start, we'll import `Acquire` and create a `Runtime` object, which coordinates the streaming process.

```python
import acquire
runtime = acquire.Runtime()
```

## Configure Camera

All camera settings are captured by an instance of the `Properties` class, which will be associated with a given camera acquisition. 

```python
# Instantiate a Properties object for the Runtime
props = runtime.get_configuration()
```
You can update any of the settings in this instance of `Properties`. To save any updated settings, use the `set_configuration` function.  For this tutorial, we'll simply specify a camera, and then save these new settings. Note that more settings must be provided before this `Properties` object could be used for an acquistion.

```python
# set the radial sine simulated camera as the first video stream
props.video[0].camera.identifier = runtime.device_manager().select(acquire.DeviceKind.Camera, "simulated: radial sin")

# save the updated settings
props = runtime.set_configuration(props)
```

## Save Properties to a JSON file
We'll utilize the [json library](https://docs.python.org/3/library/json.html#) to write our properties to a JSON file to save for subsequent acquisition.

```python
import json

# cast the properties to a dictionary
props = props.dict()

# convert the dictionary to json with "human-readable" formatting
props = json.dumps(props, indent=4, sort_keys=True)

# save the properties to file "sample_props.json" in the current directory
with open("sample_props.json", "w") as outfile:
    outfile.write(props)
```

## Example JSON file
The resulting sample_props.json file is below:

```json
{
    "video": [
        {
            "camera": {
                "identifier": {
                    "id": [
                        0,
                        1
                    ],
                    "kind": "Camera",
                    "name": "simulated: radial sin"
                },
                "settings": {
                    "binning": 1,
                    "exposure_time_us": 0.0,
                    "input_triggers": {
                        "acquisition_start": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        },
                        "exposure": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        },
                        "frame_start": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        }
                    },
                    "line_interval_us": 0.0,
                    "offset": [
                        0,
                        0
                    ],
                    "output_triggers": {
                        "exposure": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        },
                        "frame_start": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        },
                        "trigger_wait": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        }
                    },
                    "pixel_type": "U16",
                    "readout_direction": "Forward",
                    "shape": [
                        1,
                        1
                    ]
                }
            },
            "frame_average_count": 0,
            "max_frame_count": 18446744073709551615,
            "storage": {
                "identifier": {
                    "id": [
                        0,
                        0
                    ],
                    "kind": "NONE",
                    "name": ""
                },
                "settings": {
                    "chunking": {
                        "max_bytes_per_chunk": 16777216,
                        "tile": {
                            "height": 0,
                            "planes": 0,
                            "width": 0
                        }
                    },
                    "enable_multiscale": false,
                    "external_metadata_json": "",
                    "filename": "",
                    "first_frame_id": 0,
                    "pixel_scale_um": [
                        0.0,
                        0.0
                    ]
                },
                "write_delay_ms": 0.0
            }
        },
        {
            "camera": {
                "identifier": {
                    "id": [
                        0,
                        0
                    ],
                    "kind": "NONE",
                    "name": ""
                },
                "settings": {
                    "binning": 1,
                    "exposure_time_us": 0.0,
                    "input_triggers": {
                        "acquisition_start": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        },
                        "exposure": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        },
                        "frame_start": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        }
                    },
                    "line_interval_us": 0.0,
                    "offset": [
                        0,
                        0
                    ],
                    "output_triggers": {
                        "exposure": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        },
                        "frame_start": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        },
                        "trigger_wait": {
                            "edge": "Rising",
                            "enable": false,
                            "kind": "Input",
                            "line": 0
                        }
                    },
                    "pixel_type": "U16",
                    "readout_direction": "Forward",
                    "shape": [
                        0,
                        0
                    ]
                }
            },
            "frame_average_count": 0,
            "max_frame_count": 18446744073709551615,
            "storage": {
                "identifier": {
                    "id": [
                        0,
                        0
                    ],
                    "kind": "NONE",
                    "name": ""
                },
                "settings": {
                    "chunking": {
                        "max_bytes_per_chunk": 16777216,
                        "tile": {
                            "height": 0,
                            "planes": 0,
                            "width": 0
                        }
                    },
                    "enable_multiscale": false,
                    "external_metadata_json": "",
                    "filename": "",
                    "first_frame_id": 0,
                    "pixel_scale_um": [
                        0.0,
                        0.0
                    ]
                },
                "write_delay_ms": 0.0
            }
        }
    ]
}
```

## Load Properties from a JSON file
You can load the settings in the JSON file to a `Properties` object and set this configuration for your `Runtime` as shown below:

```python
import acquire
import json

# create a Runtime object
runtime = acquire.Runtime()

# Instantiate a `Properties` object from the settings in sample_props.json
props = acquire.Properties(**json.load(open('sample_props.json')))

# save the properties for this instance of Runtime
props = runtime.set_configuration(props)
```

