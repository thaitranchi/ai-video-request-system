// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart'; # Using relative import for robustness

void main() {
  testWidgets('App navigation smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Verify that the navigation bar items are present.
    expect(find.text('Request'), findsWidgets);
    expect(find.text('Videos'), findsWidgets);

    // Verify we start on the Request screen (which likely has a specific button or text)
    expect(find.byIcon(Icons.edit), findsOneWidget);
  });
}
