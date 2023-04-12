import 'dart:convert' as convert;

import 'package:client/class/releve.dart';
import 'package:http/http.dart' as http;
import 'package:client/constants/adr_server.dart';

// check func

Future<List<Releve>> getReleves() async {
  final List<Releve> releves = [Releve(1, 1, DateTime(1))];

  try {
    Uri serveurAdr =
        Uri.parse('http://$ADRESSE_SERVEUR:$PORT_SERVEUR$RELEVE_PATH');

    final http.Response response = await http.get(serveurAdr);

    // check response status
    print('réponse');
    print(response.body);
    if (response.statusCode == 200) {
      Map<String, dynamic> jsonResponse = convert.jsonDecode(response.body);
      print(jsonResponse);
    }

    print(response);

    convert.jsonDecode(response.body);
  } catch (err) {
    print(err);
  }

  return releves;
}
