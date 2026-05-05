enum VideoStatus { pending, processing, completed, failed }

class VideoRequest {
  final String id;
  final String query;
  final VideoStatus status;
  final String? videoUrl;

  VideoRequest({
    required this.id,
    required this.query,
    required this.status,
    this.videoUrl,
  });

  factory VideoRequest.fromJson(Map<String, dynamic> json) {
    return VideoRequest(
      id: json['id'],
      query: json['query'],
      status: VideoStatus.values.firstWhere(
        (e) => e.toString().split('.').last == json['status'],
        orElse: () => VideoStatus.pending,
      ),
      // Ensure we get the full URL if the backend sends a relative path
      videoUrl: json['video_url'],
    );
  }
}