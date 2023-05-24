import 'package:flutter_test/flutter_test.dart';
// import 'package:http/http.dart' show Response;

import 'package:client/class/releve.dart';
import 'package:client/utils/manipulations_releves.dart';

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
      final List<Releve> listeReleves = await fetchReleves();

      for (Releve releve in listeReleves) {
        print(releve.toMap());
      }
    } catch (err) {
      print(err);
    }
  });
}
