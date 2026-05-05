import 'package:flutter/material.dart';
import 'screens/request_screen.dart';

void main() {
  runApp(const AiVideoApp());
}

class AiVideoApp extends StatelessWidget {
  const AiVideoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Video System',
      theme: ThemeData(primarySwatch: Colors.blue, useMaterial3: true),
      home: const RequestScreen(),
    );
  }
}