class Video { // Renamed from VideoRequest
  final String id;
  final String query;
  final String status; // Changed from enum to String
  final String? videoUrl;

  Video({ // Renamed constructor
    required this.id,
    required this.query,
    required this.status,
    this.videoUrl,
  });

  factory Video.fromJson(Map<String, dynamic> json) {
    return Video(
      id: json['id']?.toString() ?? "",
      query: json['query']?.toString() ?? "",
      status: json['status']?.toString() ?? "pending", // Default to "pending"
      videoUrl: json['video_url']?.toString(), // Null-safe access
    );
  }
}