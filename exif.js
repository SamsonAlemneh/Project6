// exif extraction from Piexifjs library: https://auth0.com/blog/read-edit-exif-metadata-in-photos-with-javascript/

const fs = require("fs");
const piexif = require("piexifjs");

// Handy utility functions
const getBase64DataFromJpegFile = (filename) =>
  fs.readFileSync(filename).toString("binary");

const getExifFromJpegFile = (filename) =>
  piexif.load(getBase64DataFromJpegFile(filename));

filename = "1.jpg";

// all metadata from file
console.log("All metadata from file: ");
console.log(getExifFromJpegFile(filename));
console.log("===============================================");

// just the GPS data
console.log("Just the GPS data: ");
console.log(getExifFromJpegFile(filename).GPS);
console.log("===============================================");

var latitude;
var longitude;

// getting the longitude and latitude values only
console.log(
  "Latitude (Degrees/Minutes/Seconds): " + getExifFromJpegFile(filename).GPS[2]
);
console.log(
  "Longitude (Degrees/Minutes/Seconds): " + getExifFromJpegFile(filename).GPS[4]
);
console.log("===============================================");

// latitude and longitude values formatted more neatly
console.log(
  "Latitude formatted: " +
    getExifFromJpegFile(filename).GPS[2][0][0] +
    "; " +
    getExifFromJpegFile(filename).GPS[2][1][0] +
    "; " +
    addTwoDecimalPoints(getExifFromJpegFile(filename).GPS[2][2][0])
);
console.log(
  "Longitude formatted: " +
    getExifFromJpegFile(filename).GPS[4][0][0] +
    "; " +
    getExifFromJpegFile(filename).GPS[4][1][0] +
    "; " +
    addTwoDecimalPoints(getExifFromJpegFile(filename).GPS[4][2][0])
);

// to convert degrees/minutes/seconds into decimal degrees somehow
// https://gisgeography.com/decimal-degrees-dd-minutes-seconds-dms/

function addTwoDecimalPoints(minutesFromMetadata) {
  return minutesFromMetadata / 100;
}
