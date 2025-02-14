def blinking_light_css(input_value, light_size="12px", animation_duration="1s"):
    """
    Generates CSS code for a blinking light animation with a color based on the input value.

    Args:
        input_value (int): Determines the color of the blinking light (1 for green, 2 for red).
        light_size (str): Size of the blinking light (e.g., "12px").
        animation_duration (str): Duration of the blinking animation (e.g., "1s").

    Returns:
        str: CSS code for the blinking light animation.
    """
    # Set the light color based on the input value
    if input_value == 2:
        light_color = "red"
    elif input_value == 1:
        light_color = "green"
    else:
        light_color = "gray"  # Default color if input is invalid

    css = f"""
    .blinking-light {{
        width: {light_size};
        height: {light_size};
        border-radius: 50%;
        background-color: {light_color};
        animation: blink {animation_duration} infinite;
        margin-right: 10px;
    }}

    @keyframes blink {{
        0%, 50% {{
            opacity: 1;
        }}
        50.01%, 100% {{
            opacity: 0;
        }}
    }}
    """
    return css

# Example usage
if __name__ == "__main__":
    input_value = int(input("Enter 1 for red or 2 for green: "))
    print(blinking_light_css(input_value))