# Agent Instructions for ha-unipi-neuron Repository

This document provides instructions for agents working on the `ha-unipi-neuron` repository.

## Supported Devices

This Home Assistant custom component is designed to work with the following Unipi devices:

-   **Neuron Series:** All models in the Neuron series are supported.
-   **Unipi 1.1:** The Unipi 1.1 is also supported.

The integration should be compatible with any Unipi device that can run the Evok API.

## Evok API

The integration uses the `evok-ws-client` library to communicate with the Unipi devices. This library is responsible for handling the differences between Evok API v2 and v3.

Refer to the official [Evok API documentation](https://evok.readthedocs.io/en/stable/) for more details.

## Development Best Practices

-   **Code Style:** Follow the Home Assistant coding standards.
-   **Testing:** Since there is no automated test suite, manual testing is crucial. Use the `tests/validate_api.py` script to help verify API compatibility. Test all changes on both Neuron and Unipi 1.1 devices, if possible.
-   **Dependencies:** Any new dependencies must be added to the `manifest.json` file.
-   **Documentation:** Keep the `README.md` file up-to-date with any changes to the configuration or functionality.
-   **Commit Messages:** Write clear and concise commit messages that explain the changes made.
-   **Pull Requests:** When submitting a pull request, provide a detailed description of the changes and the reasons for them.
