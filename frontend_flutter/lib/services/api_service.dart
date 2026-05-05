import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants.dart';
import '../models/video.dart';

class ApiService {
  Future<List<VideoRequest>> getVideos() async {
    final response = await http.get(Uri.parse('${ApiConstants.baseUrl}/videos/'));
    
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(utf8.decode(response.bodyBytes));
      return jsonResponse.map((data) => VideoRequest.fromJson(data)).toList();
    } else {
      throw Exception('Failed to load videos');
    }
  }

  Future<VideoRequest> createRequest(String query) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/requests/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'query': query}),
    );

    if (response.statusCode == 202) {
      return VideoRequest.fromJson(json.decode(utf8.decode(response.bodyBytes)));
    } else {
      throw Exception('Failed to create request');
    }
  }

  Future<VideoRequest> getVideoById(String id) async {
    final response = await http.get(Uri.parse('${ApiConstants.baseUrl}/videos/$id'));

    if (response.statusCode == 200) {
      return VideoRequest.fromJson(json.decode(utf8.decode(response.bodyBytes)));
    } else {
      throw Exception('Failed to get video details');
    }
  }
}

// Global instance for simplicity in the demo
final apiService = ApiService();