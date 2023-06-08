import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class EditLabel extends StatefulWidget {
  final String label;
  final String sendKey;
  final String? value;

  EditLabel({Key? key, required this.label, required this.sendKey, this.value})
      : super(key: key);

  @override
  _EditLabelState createState() => _EditLabelState();
}

class _EditLabelState extends State<EditLabel> {
  late String _inputText;

  void _saveData() async {
    if (_inputText.isEmpty) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Erreur'),
            content:
                const Text('Veuillez entrer une valeur avant d\'enregistrer.'),
            actions: [
              TextButton(
                child: const Text('OK'),
                onPressed: () {
                  Navigator.of(context).pop();
                },
              ),
            ],
          );
        },
      );
      return;
    }

    final String url =
        'https://localhost:4000/updateconfig'; // Remplacez par votre URL

    final Map<String, dynamic> requestData = {
      widget.sendKey: _inputText,
    };

    print(widget.sendKey);

    final String requestBody = json.encode(requestData);

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: requestBody,
      );

      if (response.statusCode == 200) {
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text('Succès'),
              content: const Text('Les données ont été enregistrées.'),
              actions: [
                TextButton(
                  child: const Text('OK'),
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
              ],
            );
          },
        );
      } else {
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text('Erreur'),
              content: const Text(
                  'Une erreur s\'est produite lors de l\'enregistrement des données.'),
              actions: [
                TextButton(
                  child: const Text('OK'),
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
              ],
            );
          },
        );
      }
    } catch (e) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Erreur'),
            content: const Text(
                'Une erreur s\'est produite lors de la communication avec le serveur.'),
            actions: [
              TextButton(
                child: const Text('OK'),
                onPressed: () {
                  Navigator.of(context).pop();
                },
              ),
            ],
          );
        },
      );
    }
  }

  @override
  void initState() {
    super.initState();
    _inputText = widget.value ?? '';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextFormField(
              decoration: InputDecoration(
                border: const UnderlineInputBorder(),
                labelText: widget.label,
              ),
              initialValue: widget.value,
              onChanged: (value) {
                setState(() {
                  _inputText = value;
                });
              },
            ),
            ElevatedButton(
              onPressed: _saveData,
              child: const Text('Enregistrer'),
            ),
          ],
        ),
      ),
    );
  }
}
