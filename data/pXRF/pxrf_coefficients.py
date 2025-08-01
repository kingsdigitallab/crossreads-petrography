# pxrf_coefficients.py

"""
pXRF polynomial coefficients with threshold limits.
Each element has threshold values (T, U, V) that determine which coefficient range to use.
"""

COEFFICIENTS = {
    "M": {
        "Si": {
            "thresholds": {"T": 100, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": -0.01, "c": 1.69, "d": 0.00},
        },
        "Ti": {
            "thresholds": {"T": 6.50, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.06, "c": 0.57, "d": 0.00},
        },
        "Fe": {
            "thresholds": {"T": 75, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 0.53, "d": 0.00},
        },
        "Mn": {
            "thresholds": {"T": 2.00, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 0.52, "d": 0.00},
        },
        "Ca": {
            "thresholds": {"T": 100, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 0.56, "d": 0.00},
        },
        "K": {
            "thresholds": {"T": 31, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 0.61, "d": 0.00},
        },
    },
    "MK": {
        "Si": {
            "thresholds": {"T": 15, "U": 100, "V": 0},
            "T": {"a": 0.00, "b": -0.22, "c": 7.12, "d": 0.00},
            "U": {"a": 0.00, "b": -0.01, "c": 1.25, "d": 38.81},
        },
        "Ti": {
            "thresholds": {"T": 3.20, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.07, "c": 0.18, "d": 0.00},
        },
        "Fe": {
            "thresholds": {"T": 90, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": -0.01, "c": 0.40, "d": 0.00},
        },
        "Mn": {
            "thresholds": {"T": 3.50, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 0.31, "d": 0.00},
        },
        "Ca": {
            "thresholds": {"T": 31, "U": 90, "V": 100},
            "T": {"a": 0.00, "b": 0.01, "c": 0.27, "d": 0.00},
            "U": {"a": 0.00, "b": 0.02, "c": -1.72, "d": 50.17},
            "V": {"a": 0.00, "b": 0.27, "c": -47.18, "d": 2129.00},
        },
        "K": {
            "thresholds": {"T": 55, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 0.37, "d": 0.00},
        },
    },
    "t": {
        "Ti": {
            "thresholds": {"T": 0.02, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 371.72, "d": 0.00},
        },
        "Fe": {
            "thresholds": {"T": 0.07, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 949.05, "c": 280.88, "d": 0.00},
        },
        "Mn": {
            "thresholds": {"T": 0.01, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 241.09, "d": 0.00},
        },
        "Ca": {
            "thresholds": {"T": 0.75, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 140.05, "d": 0.00},
        },
        "K": {
            "thresholds": {"T": 0.10, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 191.70, "d": 0.00},
        },
        "Ba": {
            "thresholds": {"T": 0.003, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 3.00e08, "c": 600647.00, "d": 0.00},
        },
        "Co": {
            "thresholds": {"T": 0.0005, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 7.00e08, "c": 150955.00, "d": 0.00},
        },
        "Cr": {
            "thresholds": {"T": 0.01, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 993958.00, "d": 0.00},
        },
        "Ni": {
            "thresholds": {"T": 0.002, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 1.00e06, "d": 0.00},
        },
        "Pb": {
            "thresholds": {"T": 0.002, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 102829.00, "d": 0.00},
        },
        "Rb": {
            "thresholds": {"T": 0.01, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 119827.00, "d": 0.00},
        },
        "Sr": {
            "thresholds": {"T": 0.01, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 130029.00, "d": 0.00},
        },
        "V": {
            "thresholds": {"T": 0.004, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 1.00e06, "d": 0.00},
        },
        "Y": {
            "thresholds": {"T": 0.01, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 123407.00, "d": 0.00},
        },
        "Zn": {
            "thresholds": {"T": 0.0008, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 518901.00, "d": 0.00},
        },
        "Zr": {
            "thresholds": {"T": 0.70, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 135049.00, "d": 0.00},
        },
        "Au": {
            "thresholds": {"T": 0.002, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 102829.00, "d": 0.00},
        },
        "Hg": {
            "thresholds": {"T": 0.002, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 102829.00, "d": 0.00},
        },
        "As": {
            "thresholds": {"T": 0.0008, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 518901.00, "d": 0.00},
        },
        "Cu": {
            "thresholds": {"T": 0.002, "U": 0, "V": 0},
            "T": {"a": 0.00, "b": 0.00, "c": 1000000.00, "d": 0.00},
        },
    },
}


def get_coefficients(input_type, element, value):
    """
    Get the appropriate coefficients for a given input type, element, and value.

    Args:
        input_type (str): 'M', 'MK', or 't'
        element (str): Element symbol (e.g., 'Si', 'Fe', 'Ca')
        value (float): The input value (percentage or mass fraction)

    Returns:
        dict: Coefficients {'a', 'b', 'c', 'd'} for the polynomial
    """
    # Check if value is already an error string
    if isinstance(value, str):
        raise ValueError(value)  # Re-raise the error string as ValueError

    if input_type not in COEFFICIENTS:
        raise ValueError(f"Invalid input type: {input_type}")

    if element not in COEFFICIENTS[input_type]:
        raise ValueError(f"Element {element} not found for input type {input_type}")

    element_data = COEFFICIENTS[input_type][element]
    thresholds = element_data["thresholds"]

    if value <= thresholds["T"]:
        return element_data["T"]
    elif thresholds["U"] > 0 and value <= thresholds["U"]:
        return element_data["U"]
    elif thresholds["V"] > 0 and value <= thresholds["V"]:
        return element_data["V"]

    raise ValueError(
        f"Value {value} is out of range for element {element} in input type {input_type}. "
        f"Valid range: 0 to {max(thresholds.values())}"
    )


def calculate_corrected_value(input_type, element, value):
    """
    Calculate the corrected value using the polynomial coefficients.

    Args:
        input_type (str): 'M', 'MK', or 't'
        element (str): Element symbol
        value (float): Input value

    Returns:
        float or str: Corrected value or error message
    """
    try:
        coeffs = get_coefficients(input_type, element, value)
        return (
            coeffs["a"] * value**3
            + coeffs["b"] * value**2
            + coeffs["c"] * value
            + coeffs["d"]
        )
    except ValueError as e:
        return str(e)  # Return error message as string for logging
