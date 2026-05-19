import 'dart:io';

class ApiConstants {
  static String get _host {
    if (Platform.isAndroid) return 'http://10.0.2.2:8000'; // Android emulator
    if (Platform.isIOS) return 'http://localhost:8000'; // iOS simulator
    return 'http://localhost:8000'; // web/desktop
  }

  // API endpoint base URL
  static String get baseUrl => '$_host/api/v1';

  // Used for prepending the relative paths returned by the server
  static String get serverRoot => _host;
}
