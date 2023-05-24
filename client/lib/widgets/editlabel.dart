import 'package:flutter/material.dart';

class EditLabel extends StatelessWidget {
  final String label;
  final String? value;

  const EditLabel({super.key, required this.label, this.value});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Row(children: []),
    );
  }
}
