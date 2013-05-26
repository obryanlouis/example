from PIL import Image
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def create_sizes_profile_pic(original):
    '''
    Takes the uploaded profile_pic image file that the user uploads in /backboard_general/views.UploadProfilePic as the only argument.

    Creates a crop of the original image (maximum possible square crop).
    Creates a resize of the square crop (200px, 200px), stores it as an InMemoryUploadedFile.
    Creates another resize from the square crop (32px, 32px), also stores it as an InMemoryUploadedFile.

    Returns both InMemoryUploadedFile objects as a tuple (square_200_imagefile, thumbnail_imagefile).
    '''
    img = Image.open(original) # open user-uploaded file as a PIL.Image() object
    img.verify() # determines if the file is broken
    original.seek(0) # return the start of the file, after verify advances in the file to read first few bytes
    img = Image.open(original) # reopen (this is needed whenever verify is run.

    max_square_dim = min(img.size) # finds the pixel length of the shortest side of the uploaded image as the dimensions for the cropped square.
    left = 0
    top = 0
    width = max_square_dim
    height = max_square_dim
    box = (left, top, left+width, top+height)
    square_max = img.crop(box) # crops the img using the box coordinates (starting on the top left (0,0) corner of img)

    ## CREATE 200x200 RESIZE
    width = 200
    height = 200
    square_200 = square_max.resize((width, height), Image.ANTIALIAS) # resizes square_max to 200x200, using Image.ANTIALIAS, which ensures the best quality (not the best speed)
    square_io = StringIO.StringIO() # create an empty StringIO object. StringIO is a file-like class, that reads and writes a string buffer (also known as MEMORY FILES). It can be used where a file was expected.
    square_200.save(square_io, format='JPEG') # save square_200 to the StringIO object. Image.save usage is: img.save(outfile, [format, options...]). Typically, you save to a filename, but you can also save to a file object (StringIO object, in this case).
    # create an InMemoryUploadedFile from square_io (a file uploaded into memory, ie. stream-to-memory)
    # InMemoryUploadedFile(self, file, field_name, name, content_type, size, charset)
    square_200_imagefile = InMemoryUploadedFile(square_io, None,
                                                'crop.jpg', 'image/jpeg',
                                                square_io.len, None)
    
    ## CREATE 50x50 THUMBNAIL RESIZE
    width = 50
    height = 50
    thumbnail = square_max.resize((width, height), Image.ANTIALIAS)
    thumbnail_io = StringIO.StringIO()
    thumbnail.save(thumbnail_io, format='JPEG')
    thumbnail_imagefile = InMemoryUploadedFile(thumbnail_io, None,
                                                'resize.jpg', 'image/jpeg',
                                                thumbnail_io.len, None)
    
    return (square_200_imagefile, thumbnail_imagefile)



def create_sizes_img_item(original):
    '''
    Takes the uploaded image file as the only argument.

    If the image is too big (width_max is 700, height_max is 900), creates an appropriately-scaled resize of the original called img_big,
    otherwise, returns the original image as 'img_big'
    Creates a scaled resize of 'img_big' to fit (w=363, h=?), called 'img_363'.

    Returns both InMemoryUploadedFile objects as a tuple (img_big_imagefile, img_363_imagefile).
    '''
    # open user-uploaded file as a PIL.Image() object
    img = Image.open(original)
    img.verify()
    original.seek(0)
    img = Image.open(original)
    
    (width, height) = img.size # unpack size attribute
    too_big = False # assume the image is smaller in size than the proposed max (max = (700,900))
    w_difference = None # assume the width is not bigger than max
    h_difference = None # assume the height is not bigger than the max
    if width > 700: # if the width is too big:
        w_difference = width-700 # w_difference is "how much wider than the max"
        too_big = True
    if height > 900: # if the height is too big:
        h_difference = height-900 # h_difference is "how much taller than the max"
        too_big = True
    if too_big==True: # if too wide, too tall, or both:
        if w_difference > h_difference: # if the width exceeds the max more than the height exceeds the max:
            new_height = (height*700)/width
            w = 700
            h = new_height
        else: # if the height exceeds the max more than the width exceeds the max:
            new_width = (width*900)/height
            w = new_width
            h = 900
        img_big = img.resize((w, h), Image.ANTIALIAS)
        img_big_io = StringIO.StringIO() # create an empty StringIO object. String IO is a file-like class, that reads and writes a string buffer (also known as MEMORY FILES). It can be used where a file was expected.
        img_big.save(img_big_io, format='JPEG') # save img_363 to the StringIO object. Image.save usage is: img.save(outfile, [format, options...]). Typically, you save to a filename, but you can also save to a file object (StringIO object, in this case).
        # create an InMemoryUploadedFile from img_io (a file uploaded into memory, ie. stream-to-memory)
        # InMemoryUploadedFile(self, file, field_name, name, content_type, size, charset)
        img_big_imagefile = InMemoryUploadedFile(img_big_io, None,
                                                'resize.jpg', 'image/jpeg',
                                                img_big_io.len, None)
    else:
        img_big = img
        img_big_io = StringIO.StringIO() # create an empty StringIO object. String IO is a file-like class, that reads and writes a string buffer (also known as MEMORY FILES). It can be used where a file was expected.
        img_big.save(img_big_io, format='JPEG') # save img_363 to the StringIO object. Image.save usage is: img.save(outfile, [format, options...]). Typically, you save to a filename, but you can also save to a file object (StringIO object, in this case).
        # create an InMemoryUploadedFile from img_io (a file uploaded into memory, ie. stream-to-memory)
        # InMemoryUploadedFile(self, file, field_name, name, content_type, size, charset)
        img_big_imagefile = InMemoryUploadedFile(img_big_io, None,
                                                'resize.jpg', 'image/jpeg',
                                                img_big_io.len, None)


    (width, height) = img.size
    new_height = (height*363)/width
    w = 363
    h = new_height
    img_363 = img.resize((w, h), Image.ANTIALIAS)
    img_io = StringIO.StringIO() # create an empty StringIO object. String IO is a file-like class, that reads and writes a string buffer (also known as MEMORY FILES). It can be used where a file was expected.
    img_363.save(img_io, format='JPEG') # save img_363 to the StringIO object. Image.save usage is: img.save(outfile, [format, options...]). Typically, you save to a filename, but you can also save to a file object (StringIO object, in this case).
    # create an InMemoryUploadedFile from img_io (a file uploaded into memory, ie. stream-to-memory)
    # InMemoryUploadedFile(self, file, field_name, name, content_type, size, charset)
    img_363_imagefile = InMemoryUploadedFile(img_io, None,
                                            'resize.jpg', 'image/jpeg',
                                            img_io.len, None)

    (x, y) = img.size
    if x <= y:
        left = 0
        top = (y/2 - x/2)
        right = x
        bottom = (y/2 + x/2)
        box = (left, top, right, bottom)
    else:
        left = (x/2 - y/2)
        top = 0
        right (x/2 + y/2)
        bottom = y
        box = (left, top, right, bottom)
    square_max = img.crop(box)

    width = 186
    height = 186
    square_186 = square_max.resize((width, height), Image.ANTIALIAS)
    square_io = StringIO.StringIO()
    square_186.save(square_io, format='JPEG')
    square_186_imagefile = InMemoryUploadedFile(square_io, None,
                                                'crop.jpg', 'image/jpeg',
                                                square_io.len, None)
        

    return (img_big_imagefile, img_363_imagefile, square_186_imagefile)
