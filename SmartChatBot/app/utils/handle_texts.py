def bold_text(input_string):
    """
    Detects double asterisks that enclose a text and replaces them
    with <b> and </b> tags.

    Args:
        input_string (str): The string to be processed.

    Returns:
        str: The modified string with bolded text.
    """
    new_string = ""
    start = 0

    while True:
        # Find the first occurrence of '**'
        open_tag_index = input_string.find('**', start)
        if open_tag_index == -1:
            # If no more '**' are found, append the rest of the string
            new_string += input_string[start:]
            break

        # Find the closing '**'
        close_tag_index = input_string.find('**', open_tag_index + 2)
        if close_tag_index == -1:
            # If a closing '**' is not found, treat the rest of the string as plain text
            new_string += input_string[start:]
            break

        # Append the text before the bolded part
        new_string += input_string[start:open_tag_index]

        # Append the bold tag and the text within the asterisks
        bolded_text = input_string[open_tag_index + 2:close_tag_index]
        new_string += f"<b>{bolded_text}</b>"

        # Update the starting position for the next search
        start = close_tag_index + 2
    
    return new_string
