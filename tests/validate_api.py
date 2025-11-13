# This script is designed to help validate the compatibility of your Evok API version
# with the ha-unipi-neuron Home Assistant custom component.
#
# Instructions:
# 1. Install the required library: pip install evok-ws-client
# 2. Change the IP_ADDRESS variable below to the IP address of your Unipi device.
# 3. Run the script from your terminal: python validate_api.py
#
# The script will attempt to connect to your Unipi device and perform a series
# of tests to check for compatibility with Evok API v2 and v3.

import asyncio
from evok_ws_client import UnipiEvokWsClient

IP_ADDRESS = "127.0.0.1"  # CHANGE THIS TO YOUR UNIPI DEVICE'S IP ADDRESS
NEURON_TYPE = "L203"  # A valid Neuron model, e.g., L203, M203, S203
DEVICE_NAME = "validation-test" # A unique name for this test device

async def main():
    """Run the validation tests."""
    print(f"Connecting to Unipi device at {IP_ADDRESS}...")
    client = UnipiEvokWsClient(IP_ADDRESS, NEURON_TYPE, DEVICE_NAME)

    if not await client.evok_connect():
        print("Failed to connect to the Unipi device.")
        return

    print("Connected successfully.")

    # Test 1: Full state sync
    print("\n--- Test 1: Full State Sync ---")
    try:
        await client.evok_full_state_sync()
        print("Full state sync successful.")
    except Exception as e:
        print(f"Full state sync failed: {e}")

    # Test 2: Register default filter
    print("\n--- Test 2: Register Default Filter ---")
    try:
        await client.evok_register_default_filter_dev()
        print("Registering default filter successful.")
    except Exception as e:
        print(f"Registering default filter failed: {e}")

    # Test 3: Send a command (example: toggle a relay)
    # NOTE: This test will attempt to toggle relay 1_01.
    #       If you do not have a relay at this port, this test may fail.
    print("\n--- Test 3: Send Command (Relay Toggle) ---")
    try:
        print("Attempting to toggle relay 1_01...")
        await client.evok_send("relay", "1_01", "1")
        await asyncio.sleep(1)
        await client.evok_send("relay", "1_01", "0")
        print("Relay toggle command sent successfully.")
        print("This suggests compatibility with both v2 and v3 via the evok-ws-client.")
    except Exception as e:
        print(f"Sending command failed: {e}")
        print("This may indicate an incompatibility or that relay 1_01 is not available.")

    await client.evok_close()
    print("\nValidation complete.")

if __name__ == "__main__":
    asyncio.run(main())
