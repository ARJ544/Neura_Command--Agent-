"""
Control system brightness and volume tools for an AI agent.
Provides two tools:
- set_volume: Adjusts or retrieves the system volume.
- set_brightness: Adjusts or retrieves the system brightness.

"""
from langchain_core.tools import tool
from typing import Literal
from pycaw.pycaw import AudioUtilities
import comtypes
import screen_brightness_control as sbc

# Volume Control Tool
@tool
def set_volume(action: Literal["set_to", "increase_by", "decrease_by", "current_vol"], amount: int|None ):
    """ 
    Sets the system volume to the specified percentage level. Also gets the current volume level.
        - 0 = Mute
        - 50 = Half
        - 100 = Full
    
    Args:
        amount (int): The target volume level as a percentage (0-100). Must be an integer between 0 and 100, inclusive.
            - Can be None if action is "current_vol".
        action (str): The action to perform on the volume. It can be one of the following:
            - "set_to": Set the volume to the specified amount.
            - "increase_by": Increase the current volume by the specified amount.
            - "decrease_by": Decrease the current volume by the specified amount.
            - "current_vol": Get the current volume level.
    
    Returns:
        Success message indicating the previous and new volume levels, or an Error message if the input is out of range.
    """
    
    if action == "current_vol":
        try:
            comtypes.CoInitialize()
            devices = AudioUtilities.GetSpeakers()
            volume = devices.EndpointVolume
            current_scalar = volume.GetMasterVolumeLevelScalar()
            current_percent = int(current_scalar * 100)
            return f"The current system volume is {current_percent}%."
        except Exception as e:
            return f"An error occurred while retrieving the current volume: {e}"
        finally:
            try:
                comtypes.CoUninitialize()
            except:
                pass

    if not (0 <= amount <= 100):
        return f"Enter a value between 0-100 inclusive. {amount}% is invalid."

    if action not in ["set_to", "increase_by", "decrease_by"]:
        return f"Invalid action '{action}'. Use 'set_to', 'increase_by', or 'decrease_by'."

    # Start COM session
    try:
        comtypes.CoInitialize()
    except Exception as e:
        return f"COM initialization failed: {e}"

    try:
        
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        
        current_scalar = volume.GetMasterVolumeLevelScalar()
        current_percent = int(current_scalar * 100)

        
        if action == "set_to":
            new_scalar = amount / 100
            volume.SetMasterVolumeLevelScalar(new_scalar, None)
            return f"Previous volume was {current_percent}%. Volume set to {amount}% successfully."

        
        if action == "increase_by":
            new_percent = current_percent + amount
            if new_percent > 100:
                return (
                    f"Volume cannot be increased by {amount}%. "
                    f"Current: {current_percent}%. Max allowed: 100%."
                )
            new_scalar = new_percent / 100
            volume.SetMasterVolumeLevelScalar(new_scalar, None)
            return (
                f"Previous volume was {current_percent}%. "
                f"Volume increased by {amount}%. New volume: {new_percent}%."
            )


        if action == "decrease_by":
            new_percent = current_percent - amount
            if new_percent < 0:
                return (
                    f"Volume cannot be decreased by {amount}%. "
                    f"Current: {current_percent}%. Min allowed: 0%."
                )
            new_scalar = new_percent / 100
            volume.SetMasterVolumeLevelScalar(new_scalar, None)
            return (
                f"Previous volume was {current_percent}%. "
                f"Volume decreased by {amount}%. New volume: {new_percent}%."
            )

    except Exception as e:
        return f"An error occurred while controlling volume: {e}"

    finally:
        try:
            comtypes.CoUninitialize()
        except:
            pass

# Brightness Control Tool
@tool
def set_brightness(action: Literal["set_to", "increase_by", "decrease_by", "current_brt"], level: int):
    """
    Sets the system brightness to the specified percentage level. Also get the current brightness level.
        - 0 = Minimum brightness
        - 50 = Medium brightness
        - 100 = Maximum brightness

    Args:
        action (str): The action to perform on the brightness. It can be one of the following:
            - "set_to": Set the brightness to the specified level.
            - "increase_by": Increase the current brightness by the specified level.
            - "decrease_by": Decrease the current brightness by the specified level.
            - "current_brt": Get the current brightness level.
        level (int): The target brightness level as a percentage Multiple of 10 (0, 10, 20, ..., 100).

    Returns:
        str: Success message indicating the previous and new brightness levels,
             or an Error message if the input is out of range.
    """
    if action not in ["set_to", "increase_by", "decrease_by", "current_brt"]:
        return f"Invalid action '{action}'. Use 'set_to', 'increase_by', 'decrease_by', or 'current_brt'."
    if level not in range(0, 101, 10):
        return f"Enter a value between 0-100 inclusive in multiples of 10. {level}% is invalid."
    
    current_brightness = sbc.get_brightness(display=0)[0]
    
    if action == "current_brt":
        return f"The current system brightness is {current_brightness}%."
    
    elif action == "set_to":
        sbc.set_brightness(level, display=0, no_return=False)
        return f"Previous brightness was {current_brightness}%. Brightness set to {level}% successfully."
    
    elif action == "increase_by":
        sbc.set_brightness(f'+{level}', display=0)
        new_brightness = sbc.get_brightness(display=0)[0]
        return (
            f"Previous brightness was {current_brightness}%. "
            f"Brightness increased by {level}%. New brightness: {new_brightness}%."
        )
        
    elif action == "decrease_by":
        sbc.set_brightness(f'-{level}', display=0)
        new_brightness = sbc.get_brightness(display=0)[0]
        return (
            f"Previous brightness was {current_brightness}%. "
            f"Brightness increased by {level}%. New brightness: {new_brightness}%."
        )
