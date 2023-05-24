import 'dart:async';

import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

import 'package:client/widgets/parametrage.dart';

import 'package:client/class/releve.dart';
import 'package:client/utils/manipulations_releves.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Releves capteur',
      home: AffichageData(),
    );
  }
}

class AffichageData extends StatefulWidget {
  const AffichageData({super.key});

  @override
  State<StatefulWidget> createState() => _AffichageDataState();
}

class _AffichageDataState extends State<AffichageData> {
  List<Releve> _listeReleves = [];
  bool _highColor = false;
  bool _showError = false;

  void getReleves() {
    fetchReleves().then((releves) {
      setState(() {
        _listeReleves = releves;
      });
    }).catchError(
      (err) {
        if (!_showError) {
          showDialog(
            context: context,
            builder: (context) {
              return WillPopScope(
                onWillPop: () async {
                  setState(() {
                    _showError = false;
                  });
                  return true;
                },
                child: AlertDialog(
                  title:
                      const Text('Erreur lors de la récupération des données'),
                  content: SingleChildScrollView(
                    child: Text(err.toString()),
                  ),
                  actions: <Widget>[
                    ButtonBar(
                      children: [
                        OutlinedButton(
                          child: const Text(
                            'Changer les paramètres de connexion',
                          ),
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const Parametrage(),
                              ),
                            );
                          },
                        ),
                        FilledButton(
                          child: const Text('Réessayer'),
                          onPressed: () {
                            Navigator.pop(context);
                            setState(() {
                              _showError = false;
                            });
                          },
                        )
                      ],
                    )
                  ],
                ),
              );
            },
          );

          setState(() {
            _showError = true;
          });
        }
      },
    );
  }

  List<FlSpot> createTemperatureSpots() {
    List<FlSpot> spots = [];

    for (int i = 0; i < _listeReleves.length; i++) {
      spots.add(FlSpot(i.toDouble(), _listeReleves[i].temperature));
    }

    return spots;
  }

  List<FlSpot> createHumiditeSpots() {
    List<FlSpot> spots = [];

    for (int i = 0; i < _listeReleves.length; i++) {
      spots.add(FlSpot(i.toDouble(), _listeReleves[i].humidite));
    }

    return spots;
  }

  @override
  void initState() {
    super.initState();
    // getReleves();

    Timer.periodic(
      const Duration(milliseconds: 500),
      (timer) {
        setState(() {
          _highColor = !_highColor;
        });
      },
    );

    Timer.periodic(
      const Duration(seconds: 5),
      (timer) {
        getReleves();
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: (_listeReleves.isEmpty && _highColor)
            ? Colors.red[600]
            : Colors.blueGrey[400],
        title: const Text('Relevés capteur local DHT22'),
        actions: <Widget>[
          IconButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const Parametrage(),
                ),
              );
            },
            icon: const Icon(Icons.settings),
          )
        ],
      ),
      body: ListView(
        children: <Widget>[
          Container(
            padding: const EdgeInsets.fromLTRB(0, 15, 0, 15),
            child: Flex(
              direction: Axis.horizontal,
              children: <Widget>[
                Expanded(
                  child: Column(
                    children: <Widget>[
                      Text(
                        'Température',
                        style: TextStyle(
                          fontSize: MediaQuery.of(context).size.height * 0.05,
                        ),
                      ),
                      Text(
                        _listeReleves.isNotEmpty
                            ? '${_listeReleves.last.temperature}°C'
                            : '-',
                        style: TextStyle(
                          fontSize: MediaQuery.of(context).size.height * 0.08,
                          color: (_listeReleves.isNotEmpty && _highColor) &&
                                  (_listeReleves.last.isTemperatureHigh() ||
                                      _listeReleves.last.isTemperatureLow())
                              ? Colors.red[600]
                              : Colors.black,
                        ),
                      )
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    children: <Widget>[
                      Text(
                        'Humidité',
                        style: TextStyle(
                          fontSize: MediaQuery.of(context).size.height * 0.05,
                        ),
                      ),
                      Text(
                        _listeReleves.isNotEmpty
                            ? '${_listeReleves.last.humidite}%'
                            : '-',
                        style: TextStyle(
                          fontSize: MediaQuery.of(context).size.height * 0.08,
                          color: (_listeReleves.isNotEmpty && _highColor) &&
                                  (_listeReleves.last.isHumiditeHigh() ||
                                      _listeReleves.last.isHumiditeLow())
                              ? Colors.red[600]
                              : Colors.black,
                        ),
                      )
                    ],
                  ),
                )
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.only(top: 20),
            child: AspectRatio(
              aspectRatio: 3,
              child: LineChart(
                LineChartData(
                  titlesData: FlTitlesData(
                    bottomTitles: AxisTitles(),
                    topTitles: AxisTitles(),
                    leftTitles: AxisTitles(),
                  ),
                  lineBarsData: [
                    LineChartBarData(
                      gradient: const LinearGradient(
                        colors: [
                          Color.fromRGBO(211, 47, 47, 1),
                          Color.fromRGBO(239, 154, 154, 1),
                        ],
                      ),
                      isCurved: true,
                      barWidth: 14,
                      spots: createTemperatureSpots(),
                    ),
                    LineChartBarData(
                      gradient: const LinearGradient(
                        colors: [
                          Color.fromRGBO(68, 138, 255, 1),
                          Color.fromRGBO(41, 98, 255, 1),
                        ],
                      ),
                      isCurved: true,
                      color: Colors.lightBlueAccent[400],
                      barWidth: 8,
                      spots: createHumiditeSpots(),
                    )
                  ],
                ),
                swapAnimationDuration: const Duration(microseconds: 150),
                swapAnimationCurve: Curves.linear,
              ),
            ),
            // child: LineChart(
            //   LineChartData(
            //     lineBarsData: [
            //       LineChartBarData(
            //         isCurved: true,
            //         barWidth: 8,
            //         spots: [
            //           FlSpot(1, 1),
            //           FlSpot(3, 1.5),
            //           FlSpot(5, 1.4),
            //           FlSpot(7, 3.4),
            //           FlSpot(10, 2),
            //           FlSpot(12, 2.2),
            //           FlSpot(13, 1.8),
            //         ],
            //       )
            //     ],
            //   ),
            //   swapAnimationDuration: const Duration(microseconds: 150),
            //   swapAnimationCurve: Curves.linear,
            // ),
            // child: ,
          )
        ],
      ),
    );
  }
}

