import 'dart:convert';

import 'package:client/widgets/editlabel.dart';
import 'package:flutter/material.dart';
import 'package:settings_ui/settings_ui.dart';
import 'package:client/constants/adr_server.dart';
import 'package:http/http.dart' as http;

class Parametrage extends StatefulWidget {
  const Parametrage({Key? key}) : super(key: key);

  @override
  _ParametrageState createState() => _ParametrageState();
}

class _ParametrageState extends State<Parametrage> {
  final String apiUrl =
      'http://$ADRESSE_SERVEUR:$PORT_SERVEUR/$CONFIG_PATH'; // Remplacez par l'URL de votre API

  Map<String, dynamic> configData =
      {}; // Variable pour stocker les données de configuration

  String nomLocal = '';

  Future<void> fetchConfigData() async {
    final response = await http.get(Uri.parse(apiUrl));

    if (response.statusCode == 200) {
      setState(() {
        configData = jsonDecode(response.body);
      });
    } else {
      print('Erreur lors de la récupération des données de configuration.');
    }
  }

  Future<void> getNomLocal(int id) async {
    final response = await http
        .get(Uri.parse('http://$ADRESSE_SERVEUR:$PORT_SERVEUR/localname/$id'));

    if (response.statusCode == 200) {
      if (!(jsonDecode(response.body) as Map).containsKey('local')) {
        setState(() {
          nomLocal = 'Local non identifié';
        });
      } else {
        setState(() {
          nomLocal = (jsonDecode(response.body) as Map)['local'];
        });
      }
    } else {
      setState(() {
        nomLocal = 'Local non identifié';
      });
    }
  }

  @override
  void initState() {
    super.initState();
    fetchConfigData(); // Appeler la méthode pour récup
  }

  @override
  Widget build(BuildContext context) {
    if (mounted &&
        configData.containsKey('settings') &&
        ((configData['settings'] as Map).containsKey('id_local'))) {
      getNomLocal(configData['settings']['id_local']);
    }

    SettingsTile createSettingNav(String label, IconData icon, String categorie,
        String key, dynamic value) {
      if (configData.containsKey(categorie) &&
          configData[categorie].containsKey(key)) {
        value = configData[categorie][key];
      }

      if (value is List) {
        value = value.join(', ');
      }

      return SettingsTile.navigation(
        leading: Icon(icon),
        title: Text(label),
        value: Text(value.toString()),
        onPressed: (context) {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => EditLabel(
                label: label,
                sendKey: '$categorie.$key',
                value: value.toString(),
              ),
            ),
          );
        },
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text("Paramétrage de l'appareil $nomLocal"),
      ),
      body: SettingsList(
        sections: [
          SettingsSection(
            title: const Text('Appareil'),
            tiles: <SettingsTile>[
              createSettingNav("Identifiant de l'appareil",
                  Icons.computer_rounded, 'settings', 'id_local', 'X')
            ],
          ),
          SettingsSection(
            title: const Text('Base de données'),
            tiles: <SettingsTile>[
              createSettingNav('Adresse IP', Icons.dns_rounded, 'database',
                  'host', 'X.X.X.X'),
              createSettingNav('Numéro du port', Icons.numbers_rounded,
                  'database', 'port', 'XXX'),
              createSettingNav('Utilisateur', Icons.person_outline_sharp,
                  'database', 'user', 'John Doe'),
              createSettingNav('Mot de passe', Icons.password_rounded,
                  'database', 'password', '*****'),
              createSettingNav(
                  'Nom base de données',
                  Icons.format_color_text_rounded,
                  'database',
                  'database',
                  'XXXXX'),
            ],
          ),
          SettingsSection(
            title: const Text("Configuration de l'appareil"),
            tiles: <SettingsTile>[
              createSettingNav('Nom du local', Icons.description_rounded,
                  'settings', 'id_local', 'XXX'),
              createSettingNav(
                  'Seuil température maximale',
                  Icons.wb_sunny_rounded,
                  'settings',
                  'seuil_temperature_max',
                  'XX.X °C'),
              createSettingNav(
                  'Seuil température minimale',
                  Icons.ac_unit_rounded,
                  'settings',
                  'seuil_temperature_min',
                  'XX.X °C'),
              createSettingNav(
                  "Seuil d'humidité relative maximale",
                  Icons.water_drop_rounded,
                  'settings',
                  'seuil_humidite_max',
                  'XX.X %'),
              createSettingNav(
                  "Seuil d'humidité relative minimale",
                  Icons.water_drop_outlined,
                  'settings',
                  'seuil_humidite_min',
                  'XX.X %'),
              createSettingNav(
                  'Compteur', Icons.pin_rounded, 'settings', 'compteur', 'X'),
              createSettingNav(
                  'Intervale en chaque mesure',
                  Icons.av_timer_rounded,
                  'settings',
                  'interval_secondes',
                  'XX secondes'),
            ],
          ),
          SettingsSection(
            title: const Text('Configuration email'),
            tiles: <SettingsTile>[
              createSettingNav('Adresses email de destination',
                  Icons.contact_mail, 'email', 'destinations', 'X'),
              createSettingNav('Adresse email source', Icons.send, 'email',
                  'sender', 'XXX@XX.XX'),
              createSettingNav('Mot de passe', Icons.password_rounded, 'email',
                  'password', '*****'),
              createSettingNav('Adresse du serveur SMTP', Icons.mail, 'email',
                  'server_addr', '*****'),
              createSettingNav('Port de connexion', Icons.numbers_rounded,
                  'email', 'server_port', 'XXX'),
            ],
          ),
        ],
      ),
    );
  }
}
