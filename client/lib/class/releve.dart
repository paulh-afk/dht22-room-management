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

  String getMinutesSecondes() {
    return '${horodatage.minute}:${horodatage.second}';
  }

  bool isTemperatureHigh() {
    return temperature > 20;
  }

  bool isTemperatureLow() {
    return temperature < 0;
  }

  bool isHumiditeHigh() {
    return humidite > 70;
  }

  bool isHumiditeLow() {
    return humidite < 40;
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
    return 'Température: $temperature\nHumidité: $humidite\nHorodatage: ${getMinutesSecondes()}';
  }
}