// class MyApp extends StatelessWidget {
//   const MyApp({super.key});

//   // This widget is the root of your application.
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'Flutter Demo',
//       theme: ThemeData(
//         // This is the theme of your application.
//         //
//         // TRY THIS: Try running your application with "flutter run". You'll see
//         // the application has a blue toolbar. Then, without quitting the app,
//         // try changing the seedColor in the colorScheme below to Colors.green
//         // and then invoke "hot reload" (save your changes or press the "hot
//         // reload" button in a Flutter-supported IDE, or press "r" if you used
//         // the command line to start the app).
//         //
//         // Notice that the counter didn't reset back to zero; the application
//         // state is not lost during the reload. To reset the state, use hot
//         // restart instead.
//         //
//         // This works for code too, not just values: Most code changes can be
//         // tested with just a hot reload.
//         colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
//         useMaterial3: true,
//       ),
//       home: const MyHomePage(title: 'Flutter Demo Home Page'),
//     );
//   }
// }

// class MyHomePage extends StatefulWidget {
//   const MyHomePage({super.key, required this.title});

//   // This widget is the home page of your application. It is stateful, meaning
//   // that it has a State object (defined below) that contains fields that affect
//   // how it looks.

//   // This class is the configuration for the state. It holds the values (in this
//   // case the title) provided by the parent (in this case the App widget) and
//   // used by the build method of the State. Fields in a Widget subclass are
//   // always marked "final".

//   final String title;

//   @override
//   State<MyHomePage> createState() => _MyHomePageState();
// }

// class _MyHomePageState extends State<MyHomePage> {
//   int _counter = 0;

//   void _incrementCounter() {
//     setState(() {
//       // This call to setState tells the Flutter framework that something has
//       // changed in this State, which causes it to rerun the build method below
//       // so that the display can reflect the updated values. If we changed
//       // _counter without calling setState(), then the build method would not be
//       // called again, and so nothing would appear to happen.
//       _counter++;
//     });
//   }

//   @override
//   Widget build(BuildContext context) {
//     // This method is rerun every time setState is called, for instance as done
//     // by the _incrementCounter method above.
//     //
//     // The Flutter framework has been optimized to make rerunning build methods
//     // fast, so that you can just rebuild anything that needs updating rather
//     // than having to individually change instances of widgets.
//     return Scaffold(
//       appBar: AppBar(
//         // TRY THIS: Try changing the color here to a specific color (to
//         // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
//         // change color while the other colors stay the same.
//         backgroundColor: Theme.of(context).colorScheme.inversePrimary,
//         // Here we take the value from the MyHomePage object that was created by
//         // the App.build method, and use it to set our appbar title.
//         title: Text(widget.title),
//       ),
//       body: Center(
//         // Center is a layout widget. It takes a single child and positions it
//         // in the middle of the parent.
//         child: Column(
//           // Column is also a layout widget. It takes a list of children and
//           // arranges them vertically. By default, it sizes itself to fit its
//           // children horizontally, and tries to be as tall as its parent.
//           //
//           // Column has various properties to control how it sizes itself and
//           // how it positions its children. Here we use mainAxisAlignment to
//           // center the children vertically; the main axis here is the vertical
//           // axis because Columns are vertical (the cross axis would be
//           // horizontal).
//           //
//           // TRY THIS: Invoke "debug painting" (choose the "Toggle Debug Paint"
//           // action in the IDE, or press "p" in the console), to see the
//           // wireframe for each widget.
//           mainAxisAlignment: MainAxisAlignment.center,
//           children: <Widget>[
//             const Text(
//               'You have pushed the button this many times:',
//             ),
//             Text(
//               '$_counter',
//               style: Theme.of(context).textTheme.headlineMedium,
//             ),
//           ],
//         ),
//       ),
//       floatingActionButton: FloatingActionButton(
//         onPressed: _incrementCounter,
//         tooltip: 'Increment',
//         child: const Icon(Icons.add),
//       ), // This trailing comma makes auto-formatting nicer for build methods.
//     );
//   }
// }
