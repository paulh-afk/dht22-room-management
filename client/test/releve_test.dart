import 'package:flutter_test/flutter_test.dart';
import 'package:client/constants/adr_server.dart';
import 'package:client/class/releve.dart';
// import 'package:client/utils/manipulations_releves.dart';
import 'dart:convert' as convert;
import 'package:http/http.dart' as http;

void main() {
  test('Création objet type Releve', () {
    const double temperature = 30;
    const double humidite = 40;

    Releve releve = Releve(temperature, humidite, DateTime(2023, 4, 7));

    expect(30, releve.temperature);
    expect(40, releve.humidite);
  });

  test('Récupération des releves serveur', () async {
    try {
      Uri adr = Uri.parse('http://$ADRESSE_SERVEUR:$PORT_SERVEUR$RELEVE_PATH');

      final http.Response response = await http.get(adr);

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

      final List<Releve> listeReleves = [];

      for (final releve in releves) {
        if (releve is! Map<String, dynamic>) {
          print('pass');
          // ne pas arreter la serialisation si mauvais enregistrement dans la liste
          // throw Exception();
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

      print(listeReleves);
    } on TypeError catch (err) {
      print(err);
    }
    /* on Exception catch (err) {
      print(err);
    } */
    catch (err) {
      // TODO? err is FormatException
      print(err);
    }
  });
}
