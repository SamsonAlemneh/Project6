import os

from flask import request, flash, redirect, jsonify

from app import allowed_file, app, db
from app.models import Tour, Location, Image


@app.route('/api/add/tour/images/<string:tour_name>', methods=['POST', 'GET'])
def api_add_tour_images(tour_name):
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        result = {}

        tour = db.session.query(Tour).filter(Tour.name == tour_name).first()
        location = Location(tour.id)
        db.session.add(location)
        db.session.commit()

        for file in files:
            if file and allowed_file(file.filename):
                filename_raw = file.filename
                filename = os.path.basename(filename_raw)
                target_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                           'tour_id=', str(tour.id),
                                           'location_id=', str(location.location_id))
                target_file = os.path.join(target_path, filename)

                # To return to user
                result[filename] = f'uploads/tour_id={tour.id}/location_id={location.location_id}/{filename}'

                # Make directory & save
                os.makedirs(target_path, exist_ok=True)
                file.save(target_file)

                image = Image(location.location_id, target_path)
                db.session.add(image)
                db.session.commit()

        flash('File(s) successfully uploaded')
        payload = {
            'tour_id': tour.id,
            'server_file_paths': result
        }
        return jsonify(payload), 200


@app.route('/api/tour/images/<string:tour_name>/<int:location_id>', methods=['GET'])
def api_get_tour_images(tour_name, location_id):
    result = {}
    # Get Tour
    tour = db.session.query(Tour).filter(Tour.name == tour_name).first()
    # Get Location(s)
    locations = db.session.query(Location).filter(Location.tour_id == tour.id).all()
    for location in locations:
        # Get Images
        images = db.session.query(Image).filter(Image.location_id == location.location_id).all()
        result = [{
            'file_path': image.file_path
        } for image in images]
        payload = {
            'count': len(result),
            'server_file_paths': result
        }
    return jsonify(payload), 200
