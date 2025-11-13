# ha-unipi-neuron

A Home Assistant custom component for [Unipi](https://www.unipi.technology) devices. This integration allows you to control and monitor your Unipi devices within Home Assistant.

## Introduction

This custom component connects to Unipi devices via the [Evok API](https://github.com/UniPiTechnology/evok), using a WebSocket connection for real-time communication. This ensures a fast and responsive user experience. The integration is designed to work with various Unipi products, including the Neuron, Axon, Patron, and Lite series, as long as they can run the Evok API.

## Supported Devices

This integration is designed to work with any Unipi device that can run the Evok API. The following devices have been confirmed to work:

-   **Neuron Series:** All models in the Neuron series.
-   **Unipi 1.1:** The original Unipi 1.1.

Because the integration uses the Evok API, it should also be compatible with other Unipi devices, such as the Axon, Patron, and Lite series, as long as they have the Evok API installed and running.

## Installation

1.  **Install Evok:** Make sure that the Evok API is installed and running on your Unipi device.
2.  **Configure I/Os:** Configure the I/Os on your Unipi device as needed.
3.  **Copy Component:** Copy the `custom_components` folder to your Home Assistant `/config` folder.
4.  **Configure in YAML:** Add the necessary configuration to your `configuration.yaml` file.

## Configuration

### Main Configuration

Here is an example of a basic configuration for three Unipi Neuron devices in your `configuration.yaml` file:

```yaml
# configuration.yaml
# Main configuration for the UniPi Neuron integration
unipi_neuron:
  # A list of your UniPi devices
  - name: "device1"  # A unique name for this device
    type: L203  # The model of your Neuron device (e.g., L203, M203, S203)
    ip_address: 192.168.11.23  # The IP address of the device
    reconnect_time: 30  # Time in seconds to wait before reconnecting if the connection is lost
  - name: "device2"
    type: M203
    ip_address: 192.168.11.21
    reconnect_time: 30
  - name: "device3"
    type: L203
    ip_address: 192.168.11.24
    reconnect_time: 30
```

The `type` parameter is not used for any specific purpose but should be set to a valid Neuron model, such as "L203", "M203", or "S203".

### Light Component

The light component supports two modes:

-   `on_off`: For simple on/off control of relays.
-   `pwm`: For dimming using Pulse-Width Modulation (only available on digital output pins).

```yaml
# configuration.yaml
light:
  - platform: unipi_neuron
    # Link to the device defined in the main unipi_neuron configuration
    device_id: "device1"
    # A list of light entities for this device
    devices:
      - name: "Light bathroom"  # The name of the light entity in Home Assistant
        device: relay  # The type of hardware device (e.g., relay)
        mode: "on_off"  # "on_off" for simple switching
        port: "1_01"  # The port name from the Evok API
      - name: "Light bedroom"
        device: relay
        mode: "on_off"
        port: "3_06"
  - platform: unipi_neuron
    device_id: "device2"
    devices:
      - name: "Light kitchen"
        device: relay
        mode: "on_off"
        port: "1_01"
      - name: "Light staircase"
        device: relay
        mode: "pwm"  # "pwm" for dimming control
        port: "1_02"
```

### Binary Sensor Component

The binary sensor component is used to monitor digital inputs.

```yaml
# configuration.yaml
binary_sensor:
  - platform: unipi_neuron
    # Link to the device defined in the main unipi_neuron configuration
    device_id: "device3"
    # A list of binary sensor entities for this device
    devices:
      - name: switch_up_utility  # The name of the binary sensor entity
        device: input  # The type of hardware device (e.g., input)
        port: "2_01"  # The port name from the Evok API
      - name: switch_down_utility
        device: input
        port: "2_08"
      - name: switch_light_toilet
        device: input
        port: "2_02"
```

### Cover Component

Used to manage dummy cover/blinds that only support driving motor up and down ( without any ability or sensor to detect location of the blinds or tilt)

**Warning:** Use this component with caution. Driving both the "up" and "down" signals at the same time can damage the motor or the Unipi device. While there are safeguards in the code, they may not cover all edge cases. Use this software at your own risk! I do not take responsibility in any way.

-   `port_up` and `port_down` are output ports used to drive blinds up and down.
-   `full_close_time` and `full_open_time` define the time it takes for blind to fully open (from closed state) or fully close (from open state) in seconds.
-   `tilt_change_time` defines time (in seconds) that the tilt changes from fully open to fully closed state (and vice-versa).
-   `min_reverse_dir_time` minimum time between changing the direction of the motor (in seconds) - defined by blind motor supplier.

```yaml
# configuration.yaml
cover:
  - platform: unipi_neuron
    # Link to the device defined in the main unipi_neuron configuration
    device_id: "main_level_1"
    # A list of cover entities for this device
    covers:
      cover_utility:
        device: relay  # The type of hardware device (e.g., relay)
        port_up: "2_01"  # The output port to drive the blinds up
        port_down: "2_08"  # The output port to drive the blinds down
        full_close_time: 40  # Time in seconds for the blind to fully close
        full_open_time: 40  # Time in seconds for the blind to fully open
        tilt_change_time: 1.5  # Time in seconds for the tilt to change from fully open to fully closed
        min_reverse_dir_time: 1  # Minimum time in seconds between changing motor direction
        name: "Cover_utility"  # The name of the cover entity
        device_class: "blind"  # The device class for the cover (e.g., blind, shutter)
        friendly_name: "Cover Utility"  # The friendly name displayed in the Home Assistant UI
      cover_bedroom:
        device: relay
        port_up: "2_06"
        port_down: "2_07"
        full_close_time: 40
        full_open_time: 40
        tilt_change_time: 1.5
        min_reverse_dir_time: 1
        name: "Cover_bedroom"
        device_class: "blind"
        friendly_name: "Cover Bedroom"
```

## Evok API Compatibility

This integration is designed to be compatible with both Evok API v2 and v3. The `evok-ws-client` library, which this integration uses to communicate with Unipi devices, handles the differences between the two API versions.

### Validating Compatibility

If you are unsure about your Evok API version or want to confirm compatibility, you can use the provided validation script:

1.  **Navigate to the `tests` directory:**
    ```bash
    cd <path_to_your_config>/custom_components/unipi_neuron/tests
    ```
2.  **Install the required library:**
    ```bash
    pip install evok-ws-client
    ```
3.  **Edit the `validate_api.py` script:** Change the `IP_ADDRESS` variable to the IP address of your Unipi device.
4.  **Run the script:**
    ```bash
    python validate_api.py
    ```

The script will run a series of tests and report on the compatibility of your device.

## FAQ

**Q: Can I use this integration with other Unipi devices?**

A: Yes, as long as the device can run the Evok API, it should work with this integration.

**Q: Where can I find the port names for my device?**

A: The port names are defined in the Evok API. You can find them in the Evok web interface or the API documentation.

**Q: What is the `directSwitch` functionality?**

A: `directSwitch` is a feature of Neuron devices that allows for direct control of outputs from inputs, without involving Home Assistant. While this integration provides a fast response time, `directSwitch` may be useful for critical applications.

**Q: My device is not connecting. What should I do?**

A: First, check the Home Assistant logs for any error messages. Then, verify that the IP address in your `configuration.yaml` is correct and that your Unipi device is connected to the network. You can also try restarting the Evok service on your Unipi device.

**Q: Can I use this integration with Home Assistant Cloud?**

A: This integration should work with Home Assistant Cloud, as long as your Home Assistant instance can reach the Unipi device on your local network.

## Feedback and Contributions

Your feedback, pull requests, and other contributions are welcome.

## License

This project is licensed under the MIT License.
