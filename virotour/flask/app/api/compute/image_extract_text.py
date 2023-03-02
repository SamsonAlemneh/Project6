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

    # NEEDED: call a function that creates and returns a panoramic image (created from all images in the server_file_paths variable.
    #panoramic_img = ...
    
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

    # the argument in the below function should be the computed paranomic image that was created above (harcoded path at the moment)
    extractTextList = compute_extracted_text_list('../../tests/images/input_images/location2/museum.jpg')
    
    return extractTextList

def compute_extracted_text_list(image_url): 

    listOfExtractedTexts = []
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_url)

    # Note: explore confidence percentage level / threshold (0.05)

    for textObj in result:

        # each extracted text object provides a confidence level [0 to 1], determining how accurate the extracted text is
        # needed to filter out extracted text objects from being returned (chosen value: 0.05 or 5% confidence level)
        confidenceLevel = textObj[2]

        if confidenceLevel > 0.05:
            # the [x, y] coordinates of the four corners that encapsulates the extracted text
            bottomLeftCoords = textObj[0][0]                                                        
            bottomRightCoords = textObj[0][1]
            topRightCoords = textObj[0][2]
            topLeftCoords = textObj[0][3]

            # determine average x and y coordinates based on the width and height of encapture box that surrounds extracted text
            averagePositionX = round((topRightCoords[0] + topLeftCoords[0]) / 2)
            averagePositionY = round((topLeftCoords[1] + bottomLeftCoords[1]) / 2)

            currentExtractedTextObj = {
                "position": { "x": averagePositionX, "y": averagePositionY, "z": 0 },
                "content": textObj[1]
            } 
            
            listOfExtractedTexts.append(currentExtractedTextObj)

    return listOfExtractedTexts