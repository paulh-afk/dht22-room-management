import 'package:client/constants/app_constants.dart';

/// Manipulation des relevés acquis par le capteur DHT22
class Releve {
  final double temperature;
  final double humidite;
  final DateTime horodatage;

  Releve(this.temperature, this.humidite, this.horodatage);
  // TODO => fromMap method
  // Releve.fromMap(Map<String, String> mapData) {
  //   this.temperature = temperature;
  //   this.humidite = humidite;
  //   this.horodatage = horodatage;
  // }

  bool isTemperatureHigh() {
    return temperature > DEFAULT_TEMPERATURE_ELEVEE;
  }

  bool isTemperatureLow() {
    return temperature < DEFAULT_TEMPERATURE_BASSE;
  }

  bool isHumiditeHigh() {
    return humidite > DEFAULT_HUMIDITE_ELEVEE;
  }

  bool isHumiditeLow() {
    return humidite < DEFAULT_HUMIDITE_BASSE;
  }

  // convertions
  Map<String, dynamic> toMap() {
    return {
      'temperature': temperature,
      'humidite': humidite,
      'horodatage': horodatage
    };
  }

  @override
  String toString() {
    return 'Température: $temperature\nHumidité: $humidite\nHorodatage: $horodatage)}';
  }
}
