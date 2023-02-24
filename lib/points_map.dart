import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_map/plugin_api.dart';
import 'package:latlong2/latlong.dart'; // Only

class MapFlutter extends StatefulWidget {
  const MapFlutter({super.key});

  @override
  State<MapFlutter> createState() => _MapFlutterState();
}

class _MapFlutterState extends State<MapFlutter> {
  // var markers = <Marker>[];

  var marker = <Marker>[
    Marker(
      point: LatLng(21.2350089, 72.858609),
      builder: (context) {
        return getMarker();
      },
    ),
    Marker(
      point: LatLng(21.2357639, 72.8567261),
      builder: (context) {
        return getMarker();
      },
    ),
    Marker(
      point: LatLng(21.2357639, 72.8567261),
      builder: (context) {
        return getMarker();
      },
    ),
    Marker(
      point: LatLng(21.2350089, 72.858609),
      builder: (context) {
        return getMarker();
      },
    ),
  ];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter Map'),
      ),
      body: FlutterMap(
        // mapController: ,
        mapController: MapController(),

        options: MapOptions(
          zoom: 13,
          center: LatLng(21.235293892731804, 72.85903282651766),
        ),
        children: [
          PolygonLayer(
            polygonCulling: true,
            polygons: [
              Polygon(
                points: [
                  LatLng(21.235293892731804, 72.85903282651766),
                  LatLng(21.235293892731804, 72.85903282651766)
                ],
                color: Colors.blue,
              ),
              Polygon(
                points: [
                  LatLng(21.235293892731804, 72.85903282651766),
                  LatLng(21.235293892731804, 72.85903282651766)
                ],
                color: Colors.blue,
              ),
              Polygon(
                points: [
                  LatLng(21.235293892731804, 72.85903282651766),
                  LatLng(21.235293892731804, 72.85903282651766)
                ],
                color: Colors.blue,
              ),
              Polygon(
                points: [
                  LatLng(21.235293892731804, 72.85903282651766),
                  LatLng(21.235293892731804, 72.85903282651766)
                ],
                color: Colors.blue,
              ),
            ],
          ),
          TileLayer(
            urlTemplate: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            userAgentPackageName: 'dev.fleaflet.flutter_map.example',
          ),
          MarkerLayer(
            markers: marker,
          ),
        ],
      ),
    );
  }
}

getMarker() {
  return ClipRRect(
    borderRadius: BorderRadius.circular(100),
    child: Image.network(
      'https://cdn-icons-png.flaticon.com/512/1946/1946770.png',
      // Icons.pin_drop_outlined,
      height: 30,
      fit: BoxFit.cover, // color: Colors.red,
    ),
  );
}
