from app.api.image_upload import api_get_tour_images

import easyocr

def image_extract_text(tour_name, location_id):

    # image_list variable below should return a list of path urls:
    #    {
    #        'count': len(result),
    #        'server_file_paths': {
    #           uploads/tour_id={tour.id}/location_id={location.location_id}/{filename}'
    #        }
    #   }

    # Example:

    # {
    #     'count': 5,
    #     'server_file_paths': {
    #         'S1.jpg': 'uploads/tour_id=1/location_id=1/S1.jpg',
    #         'S2.jpg': 'uploads/tour_id=1/location_id=1/S2.jpg',
    #         'S3.jpg': 'uploads/tour_id=1/location_id=1/S3.jpg',
    #         'S4.jpg': 'uploads/tour_id=1/location_id=1/S4.jpg',
    #         'S5.jpg': 'uploads/tour_id=1/location_id=1/S5.jpg'
    #     }
    # }
        
    image_list = api_get_tour_images(tour_name, location_id)

    # call function that creates returns a panoramic image (created from all images in the server_file_paths variable.

    # return extracted text's [x,y] coordinates and respective text from created panoramic image.
    # the return value should be an array of objects, one example below:

    # {
    #     'position': {
    #         'x': 0,
    #         'y': 0,
    #         'z': 0
    #     },
    #     "content": "Bathrooms"
    # }

    # computing text extract on the to-be panoramic image (placeholder image for now)
    reader = easyocr.Reader(['en'])
    result = reader.readtext('../../tests/images/input_images/location1/museum.jpg')
    # result = reader.readtext('../../tests/images/input_images/location1/S2.jpg')

    listOfExtractedTexts = []

    for text in result:
        # the [x, y] coordinates of the four corners that encapsulates the extracted text
        bottomLeftCoords = text[0][0]
        bottomRightCoords = text[0][1]
        topRightCoords = text[0][2]
        topLeftCoords = text[0][3]

        # determine average x and y coordiantes based on the width and height of encapture box that surrounds extracted text
        averagePositionX = round((topRightCoords[0] + topLeftCoords[0]) / 2)
        averagePositionY = round((topLeftCoords[1] + bottomLeftCoords[1]) / 2)

        currentExtractedTextObj = {
            "position": { "x": averagePositionX, "y": averagePositionY, "z": 0 },
            "content": text[1]
        } 
        
        listOfExtractedTexts.append(currentExtractedTextObj)

    return listOfExtractedTexts
