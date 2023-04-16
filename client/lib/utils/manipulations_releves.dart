import 'dart:convert' as convert;

import 'package:client/class/releve.dart';
import 'package:http/http.dart' as http;
import 'package:client/constants/adr_server.dart';

Future<List<Releve>> fetchReleves() async {
  final List<Releve> listeReleves = [];

  Uri adr = Uri.parse('http://$ADRESSE_SERVEUR:$PORT_SERVEUR/$RELEVE_PATH');

  final http.Response response = await http.get(adr).catchError(
      (err) => throw Exception('Echec de la connexion avec le serveur!'));

  // response Exceptions
  if (response.statusCode != 200) {
    throw Exception("La requête n'a pas aboutit!");
  }

  final Map<String, dynamic> decodedResponse =
      convert.jsonDecode(response.body);
  final String? responseStatus = decodedResponse['status'];

  if (responseStatus == null) {
    throw Exception('La réponse ne contient pas de status!');
  }

  if (responseStatus != 'OK') {
    // (==) responseStatus == 'KO'
    final String? responseErrMessage = decodedResponse['message'];

    if (responseErrMessage == null) {
      throw Exception('Le réponse contient un erreur!');
    }
    throw Exception(decodedResponse['message']);
  }

  // filtre resultat releves obtenu
  final dynamic releves = decodedResponse['releves'];

  if (releves == null || releves.isEmpty) {
    throw Exception('La réponse ne contient pas de relevés!');
  }

  if (releves is! List) {
    throw Exception("Le format des releves n'est pas valide!");
  }

  for (final releve in releves) {
    if (releve is! Map<String, dynamic>) {
      // ne pas arreter la serialisation si mauvais enregistrement dans la liste
      // throw Exception(); OR
      continue;
    }

    final double? temperature = double.tryParse(releve['temperature']);
    final double? humidite = double.tryParse(releve['humidite']);
    final DateTime? horodatage = DateTime.tryParse(releve['horodatage']);

    if (temperature == null || humidite == null || horodatage == null) {
      throw Exception('Les données recus ne sont pas valide!');
    }

    listeReleves.add(Releve(temperature, humidite, horodatage));
  }

  // } on TypeError catch (err) {
  //   print(err);
  // }
  // // on Exception catch (err) {
  // //     print(err);
  // //   }
  // catch (err) {
  //   // TODO? err is FormatException
  //   print(err);
  // }

  return listeReleves;
}
