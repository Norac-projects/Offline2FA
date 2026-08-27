def read_image(path: str) -> str:
    import zxingcpp
    from PIL import Image

    with Image.open(path) as img:
        results = zxingcpp.read_barcodes(img.convert("RGB"))

    for result in results:
        if result.text.startswith("otpauth://"):
            return result.text

    if results:
        raise ValueError("Found a code in the image, but it's not an otpauth:// QR")
    raise ValueError("No QR code found in that image")
