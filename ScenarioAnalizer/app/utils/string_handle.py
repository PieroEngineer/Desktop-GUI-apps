import textwrap

def wrap_label(label: str, width= 30):
    wrapped_label = '\n'.join(textwrap.wrap(label, width=width, break_long_words=False))
    print(f'🔎  Wrapped label: {wrapped_label}\n')
    return wrapped_label

if __name__ == '__main__':
    # s = '1234567890123456789012345678901234567890'
    s = 'F-100_AD11_PI 25-29 AZANGARO'

    print(wrap_label(s))


# wrapped_name = ""
# for i in range(0, len(name), 19):    # Make line break
#     wrapped_name += name[i:i+19] + "\n"
# wrapped_name = wrapped_name.strip()  # Remove trailing newline if any

