import 'package:flutter/material.dart';
import 'package:settings_ui/settings_ui.dart';

class Parametrage extends StatelessWidget {
  const Parametrage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Paramétrage'),
      ),
      body: SettingsList(
        sections: [
          SettingsSection(
            title: const Text('Base de données'),
            tiles: <SettingsTile>[
              SettingsTile.navigation(
                leading: const Icon(Icons.dns_rounded),
                title: const Text('Adresse IP'),
                value: const Text('X.X.X.X'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.numbers_rounded),
                title: const Text('Numéro du port'),
                value: const Text('XXX'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.person_outline_sharp),
                title: const Text('Utilisateur'),
                value: const Text('John Doe'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.password_rounded),
                title: const Text('Mot de passe'),
                value: const Text('*****'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.format_color_text_rounded),
                title: const Text('Nom base de données'),
                value: const Text('XXXXX'),
              ),
            ],
          ),
          SettingsSection(
            title: const Text("Configuration de l'appareil"),
            tiles: <SettingsTile>[
              SettingsTile.navigation(
                leading: const Icon(Icons.description_rounded),
                title: const Text('Nom du local'),
                value: const Text('XXX'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.wb_sunny_rounded),
                title: const Text('Seuil température maximale'),
                value: const Text('XX.X °C'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.ac_unit_rounded),
                title: const Text('Seuil température minimale'),
                value: const Text('XX.X °C'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.water_drop_rounded),
                title: const Text("Seuil d'humidité relative maximale"),
                value: const Text('XX.X %'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.water_drop_outlined),
                title: const Text("Seuil d'humidité relative minimale"),
                value: const Text('XX.X %'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.loop_rounded),
                title: const Text('Compteur'),
                value: const Text('X'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.av_timer_rounded),
                title: const Text('Intervale en chaque mesure'),
                value: const Text('XX secondes'),
              ),
            ],
          ),
          SettingsSection(
            title: const Text('Configuration email'),
            tiles: <SettingsTile>[
              SettingsTile.navigation(
                leading: const Icon(Icons.contact_mail),
                title: const Text('Adresses email de destination'),
                value: const Text('XX'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.send),
                title: const Text('Adresse email source'),
                value: const Text('XXX@XX.XX'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.password_rounded),
                title: const Text('Mot de passe'),
                value: const Text('*****'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.mail),
                title: const Text('Adresse du serveur SMTP'),
                value: const Text('*****'),
              ),
              SettingsTile.navigation(
                leading: const Icon(Icons.numbers_rounded),
                title: const Text('Port de connexion'),
                value: const Text('XXX'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
