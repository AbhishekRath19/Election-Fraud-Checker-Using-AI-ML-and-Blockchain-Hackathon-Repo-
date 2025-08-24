from PIL import Image
import io

def compress_image(image_file, max_size=(800, 800), quality=85):
    """
    Compress image file to reduce storage size.
    
    Args:
        image_file: File object containing the image
        max_size: Maximum size tuple (width, height)
        quality: JPEG quality (1-100)
        
    Returns:
        Compressed image file object
    """
    # Open the image
    image = Image.open(image_file.stream)
    
    # Convert to RGB if necessary (for PNG with transparency)
    if image.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
        image = background
    
    # Resize the image maintaining aspect ratio
    image.thumbnail(max_size, Image.LANCZOS)
    
    # Save to byte array with compression
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
    img_byte_arr.seek(0)
    
    return img_byte_arr

def get_image_info(image_file):
    """
    Get information about an image file.
    
    Args:
        image_file: File object containing the image
        
    Returns:
        Dictionary with image information
    """
    image = Image.open(image_file.stream)
    return {
        'format': image.format,
        'mode': image.mode,
        'size': image.size,
        'width': image.width,
        'height': image.height
    }