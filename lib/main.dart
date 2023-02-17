import 'package:flutter/material.dart';

void main() => runApp(MaterialApp(
  home: NinjaCard(),
));

class NinjaCard extends StatefulWidget {
  const NinjaCard({Key? key}) : super(key: key);

  @override
  State<NinjaCard> createState() => _NinjaCardState();
}

class _NinjaCardState extends State<NinjaCard> {

  int ninjaLevel = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[900],
      appBar: AppBar(
        title: Text('Flutter ID Card'),
        centerTitle: true,
        backgroundColor: Colors.blue[850],
        elevation: 0.0,

        actions: [
          PopupMenuButton(
            color: Colors.lightBlueAccent,
            icon: Icon(Icons.settings),
            itemBuilder: (context)=>[
              PopupMenuItem(child: Row(
                children: [
                  Icon(Icons.sunny,
                    color: Colors.white70,),
                  SizedBox(width: 15.0),
                  Text('Glow Effect',
                    style: TextStyle(
                        fontSize: 12.0
                    ),),
                ],
              )),

              PopupMenuItem(child: Row(
                children: [

                  Icon(Icons.video_call_rounded,
                    color: Colors.white70,),
                  SizedBox(width: 15.0),
                  Text('VR View',
                    style: TextStyle(
                        fontSize: 12.0
                    ),),
                ],
              )),
            ],
          )
        ],

      ),
      floatingActionButton: Padding(
        padding: const EdgeInsets.only(left: 30.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            FloatingActionButton(
              onPressed: () {
                setState(() {
                  ninjaLevel -=1;
                });
              },
              child: Icon(Icons.remove),
              backgroundColor: Colors.blue[600],
            ),
            Expanded(child: Container()),
            FloatingActionButton(
              onPressed: () {
                setState(() {
                  ninjaLevel +=1;
                });
              },
              child: Icon(Icons.add),
              backgroundColor: Colors.blue[600],
            ),
          ],
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,

      body: Padding(
        padding: EdgeInsets.fromLTRB(30.0, 40.0, 30.0, 0.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Center(
              child: CircleAvatar(
                backgroundImage: AssetImage('assets/pic.jfif'),
                radius: 40.0,
              ),
            ),
            Divider(
              height: 50.0,
              color: Colors.blue[100],
              thickness: 2.0,
            ),
            Text(
              'NAME',
              style: TextStyle(
                color: Colors.white,
                letterSpacing: 2.0,
              ),
            ),
            SizedBox(height: 15.0),
            Text(
              'Chun N',
              style: TextStyle(
                color: Colors.amberAccent[200],
                letterSpacing: 2.0,
                fontSize: 28.8,
                fontWeight: FontWeight.bold
              ),
            ),
            SizedBox(height: 30.0),
            Text(
              'CURRENT lEVEL',
              style: TextStyle(
                color: Colors.white,
                letterSpacing: 2.0,
              ),
            ),
            SizedBox(height: 15.0),
            Text(
              '$ninjaLevel',
              style: TextStyle(
                color: Colors.amberAccent[200],
                letterSpacing: 2.0,
                fontSize: 28.8,
                fontWeight: FontWeight.bold
              ),
            ),
            SizedBox(height: 30.00),
            Row(
              children: <Widget>[
                Icon(
                    Icons.email_sharp,
                    color: Colors.grey,
                ),
                SizedBox(width: 10.0),
                Text(
                    'samccd@ole.org',
                    style: TextStyle(
                      color: Colors.amberAccent,
                      fontSize: 20.0,
                      letterSpacing: 1.0,
                    ),
                )
              ],
            ),
            SizedBox(height: 100.0),
            Row(
              children: <Widget>[
                Expanded(
                  child: Container(
                    color: Colors.amber,
                    padding: EdgeInsets.all(20.0),
                        child: Text('bottom'),
                  ),
                ),
              ],
            ),
          ],
        ),
      )
    );
  }
}

